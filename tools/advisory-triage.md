# Security Advisory Triage — TC Oncall Guide

## Overview

When you are TC oncall, part of your responsibility is triaging incoming
security advisories across the open-telemetry organization. GitHub security
advisories are **private by default** — only repo admins and explicitly
invited collaborators can see them. Component owners typically cannot see
advisories filed against their components unless someone adds them.

This document and the accompanying script help you assign advisories to the
right people quickly.

## Quick start

```bash
# 1. Dry run — see what would happen
python3 tools/assign-advisories.py --checkout /path/to/opentelemetry-collector-contrib

# 2. Review the output, then apply
python3 tools/assign-advisories.py --checkout /path/to/opentelemetry-collector-contrib --apply
```

## What the script does

1. Fetches all security advisories in **triage** state from the repo via
   the GitHub API.

2. For each advisory, reads the `vulnerabilities[].package.name` field to
   determine which Go module / component is affected (e.g.,
   `github.com/open-telemetry/opentelemetry-collector-contrib/exporter/kafkaexporter`).

3. Maps that package path to a component directory and reads the `active`
   codeowners from that component's `metadata.yaml`.

4. Adds those codeowners as **collaborating users** on the advisory. This
   gives them access to see the advisory, discuss it, and develop a fix
   in a private fork.

**Important**: The GitHub API uses **replace** semantics for
`collaborating_users`, so the script always merges existing collaborators
with the new ones before sending the PATCH request.

## Prerequisites

- **`gh` CLI** authenticated with a token that has `repo` and
  `security_events` scopes.
- **Repo admin** or **security manager** role on the target repository.
- A local checkout of the target repository (for reading `metadata.yaml`
  files). The script auto-detects common locations or you can pass
  `--checkout /path/to/repo`.

## Options

| Flag | Description |
|------|-------------|
| `--apply` | Actually assign collaborators (default is dry-run) |
| `--repo owner/repo` | Target a different repo (default: `open-telemetry/opentelemetry-collector-contrib`) |
| `--checkout /path` | Path to the local repo checkout |
| `--ghsa GHSA-xxx` | Process a single advisory by GHSA ID |
| `-h`, `--help` | Show usage |

You can also set `REPO`, `CONTRIB_CHECKOUT`, and `GHSA_FILTER` as environment
variables.

## Triage workflow

### Step 1: Get the lay of the land

Use the org audit log to see recent advisory activity:

```
https://github.com/organizations/open-telemetry/settings/audit-log?q=action%3Arepository_advisory.open
```

### Step 2: Run the assignment script (dry run first)

```bash
python3 tools/assign-advisories.py
```

Review the output. Advisories marked `⚠` have no component mapping — these
are typically dependency CVE reports or advisories where the reporter didn't
fill in the vulnerability metadata correctly. You'll need to handle those
manually.

### Step 3: Apply the assignments

```bash
python3 tools/assign-advisories.py --apply
```

Component owners will now be able to see the advisories and will receive
GitHub notifications.

### Step 4: Evaluate advisories on merit

For each advisory, the TC oncall should assess:

- **Is the reporter likely human or a bot/script?** Check the audit log for
  rapid-fire submissions, programmatic access tokens, or suspicious
  user-agents.
- **Is the vulnerability claim plausible?** Check the actual source code at
  the lines referenced.
- **What action is needed?**
  - **Accept and open as draft** — vulnerability is real, proceed to fix
  - **Collaborate on a patch in private** — create a private fork for the fix
  - **Close security advisory** — false positive, duplicate, or not applicable

### Step 5: Follow up

For legitimate advisories, ensure the component owners have a plan:

- Is someone working on a fix?
- Does it need a CVE?
- Is there a release timeline?

## Handling advisories the script can't map

Some advisories won't have a clean package→component mapping. Common cases:

- **Dependency CVEs** (e.g., `github.com/moby/moby`): Check whether the
  vulnerable dependency version is actually in use. Often these are already
  fixed or not exploitable.
- **Cross-cutting issues** (e.g., gzip bomb across many receivers): Assign
  to the approvers team or handle at the TC level.
- **Missing metadata**: The reporter didn't fill in the vulnerable package
  field. Look at the description to determine the component.

## Adapting for other repos

The script works with any repo that uses the collector-contrib `metadata.yaml`
convention for codeowners. To use it with a different repo:

```bash
python3 tools/assign-advisories.py --repo open-telemetry/opentelemetry-collector --checkout /path/to/collector
```
