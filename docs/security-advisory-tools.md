# Security Advisory Tools

Scripts for managing GitHub security advisories in the OpenTelemetry organization.
Both require the `gh` CLI with `repo` + `security_events` scopes, and repo admin or security manager access.

## assign-advisories.py

Assigns component codeowners as collaborators on triage-state security advisories so they can view and respond to them.
The script fetches CODEOWNERS from the GitHub API -- no local checkout needed.

```bash
python3 tools/assign-advisories.py            # dry run
python3 tools/assign-advisories.py --apply    # apply changes
```

| Flag | Description |
|------|-------------|
| `--apply` | Assign collaborators (default is dry-run) |
| `--repo OWNER/REPO` | Target repo (default: `open-telemetry/opentelemetry-collector-contrib`) |
| `--ghsa GHSA-xxxx` | Process a single advisory |

## downgrade-advisory.py

Converts a security advisory into a public bug report issue, scrubbing reporter identity and sensitive metadata.
Use this when a report doesn't warrant a CVE but should be tracked as a regular bug.

```bash
python3 tools/downgrade-advisory.py GHSA-xxxx-xxxx-xxxx            # preview
python3 tools/downgrade-advisory.py GHSA-xxxx-xxxx-xxxx --apply    # create issue
```

| Flag | Description |
|------|-------------|
| `--apply` | Create the issue (default is dry-run preview) |
| `--repo OWNER/REPO` | Source repo (default: `open-telemetry/opentelemetry-collector-contrib`) |
| `--target-repo OWNER/REPO` | Repo to create the issue in (defaults to `--repo`) |
| `--label LABEL` | Labels for the issue (repeatable) |
