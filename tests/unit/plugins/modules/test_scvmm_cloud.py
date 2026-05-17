# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for the scvmm_cloud module argument specification."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib

import yaml


MODULE = "ansible_collections.microsoft.scvmm.plugins.modules.scvmm_cloud"


def _load_doc():
    mod = importlib.import_module(MODULE)
    return yaml.safe_load(mod.DOCUMENTATION)


class TestScvmmCloudArgSpec:
    """Validate the scvmm_cloud DOCUMENTATION-based argument specification."""

    def test_module_has_documentation(self):
        mod = importlib.import_module(MODULE)
        assert hasattr(mod, "DOCUMENTATION")
        assert hasattr(mod, "EXAMPLES")
        assert hasattr(mod, "RETURN")

    def test_documentation_is_valid_yaml(self):
        doc = _load_doc()
        assert isinstance(doc, dict)
        assert doc["module"] == "scvmm_cloud"

    def test_name_is_required(self):
        doc = _load_doc()
        name_opt = doc["options"]["name"]
        assert name_opt["required"] is True
        assert name_opt["type"] == "str"

    def test_state_choices(self):
        doc = _load_doc()
        state_opt = doc["options"]["state"]
        assert set(state_opt["choices"]) == {"present", "absent"}
        assert state_opt["default"] == "present"

    def test_host_group_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["host_group"]["type"] == "str"
        assert doc["options"]["host_group"].get("required") is not True

    def test_description_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["description"]["type"] == "str"
        assert doc["options"]["description"].get("required") is not True

    def test_extends_scvmm_connection_fragment(self):
        doc = _load_doc()
        assert "microsoft.scvmm.scvmm_connection" in doc["extends_documentation_fragment"]

    def test_short_description_present(self):
        doc = _load_doc()
        assert doc.get("short_description"), "short_description must not be empty"

    def test_version_added(self):
        doc = _load_doc()
        assert doc.get("version_added") is not None
