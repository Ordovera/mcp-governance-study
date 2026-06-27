"""Shared path helpers for the reproduction scripts.

Two classes of data are resolved differently:

  - The heavy evidence corpus lives OUTSIDE the repo (archived on Zenodo; see
    data/README.md). Locate it with corpus_path(), driven by --data-dir or the
    $MCP_DATA_DIR environment variable, defaulting to the current directory.

  - Small in-repo artifacts (validation samples, residual taxonomy) live under
    <repo>/data/. Locate them with repo_data(), independent of the working dir.

This lets any script run from any directory, e.g.:

    python3 code/paper-numbers-postg.py --data-dir /path/to/zenodo-corpus
    MCP_DATA_DIR=/path/to/zenodo-corpus python3 code/sensitivity-negation-variant.py
"""

import os
from importlib.util import spec_from_file_location, module_from_spec

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def corpus_path(name, data_dir=None):
    """Resolve an external corpus file. Precedence: explicit data_dir argument,
    then $MCP_DATA_DIR, then the current working directory."""
    base = data_dir or os.environ.get("MCP_DATA_DIR") or "."
    return os.path.join(base, name)


def repo_data(*parts):
    """Resolve a small in-repo data file under <repo>/data/, cwd-independent."""
    return os.path.join(REPO, "data", *parts)


def load_rgd():
    """Import rerun-gap-detection.py from this script's directory regardless of
    the working directory. (It is hyphenated, so it cannot be imported by name.)"""
    spec = spec_from_file_location("rgd", os.path.join(HERE, "rerun-gap-detection.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_data_dir_arg(ap):
    """Attach a standard --data-dir option to an argparse parser and return it."""
    ap.add_argument(
        "--data-dir",
        default=None,
        help="Directory containing the evidence corpus JSON (default: "
             "$MCP_DATA_DIR, or the current directory). The corpus is archived "
             "on Zenodo; see data/README.md.",
    )
    return ap
