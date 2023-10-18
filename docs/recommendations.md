# Recommendations

This document lists recommendations from the Security SIG for
the consideration of OpenTelemetry SIGs.

## CodeQL Scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis
of the code in various repositories. The recommendation is to run CodeQL on every
pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

# For these signatures to be publicly verified by otel users, we need to publish our public key someplace findable. 
To make the public keys used for signing artifacts by the OpenTelemetry Java projects publicly available and discoverable,Here are some of existing location for these pubkeys:

### Publish Public Keys to a Keyserver:
You can publish the public keys to a PGP keyserver. There are several well-known key servers available for this purpose. You can use a command-line tool like gpg to upload your public keys to a keyserver.

### Create Documentation: In the README or documentation of your projects, provide clear instructions on where users can find and import the public keys. Include the key IDs, fingerprints, or any other relevant information neede for users to identify and import the keys.

### Project Website:
If your projects have a website or a dedicated page, you can also include the public keys and instructions on that page.

### Include in Project Repositories:
Add the public keys (in ASCII armored format) to a trusted location within your GitHub repositories. Ensure that these keys are protected from unauthorized access and tampering.

### Utilize GitHub Actions or CI/CD Pipeline:
If you're using GitHub Actions for building and signing your artifacts, you can include a step in your workflow that automatically publishes the public keys to a keyserver after a successful build. This ensures that the public keys are kept up-to-date.

### Community Involvement:
Encourage community members and contributors to verify and sign your project's keys, which can help in building a web of trust over time.

### Verifiable Web of Trust (as mentioned):
In the future, you can explore establishing a verifiable web of trust. This involves having key signing parties, where project members physically meet and verify each other's keys. This can enhance trust in the keys used for signing.

