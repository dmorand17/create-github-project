#!/usr/bin/env bash
set -eou pipefail

SCRIPT_DIR=$(dirname "$0")
pushd "$SCRIPT_DIR" &>/dev/null

if [[ ! -d ".venv" ]] ; then
    echo "Setting up venv... This is only required on fresh clones."
    python3 -m venv --system-site-packages .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

REPO_ROOT="$(git rev-parse --show-toplevel)"

ln -fs "${REPO_ROOT}/create-github-project.sh" "${HOME}/.local/bin/create-github-project"
popd &>/dev/null
