"""Kaggle CLI wrapper used from the Hark sandbox.

WHY: behind the sandbox proxy, kaggle's token introspection call fails, so every command
errors before it starts. We replace KaggleApi._introspect_token (a PRIVATE kaggle function)
with one that returns the username. Real API calls still authenticate normally.

FRAGILE: private API, tested only with kaggle==2.2.5 (pinned in tools/requirements-kaggle.txt).
If kaggle is upgraded and the attribute disappears, this wrapper falls back to the plain CLI.
On a normal PC (no proxy) you do not need this file: just run `kaggle ...`.

Username comes from env KAGGLE_USERNAME (default kept for the current private setup).
Before making the repo public: set KAGGLE_USERNAME, drop the default below, and change the
"ironindiarat/..." ids in tools/*/kernel-metadata.json (JSON cannot read env variables).
"""
import os
import sys

from kaggle.api.kaggle_api_extended import KaggleApi

USERNAME = os.environ.get("KAGGLE_USERNAME", "ironindiarat")
if hasattr(KaggleApi, "_introspect_token"):
    KaggleApi._introspect_token = lambda self, t: USERNAME
else:  # pragma: no cover
    print("kgl.py: kaggle has no _introspect_token (version changed?); running the plain CLI", file=sys.stderr)

from kaggle.cli import main  # noqa: E402

sys.exit(main())
