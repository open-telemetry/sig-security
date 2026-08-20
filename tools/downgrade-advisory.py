#!/usr/bin/env python3
"""downgrade-advisory.py -- Convert a security advisory into a public bug report

Fetches a repository security advisory by GHSA ID, scrubs reporter
identity and sensitive metadata, and creates a public GitHub issue
with the technical description preserved.

This is a "downgrade" operation: the maintainer decides the report
does not warrant a CVE and instead publishes it as a regular issue.

Prerequisites: (1) gh CLI authenticated with a token that has the repo
scope; (2) Security manager or admin of the source repo, or a
collaborator on the advisory.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap

DEFAULT_REPO = "open-telemetry/opentelemetry-collector-contrib"

# Matches a GitHub security-advisory URL, capturing "owner/repo" and the GHSA ID.
ADVISORY_URL_RE = re.compile(
    r"github\.com/(?P<repo>[^/\s]+/[^/\s]+)/security/advisories/"
    r"(?P<ghsa>GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4})",
    re.IGNORECASE,
)


def parse_advisory_arg(value):
    """Resolve the positional arg into (repo_or_None, ghsa_id).

    Accepts either a bare GHSA ID or a full advisory URL such as
    https://github.com/<owner>/<repo>/security/advisories/GHSA-xxxx-xxxx-xxxx.
    When a URL is given, the repo it points at is returned so it can override
    the default; for a bare GHSA ID the repo is None.
    """
    m = ADVISORY_URL_RE.search(value)
    if m:
        return m.group("repo"), m.group("ghsa")
    return None, value


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
        print(f"ERROR: Failed to fetch {ghsa_id} from {repo}: {err}", file=sys.stderr)
        if "Not Found" in err or "404" in err:
            print(
                "HINT: The advisory may live in a different repository. Pass "
                "--repo <owner>/<repo> or the full advisory URL to point at "
                "the repo that owns it.",
                file=sys.stderr,
            )
        sys.exit(1)
    return data


def scrub_description(description, reporter_login):
    """Remove reporter identity and sensitive metadata from description.

    Strips: @mentions of the reporter, "Reported by", "Discovered by",
    "Submitted by", "Assisted-by" lines, GitHub username references.
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


def format_issue_body(adv, scrubbed_desc, author):
    """Build the issue body from the advisory data."""
    parts = []

    # Origin note.
    parts.append(
        f"> Downgraded from security advisory {adv['ghsa_id']}. Identifying "
        f"details have been removed. @{author} reviewed the original issue "
        f"and [determined that a security response is not required](https://github.com/open-telemetry/sig-security/blob/main/security-response.md)."
    )
    parts.append("")

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
        "--body-file", "-",
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

    result = subprocess.run(cmd, input=body, capture_output=True, text=True)
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
        help="GHSA ID (e.g. GHSA-xxxx-xxxx-xxxx) or full advisory URL",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help=f"Source repository; overrides the repo in a URL "
        f"(default: $REPO or {DEFAULT_REPO})",
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

    # The positional arg may be a bare GHSA ID or a full advisory URL.
    url_repo, ghsa_id = parse_advisory_arg(args.ghsa_id)
    # Precedence for the source repo: explicit --repo > URL > $REPO > default.
    source_repo = (
        args.repo or url_repo or os.environ.get("REPO", DEFAULT_REPO)
    )
    target_repo = args.target_repo or source_repo

    # Fetch the advisory.
    print(f"Fetching {ghsa_id} from {source_repo}...")
    adv = fetch_advisory(source_repo, ghsa_id)

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
    author, err = gh_api("/user")
    if err or not author:
        print("ERROR: Could not determine authenticated user.", file=sys.stderr)
        sys.exit(1)
    author_login = author["login"]
    title = summary
    body = format_issue_body(adv, scrubbed, author_login)

    # Create or preview.
    labels = args.label or ["bug"]
    issue_url = create_issue(target_repo, title, body, labels, dry_run=not args.apply)

    if issue_url:
        print(f"\nIssue created: {issue_url}")

        # Close the advisory and append a note linking to the issue.
        close_note = (
            f"{description}\n\n---\n\n"
            f"Reviewed and converted to a public issue: {issue_url}"
        )
        payload = json.dumps({"state": "closed", "description": close_note})
        _, err = gh_api(
            f"/repos/{source_repo}/security-advisories/{ghsa_id}",
            method="PATCH",
            input_data=payload,
        )
        if err:
            print(f"\nWARNING: Failed to close advisory: {err}", file=sys.stderr)
            print(f"Manually close {ghsa_id}.")
        else:
            print(f"Advisory {ghsa_id} closed.")


if __name__ == "__main__":
    main()
