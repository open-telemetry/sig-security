# Recommendations

This document lists recommendations from the Security SIG for the consideration
of OpenTelemetry SIGs.

## Scanning

### CodeQL scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis
of the code in various repositories. The recommendation is to run CodeQL on
every pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

### zizmor scanning

[zizmor](https://github.com/zizmorcore/zizmor) is a static analysis tool for
GitHub Actions workflows. The recommendation is to run zizmor on every pull
request and on every commit to the main branch for repositories using GitHub
Actions.

GitHub Actions workflows are part of the project supply chain. zizmor can help
identify CI/CD security issues such as template injection, unsafe credential
handling, overly broad token permissions, risky workflow triggers, and ambiguous
or mutable action references.

Where possible, repositories should make zizmor a required code scanning check
by default, with documented opt-out handling for repositories where it is not
yet applicable.

Resources:

- [zizmor documentation](https://docs.zizmor.sh/)
- [zizmor audit rules](https://docs.zizmor.sh/audits/)
- [zizmor GitHub Actions integration](https://docs.zizmor.sh/integrations/)
- [zizmor-action](https://github.com/zizmorcore/zizmor-action)

Issue: ([#268](https://github.com/open-telemetry/sig-security/issues/268))

## Integrity

### Sign release artifacts with Sigstore Cosign

Checksums help detect corruption, but they do not authenticate who produced an
artifact when the artifact and checksum are downloaded from the same location.
If both files are replaced, checksum verification can still succeed for
malicious content.

Use [Sigstore Cosign](https://docs.sigstore.dev/cosign/) to sign release
container images and other consumer-facing artifacts, such as binaries,
archives, SBOMs, and checksum manifests. Publish instructions that let
consumers verify both the artifact and the expected signer identity.

Use Cosign's keyless signing in automated release workflows. With keyless
signing, the workflow uses an OpenID Connect (OIDC) identity and a short-lived
certificate instead of a long-lived signing key. The signing event is recorded
in Sigstore's transparency infrastructure and can be audited.

#### Sign in GitHub Actions

Use a dedicated signing job that runs only for trusted release events, such as
version tags. Grant `id-token: write` only to the job that needs the GitHub OIDC
token, and grant no other permissions beyond those needed to read or publish
the artifacts.

The following excerpt installs Cosign and signs a container image after it has
been pushed. Sign the immutable image digest, not only a mutable tag.

```yaml
jobs:
  sign:
    if: startsWith(github.ref, 'refs/tags/')
    permissions:
      contents: read
      id-token: write
      packages: write # Include only when required by the target registry.
    steps:
      - name: Install Cosign
        uses: sigstore/cosign-installer@6f9f17788090df1f26f669e9d70d6ae9567deba6 # v4.1.2

      # Run after the image push step, whose output is the manifest digest.
      - name: Sign container image
        env:
          IMAGE: ghcr.io/open-telemetry/example@${{ steps.build.outputs.digest }}
        run: cosign sign --yes "${IMAGE}"
```

For downloadable files, finalize the files before signing them and use a
Sigstore bundle rather than separate signature and certificate files. Generate
checksum manifests before signing, and do not add generated bundles to the
checksum manifest or sign the bundles themselves.

```bash
artifact=dist/example-v1.2.3-linux-amd64.tar.gz

cosign sign-blob --yes \
  --bundle "${artifact}.sigstore.json" \
  "${artifact}"
```

Publish each bundle next to its artifact. Do not modify an artifact after it is
signed. Before publishing a release, verify the image signatures and bundles
in CI using the same certificate identity and OIDC issuer that users will rely
on.

#### Document verification

Document copy-pasteable verification commands for every class of signed
artifact. Bind verification to the exact release workflow and tag using
`--certificate-identity`; a repository-wide identity regular expression could
accept a signature from an unrelated workflow in the same repository.

For example:

```bash
repository=open-telemetry/example
release_tag=v1.2.3
certificate_identity="https://github.com/${repository}/.github/workflows/release.yml@refs/tags/${release_tag}"
certificate_oidc_issuer=https://token.actions.githubusercontent.com
image="ghcr.io/open-telemetry/example@sha256:IMAGE_DIGEST"

cosign verify \
  --certificate-identity "${certificate_identity}" \
  --certificate-oidc-issuer "${certificate_oidc_issuer}" \
  "${image}"

artifact=example-v1.2.3-linux-amd64.tar.gz
cosign verify-blob "${artifact}" \
  --bundle "${artifact}.sigstore.json" \
  --certificate-identity "${certificate_identity}" \
  --certificate-oidc-issuer "${certificate_oidc_issuer}"
```

If verification fails, consumers should stop and must not run, deploy, or
compile the artifact.

Signatures authenticate the final bytes and signer identity, but do not by
themselves describe how the artifact was built. Checksums, SBOMs, and build
provenance attestations provide complementary information.

Resources:

- [Sigstore security model](https://docs.sigstore.dev/about/security/)
- [Sigstore CI quickstart](https://docs.sigstore.dev/quickstart/quickstart-ci/)
- [Signing containers](https://docs.sigstore.dev/cosign/signing/signing_with_containers/)
- [Signing blobs](https://docs.sigstore.dev/cosign/signing/signing_with_blobs/)
- [Verifying signatures](https://docs.sigstore.dev/cosign/verifying/verify/)
- [GitHub OIDC reference](https://docs.github.com/en/actions/reference/security/oidc)

### Attest release artifacts with GitHub Artifact Attestations

Build provenance attestations help consumers trace a release artifact to the
repository, commit, workflow, and CI environment that produced it. This gives
auditors and automated policy checks evidence about where and how an artifact
was built, while binding that evidence to the artifact's digest.

Use GitHub Artifact Attestations for consumer-facing artifacts built in GitHub
Actions, such as binaries, archives, packages, software bills of materials
(SBOMs), checksum manifests, and container images. The `actions/attest` action
generates a signed [in-toto](https://in-toto.io/) statement with
[SLSA build provenance](https://slsa.dev/provenance/v1), using the workflow's
GitHub OIDC identity and a short-lived Sigstore certificate.

Attestations complement artifact signatures. A signature authenticates the
finished bytes and signer identity; a provenance attestation adds signed claims
about the build. Neither proves that the source or artifact is secure, so
consumers must verify the attestation against an expected identity and policy.

#### Generate build provenance in GitHub Actions

Generate attestations only for trusted release events, such as version tags.
Finalize each artifact before attesting it, because the attestation records the
digest of the exact bytes present at that point. Do not modify the artifact
afterward.

Grant `id-token: write` and `attestations: write` only to the job that
creates the attestation. Grant no other permissions beyond those the build and
publication steps require. Pin the action to a full commit SHA.

The following excerpt attests a downloadable release archive after it has been
built and packaged:

```yaml
jobs:
  release:
    if: startsWith(github.ref, 'refs/tags/')
    permissions:
      attestations: write
      contents: read
      id-token: write
    steps:
      # Build and finalize the release archive before this step.
      - name: Attest release artifact
        uses: actions/attest@f7c74d28b9d84cb8768d0b8ca14a4bac6ef463e6 # v4.2.0
        with:
          subject-path: dist/example-v1.2.3-linux-amd64.tar.gz
```

Use a multiline path or glob to attest multiple finalized files. For a
container image, push the image first, pass its fully qualified name without a
tag as `subject-name`, pass the immutable digest from the build step as
`subject-digest`, and set `push-to-registry: true`. Add
`packages: write` only when required to publish to the target registry and
`artifact-metadata: write` when creating a linked artifact storage record.

#### Verify and enforce provenance

Generating attestations alone provides no security benefit. Publish
copy-pasteable verification commands and enforce them in artifact promotion,
deployment, or admission workflows.

Verify the repository, the exact signer workflow, and the expected release ref.
Using only `--owner` trusts attestations from every repository owned by that
organization and is usually too broad.

For example:

```bash
repository=open-telemetry/example
release_tag=v1.2.3
signer_workflow="${repository}/.github/workflows/release.yml"
artifact=example-v1.2.3-linux-amd64.tar.gz

gh attestation verify "${artifact}" \
  --repo "${repository}" \
  --signer-workflow "${signer_workflow}" \
  --source-ref "refs/tags/${release_tag}"

image=oci://ghcr.io/open-telemetry/example@sha256:IMAGE_DIGEST
gh attestation verify "${image}" \
  --repo "${repository}" \
  --signer-workflow "${signer_workflow}" \
  --source-ref "refs/tags/${release_tag}"
```

If the build uses a reusable workflow, verify the reusable workflow's identity
as the signer. If verification fails, consumers should stop and must not run,
deploy, or compile the artifact.

A compromised build workflow or runner can still produce malicious artifacts
and attest them. Protect release workflows, use isolated runners, minimize job
permissions, and consider a vetted reusable workflow as a trusted builder when
stronger isolation is required.

Resources:

- [About artifact attestations](https://docs.github.com/actions/concepts/security/artifact-attestations)
- [Using artifact attestations](https://docs.github.com/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
- [`actions/attest`](https://github.com/actions/attest)
- [`gh attestation verify`](https://cli.github.com/manual/gh_attestation_verify)
- [Signing artifacts, attesting builds, and why you should do both](https://some-natalie.dev/blog/signing-attesting-builds/)

## GitHub immutable releases

GitHub supports **immutable releases**, which prevent release assets from being
modified after a release is published. This helps reduce supply-chain risk by
making it harder for an attacker (or a compromised account/token) to silently
swap binaries, SBOMs, or other artifacts after consumers have started
downloading or verifying them.

Recommendation: enable immutable releases and treat each published release as
a permanent, verifiable record.

Best practices:

- Consider creating releases as **drafts first**. This allows you to attach all
  assets before the release becomes immutable.
- Prefer a fully automated, reproducible release process (CI builds artifacts
  from a tagged commit, then publishes the release). Avoid building artifacts on
  developer workstations.
- Publish integrity metadata alongside assets (for example: checksums, SBOMs,
  provenance/attestations, and/or signatures) so downstream users can verify
  what they downloaded matches what you produced.
- Restrict who/what can publish releases:
  - Use the smallest possible GitHub Actions permissions for release workflows.
- If you need to fix a bad release, publish a new release (and clearly mark the
  old one as deprecated) rather than replacing assets in-place.

Resources:

- [Immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
- [Verifying the integrity of a release](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/verifying-the-integrity-of-a-release)

## GitHub environment secrets

GitHub [environment secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#creating-secrets-for-an-environment)
provide an additional layer of protection for sensitive secrets used in
publishing, signing, and other privileged workflows.

With **repository secrets**, any workflow running in the repository can access
them, including workflows triggered on non-protected branches. This means
anyone with Write access could push a non-protected branch containing secret
exfiltration code and trigger a workflow without going through a PR review.

With **environment secrets**, access is restricted to workflows running in the
context of a named environment, and that environment can be configured to only
allow deployments from specific branches. This means even a contributor with
Write access cannot access the secrets without their code successfully passing
all branch protection criteria (i.e. an approved and merged PR).

Recommendation: migrate publishing, signing, and other privileged secrets from
repository secrets to an environment with a deployment branch policy restricting
access to `main` and `release/**` branches.

Steps:

1. Create and configure an environment (e.g., `protected`) with a deployment
   branch policy via Terraform in [open-telemetry/admin](https://github.com/open-telemetry/admin),
   allowing only `main` and `release/**` (adjust to match your branching
   strategy).
2. Request admin permission to manage secrets for the environment. See
   [Request Repository Admin Permissions](https://github.com/open-telemetry/community/blob/main/guides/maintainer/github-admin-processes.md#request-repository-admin-permissions).
3. Add your publishing and signing secrets to the environment.
4. Update release workflows to run in the context of the environment:

   ```yaml
   jobs:
     release:
       environment: protected
       steps:
         ...
   ```

   Note: if you ever need to make an older patch release from a release branch,
   backport this workflow change to that branch first.
5. Remove the corresponding repository-level secrets. If both exist, the
   repository-level secret remains accessible from any branch, defeating the
   purpose.

Resources:

- [Using environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Creating secrets for an environment](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#creating-secrets-for-an-environment)
- [Example migration in opentelemetry-java](https://github.com/open-telemetry/opentelemetry-java/pull/8432/changes#diff-bae0feaab53d9bdd636360014c03f3456cd796c65e3984b5373443e92fdb5efeR17)

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
