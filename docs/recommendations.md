# Recommendations

This document lists recommendations from the Security SIG for
the consideration of OpenTelemetry SIGs.

## CodeQL Scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis
of the code in various repositories. The recommendation is to run CodeQL on every
pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

 sig-security/#10

# Investigate code signing OS-specific packages (deb/rpm/...)

Code signing is a critical security practice for ensuring the authenticity and integrity of software packages, regardless of the operating system or package format. Different operating systems and package management systems have their own methods for code signing. 

### code signing in OS-specific package formats like DEB (Debian) and RPM (Red Hat Package Manager):

1. DEB (Debian/Ubuntu):

    DEB packages are used in Debian-based Linux distributions like Debian, Ubuntu, and their derivatives.
    Code signing in DEB packages is primarily managed through the use of GPG (GNU Privacy Guard) keys. The steps typically include:
        Maintainers sign the source packages with their GPG key.
        Maintainers or build systems sign the resulting binary packages (the DEB files) with their GPG keys.
    A signature file is included alongside the package, typically with a .dsc or .changes file extension.
    Users can verify the signature of a DEB package using GPG to ensure it was not tampered with during download or distribution.

2. RPM (Red Hat Package Manager):

    RPM packages are used in Red Hat-based Linux distributions such as Red Hat Enterprise Linux (RHEL), CentOS, Fedora, and openSUSE.
    RPM package signing involves the use of GPG keys as well. Here's how it works:
        Maintainers or build systems sign the RPM packages with their GPG keys.
        The signature is embedded within the RPM package file.
    Users can use RPM package management tools like rpm or dnf to verify the package's signature.

3. Snap Packages (Ubuntu):

    Ubuntu's Snap packages use a different approach to code signing. Each snap is signed by the developer, and the signature is verified by the Snap Store during installation.
    Snap developers create a snap package and sign it with their credentials, and the Snap Store maintains a list of trusted developers.
    Users can trust that the package hasn't been tampered with, as the Snap Store verifies the signature during installation.

4. Flatpak (Cross-Distribution):

    Flatpak, designed for cross-distribution use, also employs code signing.
    Flatpak bundles an application along with its dependencies and signs the entire package. This provides a degree of isolation and security.
    Users can verify the signature of a Flatpak package to ensure that it's authentic and unaltered.

In all these package formats, code signing is used to verify the authenticity and integrity of the software packages. Developers and maintainers sign packages with their cryptographic keys, and users can use package management tools to check the signatures. The use of trusted cryptographic keys ensures that the packages have not been tampered with during distribution, enhancing security and trust in the software ecosystem.

Issue: ([#10](https://github.com/open-telemetry/sig-security/issues/10))


