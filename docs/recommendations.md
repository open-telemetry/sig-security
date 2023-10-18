# Recommendations

This document lists recommendations from the Security SIG for
the consideration of OpenTelemetry SIGs.

## CodeQL Scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis
of the code in various repositories. The recommendation is to run CodeQL on every
pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

## Allstar was proposed as a way to achieve consistency across the repositories in the org with regards to security policy. This issue is to:
  ### CodeQL enabled via GitHub Actions:
  "Allstar" can help automate CodeQL analysis as part of your GitHub Actions workflow. You would need to configure "Allstar" to include CodeQL checks in your         repository's workflow file.

  ### Static code analysis: govulncheck enabled on every build:
  "Allstar" may not directly provide Go vulnerability scanning like govulncheck. You may need to continue using govulncheck separately or look for alternative        GitHub Actions or tools to cover this specific need.

  ### Repository security settings:
  Security Policy, Security advisories, Private vulnerability reporting, and Dependabot alerts are typically GitHub settings that you can enable at the repository   level through the GitHub UI. "Allstar" may not directly configure these settings, but it can help monitor and report on their status.
  ### Code scanning alerts: 
  "Allstar" can integrate with GitHub's code scanning feature and provide alerts. However, the configuration of code scanning workflows and the handling of alerts    may require manual setup in each repository.

## let's propose steps to enable "Allstar" across your organization and open issues in the appropriate repositories:

  ### Enable "Allstar" Across the Organization:
    First, determine if "Allstar" is already set up in your organization. If not, you can set it up as a GitHub App with appropriate permissions.
    Configure "Allstar" to integrate with the organization's repositories.

  ### Configure "Allstar" for Security Checks:
      Create or configure "Allstar" checks that align with your organization's security policies.
      Ensure that "Allstar" runs as part of your GitHub Actions workflows for code scanning and security checks.

  ### Open Issues in Repositories:
      Use "Allstar" to scan and identify repositories that do not meet the security checklist requirements.
      For repositories that need manual configuration, open issues with detailed instructions on what needs to be done to align with the security checklist items.

  ### Documentation in Security SIG Repository:
        Document the usage of "Allstar" in your organization's Security SIG repository.
        Include instructions on how to configure "Allstar" for security checks and provide guidance on interpreting its reports.
