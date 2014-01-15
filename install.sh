#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

[[ -d "$DIR/venv" ]] || virtualenv-2.7 --no-site-packages --distribute "$DIR/venv"
source "$DIR/venv/bin/activate"
pip install -r "$DIR/reqs.txt"
