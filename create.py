#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv
from github import Github, GithubException
from pathlib import Path
import subprocess
import re

load_dotenv()


class bcolors:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_HOME = os.getenv("GITHUB_PROJECT_HOME")
README_TEMPLATE = """
# PROJECT_NAME

Description of project

## Installation

```bash
```

## Usage

```bash
```
"""


def run(cmd_lst, **kwargs):
    print(f"$ {' '.join(cmd_lst)}")
    subprocess.run(cmd_lst, **kwargs)
    print()


def create(project_name):
    p = Path(PROJECT_HOME)
    if not p.is_dir():
        sys.exit(f"{PROJECT_HOME} was not found, check directory exists.")

    project_dir = p / project_name
    if project_dir.is_dir():
        sys.exit(f"'{project_dir}' already exists!")
    else:
        project_dir.mkdir()

    curr_dir = os.getcwd()
    os.chdir(project_dir)
    print(
        f">>> Changed working directory \nold: '{curr_dir}', new: '{project_dir}'\n"
    )

    user = Github(TOKEN).get_user()
    # Check if repo already exists
    try:
        existing_repo = user.get_repo(project_name)
        if existing_repo:
            sys.exit(f"{existing_repo.html_url} already exists!")
    except GithubException as e:
        if e.status == 404:
            print(">>> Repository not found, creating...")
    repo = user.create_repo(project_name, license_template="mit")
    print(f">>> Created {project_name} in github!")
    print(f">>> url: {repo.html_url}, default_branch: {repo.default_branch}\n")

    (project_dir / "README.md").write_text(README_TEMPLATE)
    init_local_repo(project_dir, project_name)


def init_local_repo(project_dir, project_name):
    print(">>> Initializing local git repository")
    run(("git", "init"), check=True)

    print(">>> Adding remote")
    run(
        (
            "git",
            "remote",
            "add",
            "origin",
            f"git@github.com:{GITHUB_USERNAME}/{project_name}.git",
        ),
        check=True,
    )

    print(">>> Fetch changes from remote repo")
    run(("git", "fetch"), check=True)

    print(">>> Pull changes from 'origin/main'")
    run(("git", "pull", "origin", "main"), check=True)

    print(">>> Setting upstream")
    run(("git", "branch", "--set-upstream-to=origin/main", "main"), check=True)


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        sys.exit("Must supply a project name!")

    project_name = str(sys.argv[1])

    if re.search(r"\s", project_name):
        sys.exit(
            f"Invalid project name: '{project_name}'\nProject names should NOT contain spaces."
        )
    else:
        create(project_name)

    print(f"{bcolors.OK}Finished!{bcolors.RESET}")
