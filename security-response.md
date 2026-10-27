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

## Security model

This model guides vulnerability acceptance, severity assessment, and automated
security analysis across OpenTelemetry.

Repositories may document component-specific trust assumptions and scoped
exclusions in `THREAT_MODEL.md`. Exclusions should explain their rationale.

### Assets and deployment context

This model covers risks to telemetry, credentials, and the applications, hosts,
and infrastructure running OpenTelemetry. It also covers build and release
workflows and the artifacts they produce.

Identify the affected component:

- **APIs, SDKs, and instrumentation** often run within an application's process
  and can affect its data and availability, even without a listening port.
  Identify any instrumentation running outside that process.
- **Collectors, receivers, exporters, and extensions** process telemetry and
  communicate with peers. Their exposed endpoints, local access, and privileges
  depend on the enabled components and configuration.
- **Operators, agents, and deployment tooling** may have access to workloads,
  host resources, or orchestration APIs. Assess their actual permissions and
  authorization boundaries.
- **Build, test, and release tooling** can affect credentials and distributed
  artifacts. Code that is absent from production can still be security relevant
  when it processes untrusted contributions in a privileged workflow.

### Inputs and trust boundaries

For each entry point, identify who controls the input and what authority that
actor has. Follow the input through intermediaries to the operation that could
cause harm.

| Input or surface | Expected control and boundary to assess |
| --- | --- |
| Incoming propagation headers, telemetry attributes, log bodies, and resource data | External callers or telemetry producers may control these values. Treat them as potentially untrusted when parsing, processing, or forwarding. |
| Receiver and extension endpoints, including metrics and diagnostic endpoints | Identify who can connect, what authentication and authorization apply, and which data or operations are exposed. |
| Exporter responses, scrape targets, redirects, and other network peers | A configured destination or authenticated peer can return malicious data. Identify which responses and destinations the attacker can influence. |
| Configuration files, environment variables, endpoint URLs, certificates, and local files | Normally controlled by the operator. Identify the authority intentionally granted and whether a less trusted actor can modify or bypass it. |
| Instrumentation code, callbacks, plugins, and custom components | Normally controlled by the developer or operator and executed with the host's privileges. Identify any isolation or restrictions the component promises. |
| Contributions, dependencies, build inputs, and release workflows | Identify where untrusted content can reach execution, secrets, signing, or publication privileges. |

Authentication of a transport peer does not establish the provenance of every
field it forwards. For example, an authenticated exporter can forward baggage
originally supplied by an unauthenticated application client.

### Assumptions and responsibilities

