# Recommendations

This document lists recommendations from the Security SIG for the consideration of OpenTelemetry SIGs.

## CodeQL Scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis of the code in various repositories.
The recommendation is to run CodeQL on every pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

Note: we also have access to [Snyk](https://snyk.io) and you can add it to your repositories.

## Binding to Network Interfaces

Always bind to localhost rather than to 0.0.0.0 or any interface, unless there is a specific need to do otherwise.
Binding to localhost reduces the attack surface of your application by making it only accessible to devices on the same
machine. Binding to 0.0.0.0 or "all" interfaces can make your application respond on all current and future network
interfaces.

Issue: ([#19](https://github.com/open-telemetry/sig-security/issues/19#issue-1926445623))

## Code signing / Provenance

We recommend using [`sigstore`](https://www.sigstore.dev/) to create signatures for your SIG's deliverables, such as
binaries, packages, and containers. In most cases, you can achieve that with GitHub's [build provenance attestation
action](https://github.com/actions/attest-build-provenance).

Example of actions for signing packages and binaries

```yaml
name: My release - binaries

jobs:
  release:
    permissions:
      id-token: write
      attestations: write
      packages: write
      contents: read

    steps:
      - name: Attest Build Provenance
        uses: actions/attest-build-provenance@897ed5eab6ed058a474202017ada7f40bfa52940 # v1.0.0
        with:
          subject-path: "my-artifact.tar.gz"
```

And the following for a container image:

```yaml
name: My release - container images

jobs:
  release:
    permissions:
      id-token: write
      attestations: write
      packages: write
      contents: read
    steps:
      - name: Login to GitHub Container Registry
        uses: docker/login-action@0d4c9c5ea7693da7b068278f7b52bda2a190a446 # v3.2.0
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Prepare container metadata
        id: meta
        uses: docker/metadata-action@8e5442c4ef9f78752691e2d8f8d19755c6f78e81 # v5.5.1
        with:
          images: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha

      - name: Build and push the images
        id: push
        uses: docker/build-push-action@a254f8ca60a858f3136a2f1f23a60969f2c402dd # v6.4.0
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

      - name: Attest container images
        uses: actions/attest-build-provenance@5e9cb68e95676991667494a6a4e59b8a2f13e1d0 # v1.3.3
        id: attest
        with:
          subject-name: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          subject-digest: ${{ steps.push.outputs.digest }}
          push-to-registry: true
```

Your users would then be able to verify it using `gh`:

```command
gh attestation verify my-artifact.tar.gz -o open-telemetry
```

The container image can be verified with:

```command
gh attestation verify oci://ghcr.io/open-telemetry/my-sig-deliverable:0.0.1 -o open-telemetry
```

### How it works

We recommend the following resources to understand in detail how it works:

- GitHub's blog post [Introducing Artifact Attestations–now in public
  beta](https://github.blog/2024-05-02-introducing-artifact-attestations-now-in-public-beta/).
- [`sigstore` project documentation](https://docs.sigstore.dev/), altough it makes it sound more complicated than it
  really is.

In particular, this is how it works on our setup:

- When your software is being released as part of a GitHub Workflow, the GitHub Action (or `goreleaser`, see [Go](#go))
  obtains an OIDC token from GitHub, which contains the organization, repository, and build information (workflow
  execution, git reference, ...)
- Your artifact(s) is signed with an ephemeral key, with the token metadata being part of it (issuer, identity, ...)
- The results of this action are published on a transparency log, like this for the [container image for OTel Collector
  Contrib v0.104.0](https://search.sigstore.dev/?logIndex=107849861)

### Go

For Go projects, we have success using the signing integration in `goreleaser`. This uses `cosign` (from `sigstore`) as
well, consistent with our recommendation. More recently, GitHub published an improved support for provenance
attestations, which are the base for our recommendation.

### Other languages

We do not currently have other usage of `sigstore` as part of the project. The links below are not official
recommendations, and the SIG Security would certainly appreciate to hear about your experiences.

- [NPM](https://docs.npmjs.com/generating-provenance-statements)
