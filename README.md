# Advanced-Security-Enforcer

## What this repository does
This code is for a GitHub Action to check on a schedule for new repositories created in the last 24 hours and open pull requests in the new repositories for code scanning.

## Example workflow
```yaml
name: Enforce advanced security scanning

on:
  pull-request:

jobs:
  build:
    name: Enforce advanced security scanning
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2
    
    - name: Run enforcer tool
      uses: github/advanced-security-enforcer@v1
      env:
        GH_ACTOR: ${{ secrets.GH_ACTOR }}
        GH_TOKEN: ${{ secrets.GH_TOKEN }}
        ORGANIZATION: ${{ secrets.ORGANIZATION }}
        PR_BODY: your text goes here
```
- Be sure to fill out the `env` values above with your information. More info on creating secrets can be found [here](https://docs.github.com/en/actions/security-guides/encrypted-secrets).
- Your GitHub token will need to have read/write access to all the repos in the organization

## How it does this
- A CRON job on GitHub actions triggers a nightly run of this script
- The script checks for new repositories by storing the known repositories to a file
- It then iterates over new repositories and opens a pull request for the codeql.yml file stored in this repository

## Instructions to run locally
- Clone the repository
- Create a personal access token with read only permissions
- Copy the `.env-example` file to `.env`
- Edit the `.env` file by adding your Personal Access Token to it and the desired organization
- Install dependencies `pip install -r requirements.txt`
- Run the code `python3 enforcer.py`
- Note the log output for details on any pull requests that were opened
- After running locally this will have changed your git config user.name and user.email so those should be reset for this repository
