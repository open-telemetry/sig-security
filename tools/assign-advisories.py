#!/usr/bin/env python3
"""
assign-advisories.py — Assign security advisory collaborators from CODEOWNERS

Finds all "triage" state security advisories in a repo, determines which
component is affected from the advisory's vulnerability metadata, looks up
the codeowners for that component via the repo's CODEOWNERS file, and adds
them as collaborating users on the advisory so they can see and work on it.

No local checkout is required — CODEOWNERS is fetched from the GitHub API.

Prerequisites:
  - gh CLI authenticated with a token that has repo + security_events scope
  - You must be a repo admin or security manager for the target repo
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

DEFAULT_REPO = "open-telemetry/opentelemetry-collector-contrib"


def gh_api(endpoint, method="GET", input_data=None):
    """Call the GitHub API via the gh CLI."""
    cmd = ["gh", "api"]
    if method != "GET":
        cmd += ["--method", method]
    cmd.append(endpoint)
    if input_data is not None:
        cmd += ["--input", "-"]
    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None, result.stderr.strip()[:300]
    return json.loads(result.stdout), None


def fetch_codeowners(repo):
    """Fetch and parse the CODEOWNERS file from the repo.

    Returns a dict mapping directory paths (without trailing slash) to
    lists of individual GitHub usernames (teams are excluded since they
    cannot be added as advisory collaborators).
    """
    data, err = gh_api(f"/repos/{repo}/contents/.github/CODEOWNERS")
    if err:
        print(f"ERROR: Failed to fetch CODEOWNERS: {err}", file=sys.stderr)
        sys.exit(1)

    content = base64.b64decode(data["content"]).decode()
    owners_map = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        path = parts[0].rstrip("/")
        # Keep only individual users (skip teams like @org/team-name).
        users = [p.lstrip("@") for p in parts[1:] if "/" not in p]
        if users:
            owners_map[path] = users
    return owners_map


def fetch_advisories(repo, ghsa_filter=None):
    """Fetch advisories from the GitHub API."""
    if ghsa_filter:
        data, err = gh_api(f"/repos/{repo}/security-advisories/{ghsa_filter}")
        if err:
            print(f"ERROR: Failed to fetch advisory {ghsa_filter}: {err}", file=sys.stderr)
            sys.exit(1)
        return [data]

    # Paginate through all triage advisories.
    result = subprocess.run(
        ["gh", "api", f"/repos/{repo}/security-advisories?per_page=100&state=triage", "--paginate"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: Failed to list advisories: {result.stderr.strip()[:300]}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def get_component_dir(pkg_name, repo):
    """Map a Go package to a component directory relative to the repo root."""
    prefix = f"github.com/{repo}/"
    if pkg_name.startswith(prefix):
        return pkg_name[len(prefix):]
    # Bare relative path (e.g. "exporter/kafkaexporter")
    if "/" in pkg_name and not pkg_name.startswith("github.com"):
        return pkg_name
    return None


def lookup_owners(owners_map, component_dir):
    """Find codeowners for a component directory using the CODEOWNERS map.

    Tries the exact path first, then walks up parent directories to find
    the most specific matching rule (mirroring GitHub's CODEOWNERS logic
    where the last matching pattern wins — but since we search most-specific
    first, the first match is correct).
    """
    path = component_dir
    while path:
        if path in owners_map:
            return owners_map[path]
        parent = path.rsplit("/", 1)[0] if "/" in path else ""
        if parent == path:
            break
        path = parent
    return []


def summarize_engagement(adv):
    """Summarize engagement on an advisory beyond the original reporter.

    Returns a human-readable string describing who has interacted with
    the advisory based on available API fields.
    """
    author = adv.get("author", {}).get("login", "unknown")
    collabs = [u["login"] for u in adv.get("collaborating_users", [])]
    collab_teams = [t["name"] for t in adv.get("collaborating_teams", [])]
    credits = adv.get("credits", []) or []
    credited_users = [c["user"]["login"] for c in credits if c.get("user")]
    cve_id = adv.get("cve_id")

    created = adv.get("created_at", "")
    updated = adv.get("updated_at", "")

    # Determine who has engaged besides the reporter.
    others = [c for c in collabs if c != author]

    signals = []
    if others:
        signals.append(f"collaborators: {', '.join(others)}")
    if collab_teams:
        signals.append(f"teams: {', '.join(collab_teams)}")
    if credited_users:
        credited_others = [u for u in credited_users if u != author]
        if credited_others:
            signals.append(f"credited: {', '.join(credited_others)}")
    if cve_id:
        signals.append(f"CVE: {cve_id}")

    # Check if updated significantly after creation.
    if created and updated and created != updated:
        try:
            ct = datetime.fromisoformat(created.replace("Z", "+00:00"))
            ut = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            delta = ut - ct
            if delta.total_seconds() > 300:  # more than 5 minutes
                signals.append(f"updated {_human_delta(delta)} after creation")
        except (ValueError, TypeError):
            pass

    if not signals:
        return f"No engagement beyond reporter ({author})"
    return f"Reporter: {author} | {'; '.join(signals)}"


def _human_delta(delta):
    """Format a timedelta as a human-readable string."""
    seconds = int(delta.total_seconds())
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"


def process_advisories(advisories, *, repo, owners_map, dry_run):
    """Process each advisory: resolve codeowners and optionally assign them."""
    added = 0
    skipped = 0
    failed = 0
    unmapped = 0

    for adv in advisories:
        ghsa = adv["ghsa_id"]
        summary = adv["summary"][:90]
        severity = adv.get("severity", "unset")
        existing_collabs = [u["login"] for u in adv.get("collaborating_users", [])]

        pkg_names = [
            v["package"]["name"]
            for v in adv.get("vulnerabilities", [])
            if v.get("package", {}).get("name")
        ]

        component_dirs = [
            d for pkg in pkg_names if (d := get_component_dir(pkg, repo))
        ]

        if not component_dirs:
            print(f"\u26a0  {ghsa} [{severity}]")
            print(f"   {summary}")
            print(f"   No component mapping (packages: {pkg_names})")
            print(f"   {summarize_engagement(adv)}")
            print()
            unmapped += 1
            continue

        all_owners = sorted({
            owner
            for comp_dir in component_dirs
            for owner in lookup_owners(owners_map, comp_dir)
        })

        if not all_owners:
            print(f"\u26a0  {ghsa} [{severity}]")
            print(f"   {summary}")
            print(f"   Component {component_dirs} has no codeowners")
            print(f"   {summarize_engagement(adv)}")
            print()
            unmapped += 1
            continue

        new_owners = [o for o in all_owners if o not in existing_collabs]
        merged = sorted(set(existing_collabs) | set(all_owners))

        icon = "\U0001f4cb" if new_owners else "\u2705"
        print(f"{icon} {ghsa} [{severity}]")
        print(f"   {summary}")
        print(f"   Component:  {', '.join(component_dirs)}")
        print(f"   Owners:     {', '.join(all_owners)}")
        if existing_collabs:
            print(f"   Existing:   {', '.join(existing_collabs)}")
        print(f"   {summarize_engagement(adv)}")

        if not new_owners:
            print("   \u2192 All owners already assigned")
            skipped += 1
        elif dry_run:
            print(f"   \u2192 Would add: {', '.join(new_owners)}")
            added += 1
        else:
            payload = json.dumps({"collaborating_users": merged})
            resp, err = gh_api(
                f"/repos/{repo}/security-advisories/{ghsa}",
                method="PATCH",
                input_data=payload,
            )
            if resp is not None:
                final = [u["login"] for u in resp.get("collaborating_users", [])]
                print(f"   \u2705 Added {', '.join(new_owners)}")
                print(f"   Collaborators now: {', '.join(final)}")
                added += 1
            else:
                print(f"   \u274c FAILED: {err}")
                failed += 1

        print()

    print("=" * 60)
    verb = "would update" if dry_run else "updated"
    print(
        f"Summary: {added} {verb}, "
        f"{skipped} already assigned, "
        f"{unmapped} unmapped, "
        f"{failed} failed"
    )
    if dry_run and added > 0:
        print("\nRe-run with --apply to execute changes.")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually assign collaborators (default is dry-run)",
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("REPO", DEFAULT_REPO),
        help=f"Target repository (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "--ghsa",
        default=os.environ.get("GHSA_FILTER", ""),
        help="Process a single advisory by GHSA ID",
    )
    args = parser.parse_args()

    mode = "DRY RUN (use --apply to execute)" if not args.apply else "APPLY"
    print(f"Repository:  {args.repo}")
    print(f"Mode:        {mode}")
    print("---\n")

    print("Fetching CODEOWNERS...", end=" ", flush=True)
    owners_map = fetch_codeowners(args.repo)
    print(f"{len(owners_map)} entries loaded.\n")

    advisories = fetch_advisories(args.repo, ghsa_filter=args.ghsa or None)
    print(f"Found {len(advisories)} advisories in triage state.\n")

    process_advisories(
        advisories,
        repo=args.repo,
        owners_map=owners_map,
        dry_run=not args.apply,
    )


if __name__ == "__main__":
    main()
