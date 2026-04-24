#!/usr/bin/env python3
"""
downgrade-advisory.py — Convert a security advisory into a public bug report

Fetches a repository security advisory by GHSA ID, scrubs reporter
identity and sensitive metadata, and creates a public GitHub issue
with the technical description preserved.

This is a "downgrade" operation: the maintainer decides the report
does not warrant a CVE and instead publishes it as a regular bug.

Prerequisites:
  - gh CLI authenticated with a token that has repo + security_events scope
  - You must be a repo admin or security manager for the source repo
"""

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap

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
        cmd, input=input_data, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, result.stderr.strip()[:300]
    return json.loads(result.stdout), None


def fetch_advisory(repo, ghsa_id):
    """Fetch a single advisory by GHSA ID."""
    data, err = gh_api(f"/repos/{repo}/security-advisories/{ghsa_id}")
    if err:
        print(f"ERROR: Failed to fetch {ghsa_id}: {err}", file=sys.stderr)
        sys.exit(1)
    return data


def scrub_description(description, reporter_login):
    """Remove reporter identity and sensitive metadata from description.

    Strips:
      - @mentions of the reporter
      - "Reported by", "Discovered by", "Submitted by", "Assisted-by" lines
      - GitHub username references to the reporter
    """
    lines = description.splitlines()
    scrubbed = []
    for line in lines:
        # Skip lines that attribute the report to someone.
        stripped = line.strip().lower()
        if any(
            stripped.startswith(prefix)
            for prefix in [
                "reported by",
                "reported-by:",
                "discovered by",
                "submitted by",
                "assisted-by:",
                "assisted by",
                "credit:",
                "credits:",
            ]
        ):
            continue

        # Replace @reporter mentions with generic text.
        line = re.sub(
            rf"@{re.escape(reporter_login)}\b",
            "[reporter]",
            line,
            flags=re.IGNORECASE,
        )
        scrubbed.append(line)

    return "\n".join(scrubbed).strip()


def format_issue_body(adv, scrubbed_desc):
    """Build the issue body from the advisory data."""
    parts = []

    # Origin note.
    parts.append(
        f"> Downgraded from security advisory {adv['ghsa_id']}. "
        f"The original report was reviewed and determined not to require a CVE."
    )
    parts.append("")

    # Severity and CWEs.
    severity = adv.get("severity") or "unset"
    cwes = [c["cwe_id"] for c in adv.get("cwes", [])]
    cvss = adv.get("cvss", {}) or {}
    meta = [f"**Severity:** {severity}"]
    if cvss.get("vector_string"):
        meta.append(f"**CVSS:** {cvss['score']} ({cvss['vector_string']})")
    if cwes:
        meta.append(f"**CWEs:** {', '.join(cwes)}")
    parts.append(" · ".join(meta))
    parts.append("")

    # Affected packages.
    vulns = adv.get("vulnerabilities", [])
    if vulns:
        parts.append("### Affected components")
        parts.append("")
        for v in vulns:
            pkg = v.get("package", {}).get("name", "unknown")
            vrange = v.get("vulnerable_version_range", "")
            patched = v.get("patched_versions", "")
            line = f"- `{pkg}`"
            if vrange:
                line += f" {vrange}"
            if patched:
                line += f" (fixed in {patched})"
            parts.append(line)
        parts.append("")

    # Main description.
    parts.append(scrubbed_desc)

    return "\n".join(parts)


def create_issue(repo, title, body, labels, dry_run):
    """Create a GitHub issue via gh CLI."""
    cmd = [
        "gh", "issue", "create",
        "--repo", repo,
        "--title", title,
        "--body", body,
    ]
    for label in labels:
        cmd += ["--label", label]

    if dry_run:
        print("Would create issue:")
        print(f"  Repo:   {repo}")
        print(f"  Title:  {title}")
        print(f"  Labels: {', '.join(labels) if labels else '(none)'}")
        print(f"  Body length: {len(body)} chars")
        print()
        print("--- Issue body preview ---")
        print(body)
        print("--- End preview ---")
        return None

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: Failed to create issue: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    issue_url = result.stdout.strip()
    return issue_url


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "ghsa_id",
        help="GHSA ID of the advisory to downgrade (e.g. GHSA-xxxx-xxxx-xxxx)",
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("REPO", DEFAULT_REPO),
        help=f"Source repository (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "--target-repo",
        default=None,
        help="Repository to create the issue in (defaults to --repo)",
    )
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help="Labels to add to the issue (can be repeated)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually create the issue (default is dry-run / preview)",
    )
    args = parser.parse_args()

    target_repo = args.target_repo or args.repo

    # Fetch the advisory.
    print(f"Fetching {args.ghsa_id} from {args.repo}...")
    adv = fetch_advisory(args.repo, args.ghsa_id)

    summary = adv["summary"]
    reporter = adv.get("author", {}).get("login", "unknown")
    description = adv.get("description", "")
    severity = adv.get("severity") or "unset"
    state = adv["state"]

    print(f"  Summary:  {summary[:80]}")
    print(f"  Severity: {severity}")
    print(f"  State:    {state}")
    print(f"  Reporter: [REDACTED]")
    print()

    # Scrub and build the issue.
    scrubbed = scrub_description(description, reporter)
    title = f"[{severity.upper()}] {summary}"
    body = format_issue_body(adv, scrubbed)

    # Create or preview.
    labels = args.label or ["bug"]
    issue_url = create_issue(target_repo, title, body, labels, dry_run=not args.apply)

    if issue_url:
        print(f"\nIssue created: {issue_url}")
        print(
            f"\nRemember to close the advisory {args.ghsa_id} "
            f"and link to this issue."
        )


if __name__ == "__main__":
    main()
