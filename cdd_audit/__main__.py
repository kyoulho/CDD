from __future__ import annotations

import sys

from cdd_audit.cli import run_cli

raise SystemExit(run_cli(sys.argv[1:]))