- Trace IDs, span IDs, baggage, and other caller-supplied telemetry are not
  authentication or authorization credentials. Accepting remote context or
  caller-selected attributes is expected behavior; a report must identify an
  additional security consequence, such as bypassing enforced tenant isolation.
  See [Baggage security
  considerations](https://opentelemetry.io/docs/concepts/signals/baggage/#baggage-security-considerations).
- Telemetry can contain sensitive information. Users are responsible for
  selecting data to collect and applying appropriate protection, as described in
  [Handling sensitive
  data](https://opentelemetry.io/docs/security/handling-sensitive-data/).
  Unexpected collection of credentials or failure of a configured redaction
  control still requires security assessment.
- Operators are responsible for protecting configuration, credentials, and
  telemetry endpoints and limiting exposure and resource consumption. Use
  encryption, authentication, network restrictions, and appropriate permissions.
  See [Collector configuration best
  practices](https://opentelemetry.io/docs/security/config-best-practices/).
  A defect that bypasses these configured protections is a potential
  vulnerability.
- A capability intentionally granted to a configuration author or custom
  component is not, by itself, a vulnerability. For example, selecting an
  exporter destination is expected operator authority. Untrusted telemetry
  overriding that destination, leaking credentials on a redirect, or bypassing
  a destination restriction requires assessment.
- Markup or query syntax in telemetry alone does not establish injection;
  identify a reachable unsafe interpreter.
- Supported nondefault configurations can be affected by vulnerabilities.
  Record the required settings and whether they are defaults; configuration
  requirements alone do not establish or exclude a vulnerability.

### Availability policy

Denial of service and resource exhaustion, including through unbounded
telemetry, can be security vulnerabilities. Assess reports involving default
settings, documented behavior, and authenticated clients. Record required
authentication and configuration. Untrusted application input can reach an SDK
without passing through a telemetry endpoint's authentication.

A missing resource limit, high-volume valid telemetry exceeding deployment
capacity, or an opportunity to reduce resource use or improve performance does
not, by itself, establish a vulnerability. A report must identify a reachable
processing, retention, or resource-isolation weakness and demonstrate how
attacker-controlled input exploits it to deny service. Examples include retaining
records beyond their intended lifetime or bypassing a configured resource
budget. Valid input and linear resource growth do not, by themselves, exclude
such weaknesses.

For each availability report:

- Identify the attacker-controlled input and reachable processing or retention
  path, including any missing or ineffective resource bounds.
- Record input size, volume, rate, and concurrency, resulting CPU, memory, disk,
  or network cost, and how long resources remain occupied. Identify amplification
  or unbounded accumulation where present.
- Describe the consequence and recovery: bounded telemetry drops, a stalled
  pipeline, or failure of the Collector, host application, or another service;
  affected tenants; and whether recovery requires a restart or operator action.
- Assess available protections in the affected version and configuration,
  including whether limits apply before expensive work and whether an attacker
  can bypass them. Consider the security policies of compatible projects
  (e.g. Prometheus), documenting how they apply to the affected component.

Operator responsibilities do not exempt implementation defects or unsafe
defaults from assessment.

### Vulnerability assessment

Acknowledgment confirms receipt, not acceptance or severity. Request missing
information as needed.

For each report, establish:

1. **Affected component and configuration:** repository, package or artifact,
   released versions, relevant features, deployment, and required settings.
1. **Attacker capability:** the exact input under attacker control, access and
   privileges required, and any cooperation needed from another party.
1. **Reachable behavior:** the entry point and code path from that input to the
   affected operation, including dependency calls and applicable checks.
1. **Security consequence:** the missing or ineffective protection and concrete
   confidentiality, integrity, or availability impact. Identify whose data or
   resources are affected and any tenant or privilege boundary crossed.
1. **Evidence and mitigations:** a reproducer or code-based explanation,
   supporting source locations, relevant limits and protections, and why they
   do not prevent the impact. State assumptions and unresolved questions.

Automated findings should provide this information, cite code at the scanned
revision, and distinguish verified facts from assumptions.

Record whether the report is a confirmed vulnerability, needs more evidence,
is a duplicate, or is a bug, hardening opportunity, or out-of-scope issue, with
the reason. Missing evidence is uncertainty, not a low severity rating. A
dependency advisory alone does not establish exploitability through an OTel
component; apply the reachability and impact criteria in [CVE
Management](#cve-management).

### Severity and prioritization

Use the [CVSS v4.0
specification](https://www.first.org/cvss/v4.0/specification-document) and
[calculator](https://www.first.org/cvss/calculator/4.0). For accepted
vulnerabilities, record the Base score (`CVSS-B`), full `CVSS:4.0` vector, and
metric rationale. Label additional scores that include Threat or Environmental
metrics as `CVSS-BT`, `CVSS-BE`, or `CVSS-BTE`, as applicable.

The CVSS v4.0 qualitative bands are:

| Rating | Score |
| --- | --- |
| Critical | 9.0 - 10.0 |
| High | 7.0 - 8.9 |
| Medium | 4.0 - 6.9 |
| Low | 0.1 - 3.9 |
| None | 0.0 |

Select metrics from the attack path and impact, documenting reasonable
worst-case usage assumptions for general-purpose libraries. A library flaw
reachable through network input is not necessarily a local attack. Account for
required privileges (`PR`) and user interaction (`UI`). Assess Attack
Requirements (`AT`) separately from Attack Complexity (`AC`); a required
nondefault configuration alone does not justify `AT:P`. Assess dependencies
through their use in OTel rather than copying their scores.

Define the vulnerable system being scored. Assess confidentiality, integrity,
and availability within it (`VC`, `VI`, `VA`) and in any subsequent systems
(`SC`, `SI`, `SA`). An SDK and its host application can form one vulnerable
system; host application impact is not automatically subsequent-system impact.
Distinguish exposure of telemetry from exposure of credentials or unrelated
application data.

For availability findings, distinguish expected bounded telemetry loss from
loss of a telemetry service or failure of the instrumented application. Record
duration, recoverability, and affected users; authentication affects the attack
prerequisites and does not alone justify an availability impact of None
(`VA:N` or `SA:N`).

Keep confidence in the evidence and response priority separate from severity.
Record active exploitation, public disclosure, affected deployments, and
available mitigations when prioritizing the response. Use Exploit Maturity
(`E`) for Threat assessments and Environmental metrics for deployment-specific
requirements and controls. Supplemental metrics such as Recovery (`R`) and
Provider Urgency (`U`) add context without changing the numeric score.

## Reporting Process - For Vulnerability Reporters

### Reporting Methods

In order for the vulnerability reports to reach maintainers as soon as possible,
the preferred way is to use the `Report a vulnerability` button on the
`Security` tab in the respective GitHub repository. It creates a private
communication channel between the reporter and the maintainers.

If you are unable to or have strong reasons not to use the GitHub reporting
workflow, please reach out to
[security@opentelemetry.io](mailto:security@opentelemetry.io)
and we will provide instruction on how to report the vulnerability.

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

## Vulnerability Management - For Maintainers

Maintainers of OTel projects have the role of being the primary responders
and managers of vulnerabilities reported in their respective repos.

Maintainers should familiarize themselves with the above guidance for Reporters
and encourage any potential Reporters to follow that guidance.

### Permissions Model

By default, only GitHub Org Owners, org-wide Security Managers, and Repository
Admins have access to a repository's Security Advisories. Repository
Maintainers do not automatically have access. Security SIG Maintainers have
been granted the org-wide Security Manager role, which gives them full access
to Advisories across OTel repositories.

Automation in the OpenTelemetry [Zapier
account](https://github.com/open-telemetry/community/blob/main/assets.md#zapier-account)
adds Repository Maintainers as Collaborators on each Security Advisory so
they can view the advisory and participate in fixing it.

Collaborator access is sufficient for most day-to-day work on an advisory,
including viewing details, commenting, editing the advisory, and contributing
fixes in the temporary private fork. However, some actions require Repository
Admin permissions, including:

- Publishing the advisory
- Requesting a CVE (via the "Request CVE" button on the advisory form)
- Creating the temporary private fork
- Merging pull requests in the temporary private fork

Please follow [Request Repository Admin
Permissions](https://github.com/open-telemetry/community/blob/main/guides/maintainer/github-admin-processes.md#request-repository-admin-permissions)
if you are a repository maintainer and need admin permissions.

### GitHub Tooling

Vulnerabilities reported via the `Report a vulnerability` button will appear
for Maintainers as a Security Advisory under the `Security` tab under
the `Advisories` side bar option.

Maintainers can also create their own draft Security Advisory here using the
`New draft security advisory` button if they discover an unreported issue or
need to report for someone who is unwilling or unable to use the
`Report a vulnerability` button.

Note that access to Security Advisories is limited; see the [Permissions
Model](#permissions-model) section above for details on who has access by
default and which actions require Repository Admin permissions.

For more detailed GitHub documentation on this feature, see
[this link](https://docs.github.com/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories)

### Incident Response

Vulnerability reports should be acknowledged by Maintainers within 3 working
days. This acknowledgment should include a brief confirmation that the report
has been received and that Maintainers are evaluating the issue.

Use the [Security model](#security-model) to evaluate acceptance and severity.

When processing a vulnerability report, Maintainers should:

1. Acknowledge receipt of the report within 3 working days
1. Invite Collaborators as needed
1. Verify if the reported issue is actually a vulnerability
1. Assess the severity and impact of the vulnerability
1. Determine if the vulnerability is already publicly known or disclosed
1. Negotiate an embargo period, if needed
1. Request a CVE, if needed _(Admin)_
1. Create a Temporary Private Fork, if needed _(Admin)_
1. Ensure work is progressing on a resolution in accordance with severity and
  embargo timeline
1. After a release containing the fix is published, publish the Advisory
  _(Admin)_

Steps marked _(Admin)_ require Repository Admin permissions; see the
[Permissions Model](#permissions-model) section.

### Managing Collaborators

When working on security advisories in GitHub:

1. Repository Maintainers are typically added as Collaborators automatically
   (see the [Permissions Model](#permissions-model) section). To add
   additional Collaborators beyond the default Maintainer set, use the
   "Add users or teams" edit box in the Collaborators section of the
   GitHub Security Advisory interface.
2. Try to keep the number of Collaborators small to limit the exposure of the
   vulnerability details before a fix is available.
3. Only add Collaborators who are necessary for investigating or fixing the
   issue.
4. Consider adding Collaborators who:
   - Understand the affected code
   - Can assist with implementing or reviewing fixes
   - Have expertise in the specific security domain

### Using Temporary Private Forks

GitHub provides temporary private forks as a secure environment to fix
vulnerabilities without exposing them to the public. These forks allow you to
collaborate with others on fixing security issues before making the fixes
public.

#### Creating a Temporary Private Fork

1. Navigate to the main page of the repository
2. Click on the "Security" tab
3. In the left sidebar under "Reporting", click "Advisories"
4. Select the security advisory you're working on
5. Scroll to the bottom of the advisory form and click
  "Start a temporary private fork"

Creating the temporary private fork requires Repository Admin permissions;
see the [Permissions Model](#permissions-model) section above.

The temporary private fork will be created with a name in the format:
`repo-ghsa-xxxx-xxxx-xxxx`, where `repo` is your repository name (truncated to
80 characters if needed) and `xxxx-xxxx-xxxx` is the unique identifier of the
security advisory.

#### Adding Changes to the Fork

You can make changes to the private fork either on GitHub or locally:

- **On GitHub**: Navigate to the temporary private fork from the advisory page,
  create a new branch, and edit the files as needed

- **Locally**: Clone the temporary private fork, create a branch, make your
  changes, and push them back to the fork

#### Creating Pull Requests and Merging Changes

1. From the security advisory page, click "Compare & pull request" to create a
   pull request for your changes

2. When all necessary changes are ready, scroll to the bottom of the advisory
   page and click "Merge pull request(s)" to merge all open pull requests in the
   temporary private fork

Merging from a temporary private fork requires extra care because the
repository's standard branch protections and rulesets typically block the
merge. The merge is performed by GitHub against the upstream repository (not
the fork), so the upstream branch protections apply. However, no CLA check or
CI runs are attached to the PR, since neither runs in a private fork. As a
result, the person performing the merge usually needs to temporarily relax
the upstream protections, perform the merge, and then restore them.

Before relaxing protections, make sure the fix has already been reviewed in
the temporary private fork, since the usual review, CI, and CLA gates will
all be bypassed at merge time.

The exact steps vary per repository, but the typical pattern is to
temporarily:

- Add yourself as a bypasser on the repository's main ruleset
- Add yourself as a bypasser on the EasyCLA ruleset
- Disable "Do not allow bypassing the above settings" on the main classic
  branch protection rule (if the repository still uses one)

After the merge completes, immediately revert each of these changes.

Important notes about temporary private forks:

- CI/CD integrations do not run in temporary private forks to maintain security
- You cannot merge individual pull requests; all open PRs are merged together
- Status checks will not run on PRs in temporary private forks
- After merging changes and releasing a version that contains the fix, you can
  publish the advisory to alert the community

For more details, see the [GitHub documentation on private forks](https://docs.github.com/code-security/security-advisories/working-with-repository-security-advisories/collaborating-in-a-temporary-private-fork-to-resolve-a-repository-security-vulnerability).

### TC Point of Contact

The TC maintains a weekly on-call rotation. When a new security advisory is
opened, the on-call TC member for that week serves as the primary TC point of
contact (POC) for the advisory. They are responsible for self-assigning to the
advisory and helping to progress it to conclusion, even after their rotation ends.

If the assigned TC POC is unavailable and TC assistance is needed, maintainers
should reach out to the current on-call TC member instead. The on-call schedule
can be found in the [TC on-call schedule](https://docs.google.com/spreadsheets/d/1GuhkiK4MjzcFij_KQojiE_2yGsFvPV6wC7fqHULGm98/edit?gid=0#gid=0).

### Getting Assistance

If Maintainers need assistance with how to handle a security vulnerability:

1. For general guidance of a non sensitive nature, Contact the Security SIG
  through the [#otel-sig-security](https://cloud-native.slack.com/archives/C05A85QC281)
  channel in the CNCF Slack workspace.
  Do not expose sensitive information in this channel as it isn't a secure
  communication mechanism.

2. For sensitive guidance specific to an Advisory, reach out to [Security SIG
  Maintainers](https://github.com/open-telemetry/sig-security#maintainers) as
  they have access to all Advisories and can comment directly in
  them. For complex or high impact issues, the Security SIG may also involve
  the TC and/or GC.

3. For TC assistance specific to an Advisory, contact the assigned TC POC
  directly via the advisory. If the assigned TC POC is unavailable, reach out
  to the current on-call TC member instead; see the
  [TC Point of Contact](#tc-point-of-contact) section for the schedule.

### CVE Management

#### When to Request a CVE

When determining whether to request a CVE identifier, Maintainers should
consider the type of OTel deliverables affected (executable vs. library) and the
source of the vulnerability (direct vs. dependency):

##### For Executables (Collector, Tools, etc.)

1. **Direct Vulnerabilities**: Always request a CVE when a vulnerability exists
   in OTel's own code that could expose users to security risks.

2. **Dependency Vulnerabilities**: Request a CVE if these are all true:
   - The executable uses the vulnerable part of the dependency
   - The vulnerability can be exploited through the executable's usage patterns
   - The vulnerability creates a security impact for users of the executable

   Do not request a CVE if the dependency vulnerability cannot be triggered
   through the executable's supported entry points, even with
   attacker-controlled input.

   Note that the vulnerability impact for the OTel executable may be different
   than for the dependency that caused it, depending on how it is used.  Do not
   assume that the OTel CVE must have the same score as the dependency's CVE.

##### For Libraries

1. **Direct Vulnerabilities**: Request a CVE if the vulnerability exists in
   OTel's own library code.

2. **Dependency References**: Request a CVE if these are all true:
   - The vulnerable dependency is transitively included in the runtime
   environment, even when users of the OTel library do not explicitly include
   the vulnerable dependency themselves (this is likely true in most cases
   for library code)
   - The library uses the vulnerable part of the dependency
   - The vulnerability can be exploited through the library's usage patterns
   - The vulnerability creates a security impact for users of the library

   Note that the vulnerability impact for the OTel library may be different
   than for the dependency that caused it, depending on how it is used.  Do not
   assume that the OTel CVE must have the same score as the dependency's CVE.

#### General criteria for all CVE requests

1. The vulnerability must affect released versions of OTel
2. The vulnerability must have security impact (confidentiality, integrity, or
   availability)
3. The vulnerability must not already have a CVE assigned to the specific OTel
   component

#### How to Request a CVE

GitHub provides a streamlined process for requesting CVE identifiers:

1. Within the Security Advisory interface, scroll to the bottom of the form
2. Click the "Request CVE" button
3. GitHub will review the request (typically within 72 hours)
4. Once approved, GitHub will assign a CVE ID to the advisory

If you already have a CVE ID from another CVE Numbering Authority (CNA), you can
add this to the Security Advisory form instead of requesting a new one through
GitHub.

For more information on requesting CVEs through GitHub, see the
[GitHub documentation on requesting CVE identification numbers](https://docs.github.com/code-security/security-advisories/working-with-repository-security-advisories/publishing-a-repository-security-advisory#requesting-a-cve-identification-number-optional).

### FAQ for Maintainers

#### Q: How do I determine the severity of a vulnerability?

**A:** Follow [Severity and prioritization](#severity-and-prioritization) for
CVSS v4.0 scoring and the required score, vector, and metric rationale.

#### Q: Should I fix the vulnerability before publishing the advisory?

**A:** Whenever possible, include a fix version in the advisory before
publishing. This allows users to update to a secure version immediately upon
full disclosure. For vulnerabilities that are not publicly known, this is the
entire point of embargo periods before disclosure.

#### Q: When should I involve the Security SIG or Technical Committee?

**A:** Consider involving the Security SIG for critical or high-severity issues
that can't be fixed promptly, vulnerabilities affecting multiple repositories,
or if you need guidance on handling a security related issue. For TC
involvement, contact the assigned [TC Point of Contact](#tc-point-of-contact).
If in doubt, feel free to reach out.  Just be careful to avoid disclosing
non-public vulnerability information in non-secure communication channels.

#### Q: How do I handle embargo periods?

**A:** For non-public vulnerabilities, coordinate with the reporter to determine
if they have a need for public disclosure, for example an upcoming security
conference at which they want to present. Politely negotiate a timeline for
disclosure as best you can, but understand that Reporters are under no
obligation to OTel.  In general, ask that the Reporter not disclose the
vulnerability beyond the conversation in the Advisory until a fix is made and
the Advisory has been published.

#### Q: How do I handle a vulnerability that's already public?

**A:** For publicly known vulnerabilities, prioritize creating an advisory and
releasing a fix as quickly as possible. Note in the advisory that the
vulnerability is already publicly known. If there is a known work-around or
mitigation that users can implement, consider publishing an advisory with the
work-around info until a fix can be made. This option should be balanced with
how useful the work-around would be to users vs further advertising the
vulnerability. If a vulnerability is so well known that multiple reports are
being made, it can be advantageous to publish to avoid the reporting noise.

#### Q: What do I do if a private vulnerability becomes public?

**A:** Similar to a reported vulnerability that was already publicly known:
Continue your efforts to fix the vulnerability with urgency appropriate to its
severity.  Document the change in status in the Advisory so that the
Collaborators and Reporter are aware that the vulnerability is openly known.
However, continue to avoid spreading information about the
vulnerability unless it significantly helps with the speed of the fix or
users need to be informed of a work-around or mitigation steps.

#### Q: What if we can't fix the vulnerability quickly?

**A:** If a fix will take a long time, particularly if the vulnerability is high
or critical severity, you should bring this up with the Security SIG and/or the
assigned TC POC (see [TC Point of Contact](#tc-point-of-contact)) to determine
if there is any public messaging or other actions that need to be taken.
