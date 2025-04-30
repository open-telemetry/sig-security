# Security Response Guidelines

Security vulnerabilities should be handled quickly and sometimes privately. The
primary goal of this process is to reduce the total time users are vulnerable to
publicly known exploits.

The relevant OTel repository maintainers, supported by the Security SIG and
OpenTelemetry Technical Committee (OTel TC), are responsible for responding to
the incident including internal communication and external disclosure.

## Supported Versions

The OTel project provides community support only for the last overall minor
version: bug fixes are released either as part of the next minor version or as
an on-demand patch version. Independent of which version is next, all patch
versions are cumulative, meaning that they represent the state of our `main`
branch at the moment of the release. For instance, if the latest version is
0.10.0, bug fixes are released either as part of 0.11.0 or 0.10.1.

Security fixes are given priority and might be enough to cause a new version to
be released. Each repository is entitled to establish their own complementary
processes. SIG-Security in conjunction with the TC can advise in case
clarifications are required.

## Reporting Process - For Vulnerability Reporters

### Reporting Methods

In order for the vulnerability reports to reach maintainers as soon as possible,
the preferred way is to use the `Report a vulnerability` button on the
`Security` tab in the respective GitHub repository. It creates a private
communication channel between the reporter and the maintainers.

If you are unable to or have strong reasons not to use the GitHub
reporting workflow, please reach out to the Technical Committee using
[cncf-opentelemetry-tc@lists.cncf.io](mailto:cncf-opentelemetry-tc@lists.cncf.io)
and we will provide instruction on how to report the vulnerability using an
encrypted message, if desired. The TC should receive the message and re-direct
it to the relevant repository maintainers for ownership.

Reports should be acknowledged within 3 working days.

**Please avoid reporting any vulnerabilities as a generic public "Issue" in
GitHub.**

Given the public visibility of GitHub issues, reporting a vulnerability as a
GitHub issue would be public disclosure. If this is done accidentally or if you
notice a vulnerability reported this way, please immediately re-report the
vulnerability using "Report a vulnerability" and note the public disclosure as
part of that report. You can ask GitHub to delete the issue but this shouldn't
be considered a sufficient mitigation and the vulnerability should be considered
publicly disclosed.

### Non-Public Vulnerabilities

If a vulnerability appears to be not publicly known or disclosed, the repository
maintainers will engage and the reporter is requested to honor an embargo period
in which the vulnerability is keep private until a fix can be released and
disclosed in an orderly manner. If the reporter has a need to disclose the
vulnerability further, perhaps for a security conference or other obligation,
they are asked to negotiate the disclosure date with the maintainers fixing the
vulnerability. The repository maintainers will in any case do their best to move
swiftly with the fix and release process.

### Publicly Known Vulnerabilities

If you discover an unreported publicly disclosed/known vulnerability please
IMMEDIATELY use the reporting methods above to inform the team about the
vulnerability so they may start the patch, release and communication process.
Please include any relevant information about current public exploitations of
this vulnerability, if known, to help with scoring and prioritization.

## Patch, Release, and Public Communication

### Fix Team Organization

The Fix Team is made up of the relevant repository maintainers and a Fix Lead is
responsible for ensuring the successful execution of the incident response.

### TC Role

- Assign a Fix Lead, typically a code owner or maintainer for the affected code
- A member of the TC will need to review the proposed CVSS score and severity
  from the Fix Team
- Acknowledge when a proposed fix is completed

### Fix Development Process

All of the timelines below are suggestions that assume a Private Disclosure and
that the report is accepted as valid.

#### Initial Incident Response

- The TC is notified of an incident and the relevant repository maintainers are
  added automatically using a Zapier workflow as the Fix Team to the issue.
- The Fix Team acknowledges the incident to the reporter, asks for further
  details if necessary, and begins mitigation planning.
- The Fix Team confirms with the reporter if the incident is valid and requires
  a fix.
- The Fix Team creates a temporary Slack channel and private branch to start
  work on the fix.
- The Fix Team will create a
  [CVSS](https://www.first.org/cvss/specification-document) Base score using the
  [CVSS Calculator](https://www.first.org/cvss/calculator/3.1) and ping the TC
  GitHub team for confirmation.
- The Fix Team will request a CVE from GitHub and follow up with the reporter.
- The Fix Team will report the CVE to the [security contact
  list](./docs/contact-list.md) if applicable.
- The Fix Team publishes the CVE to the GitHub Security Advisory Database for
  user notification.

#### Incident Mitigation

The incident mitigation timeline depends on the severity of the incident and
repository release cadence.

- The Fix Team will ping the TC GitHub team to alert them that work on the fix
  branch is complete once there are LGTMs on all commits in the temporary
  private fork created for the GitHub Security Advisory.
- The updated version is released with the fix.
- The incident is published to the GitHub Security Advisory Database and
  affected users are automatically notified using GitHub security alerts.

### Fix Disclosure Process

OTel relies on GitHub tooling to notify the affected repositories and publish a
security advisory. GitHub will publish the CVE to the CVE List, broadcast the
Security Advisory via the GitHub Advisory Database, and send security alerts to
all repositories that use the package and have alerts on. The CVE will also be
added to the [OTel website's CVE
feed](https://opentelemetry.io/docs/security/cve/).

#### Fix Release Day

The Fix Team as repository owners will release an updated version and optionally
notify their communities via Slack.

## Severity

The Fix Team evaluates vulnerability severity on a case-by-case basis, guided by
CVSS 3.1 and is subject to TC review.

## Retrospective

TBD
