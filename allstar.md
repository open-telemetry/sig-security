I have investigated what Allstar is about, it's capabilities and how it aligns with the needs of this project as inidicated in the checklist in issue #12.
I found out that Allstar is a Security Policy for open source projects which canhelp to ensure that all repositories have a 
1. Security policy
2. Scan all repos for common vulnerabilitie 
3. Enforce best practices for code reviews and, 
4. Require security testing for all releases. I am unsure how to proceed from here.

## The items that needs to be configured manaully include;
1. Private vulnerability reporting

## The steps needed to enable allstar app includes, 
 1. Install the Allstar GitHub app.
 2.  Open the installation page and click Configure
If you have multiple organizations, select the one you want to install Allstar on
3. Select "All Repositories" under Repository Access, even if you plan to disable Allstar on some repositories later
4. Fork the sample repository
5. Open the sample repository and click the "Use this template" button
6. In the field for Repository Name, type .allstar
7. Click "Create repository from template"
https://github.com/ossf/allstar/blob/main/manual-install.md
