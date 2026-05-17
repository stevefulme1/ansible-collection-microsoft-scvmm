# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import types

import pytest


def _ensure_namespace_package():
    """Wire up the ``ansible_collections.microsoft.scvmm`` namespace so that
    ``importlib.import_module`` resolves modules from the local checkout
    without requiring a full collection install.
    """
    import pathlib

    collection_root = pathlib.Path(__file__).resolve().parents[2]  # tests/unit -> repo root
    plugins_root = collection_root / "plugins"

    for name in (
        "ansible_collections",
        "ansible_collections.microsoft",
        "ansible_collections.microsoft.scvmm",
        "ansible_collections.microsoft.scvmm.plugins",
        "ansible_collections.microsoft.scvmm.plugins.modules",
    ):
        if name not in sys.modules:
            pkg = types.ModuleType(name)
            pkg.__path__ = []
            pkg.__package__ = name
            sys.modules[name] = pkg

    # Point the ``modules`` namespace at the actual plugins/modules directory
    sys.modules["ansible_collections.microsoft.scvmm.plugins.modules"].__path__ = [
        str(plugins_root / "modules"),
    ]


def _mock_optional_sdks():
    """Insert stub modules for pywinrm / pypsrp so tests pass on systems
    (CI runners, macOS dev boxes) where those SDKs are not installed.
    """
    for mod_name in ("winrm", "pypsrp", "pypsrp.client"):
        if mod_name not in sys.modules:
            sys.modules[mod_name] = types.ModuleType(mod_name)


_mock_optional_sdks()
_ensure_namespace_package()


@pytest.fixture
def module_args():
    """Common SCVMM connection arguments used by every module."""
    return {
        "scvmm_server": "scvmm.test.local",
        "scvmm_port": 8100,
        "scvmm_username": "admin",
        "scvmm_password": "test",
    }
