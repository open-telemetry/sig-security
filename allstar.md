I have investigated what Allstar is about, it's capabilities and how it aligns with the needs of this project as inidicated in the checklist in issue #12.
Allstar is a security policy engine that helps organizations automate and enforce security best practices. Allstar can be used to scan code, dependencies, andinfrastructure for vulnerabilities. Allstar can also be used to enforce best practices for code reviews, security testing, and vulnerability management.

##Based on the checklist on issue #12, All star can cover everything on the checklist.

- CodeQL enabled via GitHub Actions: Allstar can be integrated with GitHub Actions to automatically scan code for vulnerabilities using CodeQL.
- Static code analysis:  Allstar can be integrated with govulncheck to automatically scan Go code for vulnerabilities.
- Repository security settings: Allstar can be used to enforce security settings for repositories, such as requiring a security policy and enabling security advisories.
- Dependabot alerts: Allstar can be integrated with Dependabot to automatically scan dependencies for vulnerabilities.
- Code scanning alerts: Allstar can be integrated with code scanning tools to automatically scan code for vulnerabilities.

## Items that still needs to be manually configured in individual repositories
- Security Policies
- Security advisories
- Private vulnerabilty reporting
- Dependabot alerts
- Code scanning alerts

###Allstar can also configure the following that were not listed on the checklist
- Branch protection
- Security testing
- Code review requirements

## The steps needed to enable Allstar app across organisation includes; 
 1. Install the Allstar GitHub app.
 2.  Open the [installation page](https://github.com/apps/allstar-app) and click Configure. If you have multiple organizations, select the one you want to install Allstar on
3. Select "All Repositories" under Repository Access, even if you plan to disable Allstar on some repositories later
4. Fork the [sample repository](https://github.com/jeffmendoza/dot-allstar-quickstart)
5. Open the sample repository and click the "Use this template" button
6. In the field for Repository Name, type `.allstar`
7. Click "Create repository from template"
That's it! All current Allstar [policies](https://github.com/ossf/allstar?installation_id=42556888&setup_action=install#policies) are now enabled on all your repositories. Allstar will create an issue if a policy is violated.
To change any configurations, see the [manual installation directions](https://github.com/ossf/allstar/blob/main/manual-install.md).


