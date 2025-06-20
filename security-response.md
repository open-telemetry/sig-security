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

## Vulnerability Management - For Maintainers

Maintainers of OTel projects have the role of being the primary responders
and managers of vulnerabilities reported in their respective repos.

Maintainers should familiarize themselves with the above guidance for Reporters
and encourage any potential Reporters to follow that guidance.

### GitHub Tooling

Vulnerabilities reported via the `Report a vulnerability` button will appear
for Maintainers as a Security Advisory under the `Security` tab under
the `Advisories` side bar option.

Maintainers can also create their own draft Security Advisory here using the
`New draft security advisory` button if they discover an unreported issue or
need to report for someone who is unwilling or unable to use the
`Report a vulnerability` button.

Note that for a specific OTel repo, only that repo's Maintainers and Security
SIG Maintainers (which have been granted the Security Manager role) will have
access to the full Advisories data and functionality.

For more detailed GitHub documentation on this feature, see
[this link](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories)

### Incident Response

Vulnerability reports should be acknowledged by Maintainers within 3 working
days. This acknowledgment should include a brief confirmation that the report
has been received and that Maintainers are evaluating the issue.

When processing a vulnerability report, Maintainers should:

1. Acknowledge receipt of the report within 3 working days
1. Invite Collaborators as needed
1. Verify if the reported issue is actually a vulnerability
1. Assess the severity and impact of the vulnerability
1. Determine if the vulnerability is already publicly known or disclosed
1. Negotiate an embargo period, if needed
1. Request a CVE, if needed
1. Create a Temporary Private Fork, if needed
1. Ensure work is progressing on a resolution in accordance with severity and
  embargo timeline
1. When a fix is ready, Publish the Advisory

### Managing Collaborators

When working on security advisories in GitHub:

1. Maintainers can add Collaborators to assist with investigation and fixing by
   using the "Add users or teams" edit box in the Collaborators section in the
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

Important notes about temporary private forks:

- CI/CD integrations do not run in temporary private forks to maintain security
- You cannot merge individual pull requests; all open PRs are merged together
- Status checks will not run on PRs in temporary private forks
- After merging changes, you can publish the advisory to alert the community

For more details, see the [GitHub documentation on private forks](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/collaborating-in-a-temporary-private-fork-to-resolve-a-repository-security-vulnerability).

### Getting Assistance

If Maintainers need assistance with how to handle a security vulnerability:

1. For general guidance of a non sensitive nature, Contact the Security SIG
  through the [#otel-sig-security](https://cloud-native.slack.com/archives/C05A85QC281) channel in the CNCF Slack workspace.
  Do not expose sensitive information in this channel as it isn't a secure
  communication mechanism.

2. For sensitive guidance specific to an Advisory, reach out to [Security SIG
  Maintainers](https://github.com/open-telemetry/sig-security#maintainers) as they have access to all Advisories and can comment directly in
  them. For complex or high impact issues, the Security SIG may also involve
  the TC and/or GC.

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

   Do not request a CVE if the vulnerability in the dependency cannot be
   triggered through normal usage of the executable.

   Note that the vulnerability impact for the OTel executable may be different
   than for the dependency that caused it, depending on how it is used.  Do not
   assume that the OTel CVE must have the same score as the dependency's CVE.

##### For Libraries

1. **Direct Vulnerabilities**: Request a CVE if the vulnerability exists in
   OTel's own library code.

2. **Dependency References**: Generally, do not request a CVE when:
   - The library only references a vulnerable dependency
   - The dependency is not bundled with the OTel deliverable
   - The vulnerability only affects consumers who explicitly import both the
     OTel library and the vulnerable dependency

General criteria for all CVE requests:

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
[GitHub documentation on requesting CVE identification numbers](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/publishing-a-repository-security-advisory#requesting-a-cve-identification-number-optional).

### FAQ for Maintainers

#### Q: How do I determine the severity of a vulnerability?

**A:** Use the Common Vulnerability Scoring System (CVSS) to assess
severity. GitHub provides a CVSS calculator in the Security Advisory interface,
or you can use the [CVSS Calculator](https://www.first.org/cvss/calculator/3.1).

#### Q: Should I fix the vulnerability before publishing the advisory?

**A:** Whenever possible, include a fix version in the advisory before
publishing. This allows users to update to a secure version immediately upon
full disclosure. For vulnerabilities that are not publicly known, this is the
entire point of embargo periods before disclosure.

#### Q: When should I involve the Security SIG or Technical Committee?

**A:** Consider involving them for critical or high-severity issues that can't
be fixed promptly, vulnerabilities affecting multiple repositories, or if you
need guidance on handling a security related issue.  If in doubt, feel free
to reach out.  Just be careful to avoid disclosing non-public vulnerability
information in non-secure communication channels.

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
or critical severity, you should bring this up with the Security SIG and/or TC
to determine if there is any public messaging or other actions that need to be
taken.
