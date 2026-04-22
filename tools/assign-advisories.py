#!/usr/bin/env python3
"""
assign-advisories.py — Assign security advisory collaborators from CODEOWNERS

Finds all "triage" state security advisories in a repo, determines which
component is affected from the advisory's vulnerability metadata, looks up
the codeowners for that component, and adds them as collaborating users on
the advisory so they can see and work on it.

Prerequisites:
  - gh CLI authenticated with a token that has repo + security_events scope
  - You must be a repo admin or security manager for the target repo
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REPO = "open-telemetry/opentelemetry-collector-contrib"

# Where to look for a local repo checkout, relative to this script or CWD.
CHECKOUT_CANDIDATES = [
    "../opentelemetry-collector-contrib",
    "{script_dir}/../opentelemetry-collector-contrib",
    os.path.expanduser("~/src/otel/opentelemetry-collector-contrib"),
]


def find_checkout(repo):
    """Auto-detect a local checkout by looking for versions.yaml or go.mod."""
    repo_name = repo.split("/")[-1]

    candidates = [
        f"../{repo_name}",
        os.path.join(os.path.dirname(__file__), "..", repo_name),
        os.path.expanduser(f"~/src/otel/{repo_name}"),
    ]
    for candidate in candidates:
        candidate = os.path.realpath(candidate)
        if os.path.isdir(candidate) and (
            os.path.isfile(os.path.join(candidate, "versions.yaml"))
            or os.path.isfile(os.path.join(candidate, "go.mod"))
        ):
            return candidate
    return None


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


def get_codeowners(checkout, component_dir):
    """Read active codeowners from a component's metadata.yaml."""
    metadata_path = os.path.join(checkout, component_dir, "metadata.yaml")
    if not os.path.isfile(metadata_path):
        return []
    try:
        with open(metadata_path) as f:
            content = f.read()
        # Match both inline list and multi-line list formats.
        match = re.search(r"active:\s*\[([^\]]+)\]", content)
        if match:
            return [o.strip().strip("'\"") for o in match.group(1).split(",")]
    except Exception:
        pass
    return []


def process_advisories(advisories, *, repo, checkout, dry_run):
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
            print()
            unmapped += 1
            continue

        all_owners = sorted({
            owner
            for comp_dir in component_dirs
            for owner in get_codeowners(checkout, comp_dir)
        })

        if not all_owners:
            print(f"\u26a0  {ghsa} [{severity}]")
            print(f"   {summary}")
            print(f"   Component {component_dirs} has no codeowners in metadata.yaml")
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
        "--checkout",
        default=os.environ.get("CONTRIB_CHECKOUT", ""),
        help="Path to local repo checkout (auto-detected if omitted)",
    )
    parser.add_argument(
        "--ghsa",
        default=os.environ.get("GHSA_FILTER", ""),
        help="Process a single advisory by GHSA ID",
    )
    args = parser.parse_args()

    checkout = args.checkout or find_checkout(args.repo)
    if not checkout or not os.path.isdir(checkout):
        print(
            "ERROR: Cannot find local repo checkout.\n"
            "Use --checkout /path/to/repo or set CONTRIB_CHECKOUT env var.",
            file=sys.stderr,
        )
        sys.exit(1)
    checkout = os.path.realpath(checkout)

    mode = "DRY RUN (use --apply to execute)" if not args.apply else "APPLY"
    print(f"Repository:  {args.repo}")
    print(f"Checkout:    {checkout}")
    print(f"Mode:        {mode}")
    print("---\n")

    advisories = fetch_advisories(args.repo, ghsa_filter=args.ghsa or None)
    print(f"Found {len(advisories)} advisories in triage state.\n")

    process_advisories(
        advisories,
        repo=args.repo,
        checkout=checkout,
        dry_run=not args.apply,
    )


if __name__ == "__main__":
    main()
