#!/usr/bin/env python3

import os
import re
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from github import Github, GithubException

load_dotenv()


class bcolors:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_HOME = os.getenv("GITHUB_PROJECT_HOME")
README_TEMPLATE = """# PROJECT_NAME

<insert description here>

## Getting Started

```bash
...
```

## Development

Development notes here

Create and launch virtual environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
"""


def _run(cmd_lst, **kwargs):
    print(f"$ {' '.join(cmd_lst)}")
    subprocess.run(cmd_lst, **kwargs)
    print()


def _create_directory(project_name):
    p = Path(PROJECT_HOME)
    if not p.is_dir():
        sys.exit(f"[!] {PROJECT_HOME} was not found, check directory exists.")

    project_dir = p / project_name
    if project_dir.is_dir():
        sys.exit(f"'[!] {project_dir}' already exists!")
    else:
        project_dir.mkdir()

    curr_dir = os.getcwd()
    os.chdir(project_dir)
    print(f"[-] Changed working directory \nold: '{curr_dir}', new: '{os.getcwd()}'\n")

    return project_dir


def _create_github_repository(project_dir, project_name):
    user = Github(TOKEN).get_user()
    # Check if repo already exists
    try:
        existing_repo = user.get_repo(project_name)
        if existing_repo:
            sys.exit(f"{existing_repo.html_url} already exists!")
    except GithubException as e:
        if e.status == 404:
            print("[-] Repository not found, creating...")
    repo = user.create_repo(project_name, license_template="mit")
    print(f"[-] Created {project_name} in github!")
    print(f"[-] url: {repo.html_url}, default_branch: {repo.default_branch}\n")


def _init_local_repo(project_dir, project_name):
    (project_dir / "README.md").write_text(README_TEMPLATE)
    print("[-] Initializing local git repository")
    _run(("git", "init"), check=True)

    print("[-] Adding remote")
    _run(
        (
            "git",
            "remote",
            "add",
            "origin",
            f"git@github.com:{GITHUB_USERNAME}/{project_name}.git",
        ),
        check=True,
    )

    print("[-] Fetch changes from remote repo")
    _run(("git", "fetch"), check=True)

    print("[-] Pull changes from 'origin/main'")
    _run(("git", "pull", "origin", "main"), check=True)

    print("[-] Setting upstream")
    _run(("git", "branch", "--set-upstream-to=origin/main", "main"), check=True)


def init_and_create(project_name):
    project_dir = _create_directory(project_name)
    _create_github_repository(project_dir, project_name)
    _init_local_repo(project_dir, project_name)

    return project_dir


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        sys.exit("Must supply a project name!")

    project_name = str(sys.argv[1])

    if re.search(r"\s", project_name):
        sys.exit(
            f"Invalid project name: '{project_name}'\nProject names should NOT contain spaces."
        )
    else:
        project_dir = None
        try:
            project_dir = init_and_create(project_name)
        finally:
            if project_dir:
                print(f"COMMAND: `cd {project_dir}` to begin!")
                print(f"{bcolors.OK}🎉 Finished!{bcolors.RESET}")
