# Recommendations

This document lists recommendations from the Security SIG for the consideration
of OpenTelemetry SIGs.

## CodeQL Scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis
of the code in various repositories. The recommendation is to run CodeQL on
every pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

## Binding to Network Interfaces

Always bind to localhost rather than to 0.0.0.0 or any interface, unless there
is a specific need to do otherwise. Binding to localhost reduces the attack
surface of your application by making it only accessible to devices on the same
machine. Binding to 0.0.0.0 or "all" interfaces can make your application
respond on all current and future network interfaces.

Issue:
([#19](https://github.com/open-telemetry/sig-security/issues/19#issue-1926445623))

## Container images

### Use the smallest image possible

While the size of an image doesn't matter for the runtime, we are responsible
for everything that is in the image. If you are delivering a statically linked
binary, you can probably build a `scratch` image for production purposes. It
might be a good idea to provide a second set of images for debugging purposes,
such as ones including a shell and networking utilities.

If you need to include files in the image, such as root certificates, use the
builder pattern to obtain the files and copy only those into the final image.
Example:

```Dockerfile
FROM alpine:3.20 as certificates
RUN apk --no-cache add ca-certificates

FROM scratch
COPY --from=certificates /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY mybinary mybinary
```

### Use a non-privileged user

Under some circumstances, your image might be executed as a privileged user by
default. In others, like a hardened Kubernetes distribution, your container is
forced to run using a non-privileged account and bugs might appear as the image
wasn't built with that in mind. It's recommended to set a high user ID when
building the image, to ensure the process always runs as a non-privileged user.
This will not only make it more secure by default but will help you uncover
issues before they affect security-conscious users.

Here's how to do it:

```Dockerfile
USER 65532:65532
```

### Keep your images up to date

Use tools like Renovate or Dependabot to achieve that.

#### Renovate

[Here's an
example](https://github.com/jpkrohling/otel-sig-security-example-go/pull/17) of
a PR created by Renovate on a repository using its default configuration.

If you are interested in using Renovate, open an issue requesting the TC to
enable it to your repository, [like
this](https://github.com/open-telemetry/community/issues/2090). You should then
receive a PR from Renovate doing the onboarding, [like
this](https://github.com/open-telemetry/opentelemetry-go/pull/5309).

#### Dependabot

For directories containing a Dockerfile, add the following to your
`.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly
```

And [here's
one](https://github.com/open-telemetry/opentelemetry-operator/pull/2990) from
Dependabot.

## Vulnerability Management

There are several aspects of vulnerability management that the Security SIG
recommends to the OpenTelemetry project maintainers:

- The maintainers of an OpenTelemetry project should establish a clear
  accountability for security issues, including identifying the direct
  responsible individual for security issues at a certain time, for
  example, via a duty rotation. This should be
  documented in the main README.md file of the project.
- The direct responsible individual should monitor the [repository security
  advisories](https://docs.github.com/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories),
  make sure security advisories are triaged in a timely manner, and there is
  active engagement and communication on the issue. Refer to the [incident
  response guideline](../security-response.md#incident-response) for more
  details.
- Regularly scan your code and dependencies for **deprecations** and
  **vulnerabilities** using tools. This should include but not be limited to:
  - CI/CD tooling - for example, some GitHub Actions might be deprecated or no
    longer maintained, certain GitHub Actions might have known vulnerabilities,
    a compiler might have a known vulnerability, etc.
  - CI/CD environment - for example, the CI/CD job might be running on a
    deprecated or vulnerable version of the operating system.
  - container image dependencies - for example, the base image used in
    Dockerfiles or image referenced by Helm charts might have known
    vulnerabilities, or the image might be using a deprecated version of a
    library.
  - repository configurations - for example, a hotfix branch might not have the
    proper branch protection rules, or the repository might not have the proper
    security settings enabled.
  - package dependencies - for example, a package might have a known
    vulnerability, or a package might be using a deprecated version of a
    library.
- All security vulnerabilities that are found - whether from the user reported
  repository security advisories or through automated scanning - should be
  handled in a timely manner based on the severity level. In case of a real
  vulnerability that doesn't have a fix available, the maintainers should
  evaluate the impact and likelihood of exploitation and take appropriate
  action, such as applying workarounds or communicating with affected users. In
  the worst case, this can be a potential end-of-life announcement of the
  affected component or project.

Here is a check list for the maintainers:

- [ ] Identify the direct responsible individual for security issues and
  document it in the main README.md file of the project.
- [ ] Monitor the GitHub repository security advisories and triage security
  issues in a timely manner.
- [ ] Daily scan CI/CD tooling for deprecations and vulnerabilities.
- [ ] Daily scan CI/CD environment for deprecations and vulnerabilities.
- [ ] Daily scan container image dependencies for deprecations and
  vulnerabilities.
- [ ] Daily scan repository configurations for deprecations and vulnerabilities.
- [ ] Daily scan package dependencies for deprecations and vulnerabilities.
- [ ] False positives are documented (e.g., by commenting on the security
  advisory, by providing the dismissal reason to a code scanning alert) and
  dismissed.
- [ ] Critical and high severity vulnerabilities are patched within 2 weeks of
  discovery.
- [ ] Medium and low severity vulnerabilities are patched within 4 weeks of
  discovery.
- [ ] For vulnerabilities that cannot be patched in a timely manner (for
  example, the component is depending on an outdated library, and there is no
  replacement), the maintainers should evaluate the impact and likelihood of
  exploitation and take appropriate action, such as applying workarounds or
  communicating with affected users.
