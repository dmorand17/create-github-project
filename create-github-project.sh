#!/usr/bin/env bash
set -eou pipefail

#
#   This file is linked into ${HOME}/.local/bin/create-github-project
#
CURRENT_WORKING_DIR=$(pwd)
SCRIPT_DIR=$(dirname $(realpath $0))
pushd $SCRIPT_DIR &>/dev/null

source .venv/bin/activate
./create_github_project/main.py ${CURRENT_WORKING_DIR} $*
