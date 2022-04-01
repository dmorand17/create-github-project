#!/usr/bin/env bash
set -eou pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"

ln -s "${REPO_ROOT}/create.py" ${HOME}/.local/bin/create-github-project
