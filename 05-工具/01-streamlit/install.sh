#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./.venv/bin/python3.14 -m pip install "$@"
