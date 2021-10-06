#!/usr/bin/env python

import os
from datetime import datetime, timedelta
from os.path import dirname, join

import github3
from dotenv import load_dotenv

if __name__ == "__main__":

    # Load env variables from file
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    # Auth and identitiy to GitHub.com
    gh = github3.login(token=os.getenv("GH_TOKEN"))
    os.system("git config --global user.name 'Advanced Security Enforcer'")
    os.system("git config --global user.email 'no-reply@github.com'")

    # Get all repos from organization
    organization = os.getenv("ORGANIZATION")
    gh_actor = os.getenv("GH_ACTOR")
    date = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d")
    search_string = (
        "org:" + str(organization) + " created:" + str(date) + " archived:false"
    )
    allowed_languages = [
        "C",
        "C++",
        "C#",
        "Go",
        "Java",
        "JavaScript",
        "TypeScript",
        "Python",
    ]
    all_repos = gh.search_repositories(search_string)

    if len(all_repos) == 0:
        print("no repos found")
    for short_repository in all_repos:
        print(short_repository.full_name)
        # check if the repo is compatible language using short_repository.languages_url
        for language in short_repository.repository.languages():
            if language[0] in allowed_languages:
                # clone the repo
                os.system(
                    "git clone https://%s:%s@github.com/%s"
                    % (gh_actor, os.getenv("GH_TOKEN"), short_repository.full_name)
                )
                # checkout a branch called code-scanning
                os.chdir("%s" % short_repository.name)
                os.system("git checkout -b code-scanning")
                # git add the code-scanning file
                os.system("mkdir -p .github/workflows")
                # Copy the default configuration file to the proper directory
                os.system("cp ../codeql.yml .github/workflows/")
                os.system("git add .github/workflows/codeql.yml")
                # git commit that file
                os.system(
                    "git commit -m'Request to add code scanning configuration to this repository'"
                )
                # git push -u origin code-scanning
                os.system("git push -u origin code-scanning")
                # open a PR from that branch to the default branch
                default_branch = short_repository.default_branch
                pr_body = str(os.getenv("PR_BODY"))
                short_repository.repository.create_pull(
                    "Request for Code Scanning",
                    default_branch,
                    "code-scanning",
                    body=pr_body,
                )
                # Clean up repository dir
                os.chdir("../")
                os.system("rm -rf %s" % short_repository.name)
                break
    print("done")
