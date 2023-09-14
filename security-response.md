# Security Response Guidelines

Security vulnerabilities should be handled quickly and sometimes privately. The
primary goal of this process is to reduce the total time users are vulnerable to
publicly known exploits.

The OpenTelemetry Technical Committee (OTel TC) and relevant repo maintainers,
supported by tooling provided by the SIG-Security, are responsible for
responding to the incident organizing the entire response including internal
communication and external disclosure.

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

## Disclosures

### Private Disclosure Processes

In order for the vulnerability reports to reach maintainers as soon as possible,
the preferred way is to use the `Report a vulnerability` button on the
`Security` tab in the respective GitHub repository. It creates a private
communication channel between the reporter and the maintainers.

If you are absolutely unable to or have strong reasons not to use GitHub
reporting workflow, please reach out to the Technical Committee using
[cncf-opentelemetry-tc@lists.cncf.io](mailto:cncf-opentelemetry-tc@lists.cncf.io)
and we will provide instruction on how to report the vulnerability using an
encrypted message, if desired.

[gh-organization]: https://github.com/open-telemetry

### Public Disclosure Processes

If you know of a publicly disclosed security vulnerability please IMMEDIATELY
email
[cncf-opentelemetry-tc@lists.cncf.io](mailto:cncf-opentelemetry-tc@lists.cncf.io)
to inform the Security Response Committee (SRC) about the vulnerability so they
may start the patch, release, and communication process.

The TC should receive the message and re-direct it to the relevant repo
maintainers for ownership. If possible the repo maintainers will engage and ask
the person making the public report if the issue can be handled via a private
disclosure process. If the reporter denies the request, the repo maintainers
will move swiftly with the fix and release process. In extreme cases you can ask
GitHub to delete the issue but this generally isn't necessary and is unlikely to
make a public disclosure less damaging.

## Patch, Release, and Public Communication

For each vulnerability, a member of the TC will volunteer track issue resolution
with the relevant repo owners. This TC member will be referred to as the Fix
Lead and is not responsible for incident remediation or implementation.

The role of Fix Lead should rotate round-robin across the TC.

### Fix Team Organization

The Fix Team is made up of the Fix Team Lead and the relevant repo maintainers as Fix Responders.

### Fix Development Process

All of the timelines below are suggestions that assume a Private Disclosure and that the report is accepted as valid. These steps should be completed within the 1-7 days of Disclosure.

- The TC is notified of an incident, a member volunteers to track the issue as Fix Lead, and the relevant repo maintainers are added as the Fix Team to the issue.
- The Fix Responders will create a
  [CVSS](https://www.first.org/cvss/specification-document) score using the
  [CVSS Calculator](https://www.first.org/cvss/calculator/3.0) and share it with the Fix Lead.
- The Fix Responders will request a CVE from GitHub.
- The Fix Responders will notify the Fix Lead that work on the fix branch is complete
  once there are LGTMs on all commits in the temporary private fork created for the GitHub Security Advisory.

### Fix Disclosure Process

OTel relies on GitHub tooling to notify the affected repositories and publish a
security advisory. GitHub will publish the CVE to the CVE List, broadcast the
Security Advisory via the GitHub Advisory Database, and send security alerts to
all repositories that use the package and have alerts on.

#### Fix Release Day

The Fix Responders as repo owners will release an updated version after confirming
approval with the Fix Lead.

## Severity

The Technical Committee evaluates vulnerability severity on a case-by-case
basis, guided by CVSS 3.1.

## Retrospective

TBD
