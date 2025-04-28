# Advanced-Security-Enforcer
[![CodeQL](https://github.com/zkoppert/advanced-security-enforcer/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/zkoppert/advanced-security-enforcer/actions/workflows/codeql-analysis.yml)
[![Docker Image CI](https://github.com/zkoppert/advanced-security-enforcer/actions/workflows/docker-image.yml/badge.svg)](https://github.com/zkoppert/advanced-security-enforcer/actions/workflows/docker-image.yml)
[![.github/workflows/linter.yml](https://github.com/zkoppert/advanced-security-enforcer/actions/workflows/linter.yml/badge.svg)](https://github.com/zkoppert/advanced-security-enforcer/actions/workflows/linter.yml)

## What this repository does
This code is for an active GitHub Action written in Python to check (on a schedule) for new repositories created on the previous day and open pull requests in the new repositories to enable GitHub advanced security code scanning.

## Support
If you need support using this project or have questions about it, please [open up an issue in this repository](https://github.com/zkoppert/advanced-security-enforcer/issues). Requests made directly to GitHub staff or support team will be redirected here to open an issue. GitHub SLA's and support/services contracts do not apply to this repository.

## Example workflow
```yaml
name: Enforce advanced security scanning

on:
  workflow_dispatch:
  schedule:
    - cron: '00 5 * * *'

jobs:
  build:
    name: Enforce advanced security scanning
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Run enforcer tool
      uses: zkoppert/advanced-security-enforcer@v2
      env:
        GH_ACTOR: ${{ secrets.GH_ACTOR }}
        GH_TOKEN: ${{ secrets.GH_TOKEN }}
        ORGANIZATION: ${{ secrets.ORGANIZATION }}
        PR_BODY: your text goes here
        HOURS_DELAY: 24
```
- Be sure to fill out the `env` values above with your information. More info on creating secrets can be found [here](https://docs.github.com/en/actions/security-guides/encrypted-secrets).
- Your GitHub token will need to have read/write access to all the repositories in the organization as well as the workflow permission
- You must include the `HOURS_DELAY` value and set it to a valid `int` in order to set what date the action is looking for new repositories on.
  This being configurable allows users to give more time for repositories to contain code by increasing the delay.
  The default 24 will make the action check for repos created on the previous day to see if they have code scanning enabled.
  Changing the value to 72, will make the action check for repositories created 3 days ago.

## How it does this
- A CRON job on GitHub actions triggers a nightly run of this script
- The script checks for new repositories by storing the known repositories to a file
- It then iterates over new repositories and opens a pull request for the codeql.yml file stored in this repository

## Contributions
We would :heart: contributions to improve this action. Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get involved.

## Debugging in GitHub Actions
- Add the following lines to the workflow .yaml file
  ```yaml
    env:
      ACTIONS_RUNNER_DEBUG: true
      ACTIONS_STEP_DEBUG: true
  ```
- That will enable debug printing to the action log so that you can see detailed information if issues arise.
- Setting the `HOURS_DELAY: 0` is helpful so that you can create a repository in an org and not wait to test the action against it

## Instructions to run locally
- Clone the repository
- Create a personal access token with repository permissions and workflow permissions
- Copy the `.env-example` file to `.env`
- Edit the `.env` file by adding your Personal Access Token to it and the desired organization
- Install dependencies `python -m pip install -r requirements.txt`
- Run the code `python3 enforcer.py`
- Note the log output for details on any pull requests that were opened
- After running locally this will have changed your git config user.name and user.email so those should be reset for this repository

## Docker debug instructions
- Install Docker and make sure docker engine is running
- cd to the repository
- Edit the Dockerfile to enable interactive docker debug as instructed in the comments of the file
- `docker build -t test .`
- `docker run -it test`
- Now you should be at a command prompt inside your docker container and you can begin debugging

## License
[MIT](./LICENSE)
