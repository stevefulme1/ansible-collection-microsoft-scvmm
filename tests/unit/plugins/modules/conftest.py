# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Common fixtures for SCVMM collection unit tests.

These tests validate the Python documentation stubs that accompany
each PowerShell module.  They do NOT execute the PowerShell logic.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib
import os
import sys
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

COLLECTION_ROOT = Path(__file__).resolve().parents[4]
MODULES_DIR = COLLECTION_ROOT / "plugins" / "modules"
DOC_FRAGMENTS_DIR = COLLECTION_ROOT / "plugins" / "doc_fragments"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_module_doc(module_name: str):
    """Import a module's Python stub and return (DOCUMENTATION, EXAMPLES, RETURN).

    The Python files in this collection are documentation-only stubs
    (the real logic lives in the paired ``.ps1`` file).  We import
    them purely to access the ``DOCUMENTATION``, ``EXAMPLES``, and
    ``RETURN`` module-level strings.
    """
    module_file = MODULES_DIR / f"{module_name}.py"
    if not module_file.exists():
        pytest.skip(f"{module_file} not found")

    spec = importlib.util.spec_from_file_location(module_name, str(module_file))
    mod = importlib.util.module_from_spec(spec)

    # Prevent side-effects from any module_utils imports that may not
    # be resolvable in the test environment.
    try:
        spec.loader.exec_module(mod)
    except (ImportError, ModuleNotFoundError):
        # Re-read as raw text and exec only the string constants.
        source = module_file.read_text()
        exec(compile(source, str(module_file), "exec"), mod.__dict__)

    documentation = getattr(mod, "DOCUMENTATION", None)
    examples = getattr(mod, "EXAMPLES", None)
    returns = getattr(mod, "RETURN", None)

    return documentation, examples, returns


def parse_documentation(raw_doc: str) -> dict:
    """Parse the YAML documentation string into a dict."""
    return yaml.safe_load(raw_doc)


# ---------------------------------------------------------------------------
# Connection doc-fragment options (used for no_log checks)
# ---------------------------------------------------------------------------

CONNECTION_FRAGMENT = DOC_FRAGMENTS_DIR / "scvmm_connection.py"

# Fields from the connection fragment that should carry ``no_log: true``
# when they accept credentials.
CREDENTIAL_FIELD_NAMES = frozenset(
    {
        "password",
        "scvmm_password",
        "credential_password",
        "secret",
        "token",
        "api_key",
    }
)

# Fields that should have ``no_log: true`` in module argument_specs.
SENSITIVE_PARAM_PATTERNS = frozenset(
    {
        "password",
        "secret",
        "token",
        "credential",
        "api_key",
    }
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def modules_dir():
    """Return the absolute path to the plugins/modules directory."""
    return MODULES_DIR


@pytest.fixture
def collection_root():
    """Return the absolute path to the collection root."""
    return COLLECTION_ROOT


@pytest.fixture
def all_python_modules():
    """Return a list of all Python module names (without .py extension)."""
    return sorted(
        f.stem
        for f in MODULES_DIR.glob("scvmm_*.py")
        if f.stem != "__init__"
    )
