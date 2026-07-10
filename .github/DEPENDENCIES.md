# Dependency update tooling

This repository uses both Renovate and Dependabot, with strictly separated
responsibilities. Do not enable a feature in one tool that the other already
owns.

## Split of responsibilities

| Concern | Tool |
| --- | --- |
| Routine Python dependency updates | Renovate |
| `pip-compile` output refreshes | Renovate |
| GitHub Actions updates | Renovate |
| Alert-driven GitHub Actions security updates | Dependabot |
| Alert-driven direct dependency security updates | Dependabot |
| Alert-driven transitive dependency security updates | Dependabot |

Configuration files:

- [renovate.json5](renovate.json5)
- [dependabot.yml](dependabot.yml)

## Why the split

Renovate owns routine maintenance. It updates the direct Python requirements,
refreshes the compiled requirements file and its hashes, and keeps GitHub
Actions pinned to full commit hashes.

Dependabot complements Renovate with updates driven by GitHub security alerts.
GitHub's dependency graph includes the resolved dependencies from
`tools/update-cve-data-requirements.txt` and the actions referenced by the
repository's workflows, so Dependabot can evaluate both direct and transitive
dependencies. `open-pull-requests-limit: 0` disables routine Dependabot pull
requests without disabling security updates.

Dependabot can create an update only when GitHub has an applicable alert and can
determine an available remediation. Alerts that cannot be remediated
automatically still require maintainer investigation.

GitHub does not apply Dependabot cooldown settings to security updates. The
cooldown values in [dependabot.yml](dependabot.yml) satisfy zizmor and would take
effect only if routine Dependabot updates were enabled in the future.
