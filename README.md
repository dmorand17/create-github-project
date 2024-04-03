# create-github-project

Automated way to create a local project. Inspired by [KalleHallden/ProjectInitializationAutomation](https://github.com/KalleHallden/ProjectInitializationAutomation)

1. Create local project
2. Create github repo
3. Initialize the local project

## Prerequisites

- Python3

## 🏁 Getting Started

1/ Install create-github-project

```bash
./install.sh
```

Installation adds a `create-github-project` symbolic link in `${HOME}/.local/bin`

2/ Setup environment variables

```bash
cp .env.sample .env
```

Modify variables

- **GITHUB_USERNAME**: github username
- **GITHUB_TOKEN**: refer to [managing your personal access tokens](https://docs.github.com/en/enterprise-server@3.9/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- **GITHUB_PROJECT_HOME**:

_Example_

```
GITHUB_USERNAME=some_github_username
GITHUB_TOKEN=github_pat_redacted
GITHUB_PROJECT_HOME=/Users/username/workspace
```

## 🚀 Usage

```bash
create-github-project <name>
```

## 🛠️ Development

Create and launch virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 📌 TODO

- Create project specific README (e.g. Python, typescript, rust, bash)
