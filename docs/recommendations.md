# Recommendations

This document lists recommendations from the Security SIG for
the consideration of OpenTelemetry SIGs.

## CodeQL Scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis
of the code in various repositories. The recommendation is to run CodeQL on every
pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

## Binding to Network Interfaces
Always bind to localhost rather than to 0.0.0.0 or any interface, unless there is a specific need to do otherwise. Binding to localhost reduces the attack surface of your application by making it only accessible to devices on the same machine.
Binding to 0.0.0.0 or "all" interfaces can make your application respond on all current and future network interfaces.

Issue: ([#19](https://github.com/open-telemetry/sig-security/issues/19#issue-1926445623))

## Container images

### Use the smallest image possible
While the size of an image doesn't matter for the runtime, we are responsible for everything that is in the image. If you are delivering a statically linked binary, you can probably build a `scratch` image for production purposes. It might be a good idea to provide a second set of images for debugging purposes, such as ones including a shell and networking utilities.

If you need to include files in the image, such as root certificates, use the builder pattern to obtain the files and copy only those into the final image. Example:

```Dockerfile
FROM alpine:3.20 as certificates
RUN apk --no-cache add ca-certificates

FROM scratch
COPY --from=certificates /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY mybinary mybinary
```

### Use a non-privileged user
Under some circumstances, your image might be executed as a privileged user by default. In others, like a hardened Kubernetes distribution, your container is forced to run using a non-privileged account and bugs might appear as the image wasn't built with that in mind. It's recommended to set a high user ID when building the image, to ensure the process always runs as a non-privileged user. This will not only make it more secure by default but will help you uncover issues before they affect security-conscious users.

Here's how to do it:

```Dockerfile
USER 65532:65532
```

### Keep your images up to date
Use tools like Renovate or Dependabot to achieve that.

#### Renovate
[Here's an example](https://github.com/jpkrohling/otel-sig-security-example-go/pull/17) of a PR created by Renovate on a repository using its default configuration. 

If you are interested in using Renovate, open an issue requesting the TC to enable it to your repository, [like this](https://github.com/open-telemetry/community/issues/2090). You should then receive a PR from Renovate doing the onboarding, [like this](https://github.com/open-telemetry/opentelemetry-go/pull/5309).

#### Dependabot
For directories containing a Dockerfile, add the following to your `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly
```

And [here's one](https://github.com/open-telemetry/opentelemetry-operator/pull/2990) from Dependabot.

