# Security Response Guidelines

Security vulnerabilities should be handled quickly and sometimes privately. The
primary goal of this process is to reduce the total time users are vulnerable to
publicly known exploits.

The OpenTelemetry (OTel) Technical Committee (TC) and relevant repo maintainers,
supported by tooling provided by the Sig-Security, are responsible for
responding to the incident organizing the entire response including internal
communication and external disclosure.

## Supported Versions

The OTel project provides community support only for the last minor
version: bug fixes are released either as part of the next minor version or as
an on-demand patch version. Independent of which version is next, all patch
versions are cumulative, meaning that they represent the state of our `main`
branch at the moment of the release. For instance, if the latest version is
0.10.0, bug fixes are released either as part of 0.11.0 or 0.10.1.

Security fixes are given priority and might be enough to cause a new version to
be released.

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
encrypted message.

[gh-organization]: https://github.com/open-telemetry

### Public Disclosure Processes

If you know of a publicly disclosed security vulnerability please IMMEDIATELY
email
[cncf-opentelemetry-tc@lists.cncf.io](mailto:cncf-opentelemetry-tc@lists.cncf.io)
to inform the Security Response Committee (SRC) about the vulnerability so they
may start the patch, release, and communication process.

If possible the TC will ask the person making the public report if the issue can
be handled via a private disclosure process. If the reporter denies the request,
the TC will move swiftly with the fix and release process. In extreme cases you
can ask GitHub to delete the issue but this generally isn't necessary and is
unlikely to make a public disclosure less damaging.

## Patch, Release, and Public Communication

For each vulnerability a member of the TC will volunteer to lead coordination
with the relevant repo owners, and is responsible for sending disclosure
emails to the rest of the community. This TC member will be referred to as the Fix Lead.

The role of Fix Lead should rotate round-robin across the TC.

All of the timelines below are suggestions and assume a Private Disclosure.
The Fix Lead drives the schedule using their best judgment based on severity,
development time, and release manager feedback. If the Fix Lead is dealing with
a Public Disclosure all timelines become ASAP. If the fix relies on another
upstream project's disclosure timeline, that will adjust the process as well.
We will work with the upstream project to fit their timeline and best protect
our users.

### Fix Team Organization

The Fix Team is made up of the Fix Team Lead and the relevant repo maintainers / contributors.

### Fix Development Process

These steps should be completed within the 1-7 days of Disclosure.

- The Fix Lead and the Fix Team will create a [CVSS](https://www.first.org/cvss/specification-document) score using the [CVSS Calculator](https://www.first.org/cvss/calculator/3.0). The Fix Lead makes the final call on the calculated risk; it is better to move quickly than make the perfect assessment.
- The Fix Lead will request a CVE from GitHub.
- The Fix Team will notify the Fix Lead that work on the fix branch is complete once there are LGTMs on all commits in the private repo.

### Fix Disclosure Process

OTel relies on GitHub tooling to notify the affected repositories and publish a security advisory. GitHub will publish the CVE to the CVE List, broadcast the Security Advisory via the GitHub Advisory Database, and send security alerts to all repositores that use the package and have alerts on.

#### Fix Release Day

The Fix Team as repo owners will release an updated version after confirming approval with the Fix Lead.

## Retrospective

### OTel Retrospective Policy

?
The assigned TC member coordinates the retrospective?

### Kubernetes Policy

These steps should be completed 1-3 days after the Release Date. The retrospective process should be blameless.

The Fix Lead will send a retrospective of the process to kubernetes-dev@googlegroups.com including details on everyone involved, the timeline of the process, links to relevant PRs that introduced the issue, if relevant, and any critiques of the response and release process.
The Release Managers and Fix Team are also encouraged to send their own feedback on the process to kubernetes-dev@googlegroups.com. Honest critique is the only way we are going to get good at this as a community.

## Severity

The Technical Committee evaluates vulnerability severity on a case-by-case basis, guided by CVSS 3.1.
