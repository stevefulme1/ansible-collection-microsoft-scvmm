# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for the scvmm_host module argument specification."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib

import yaml


MODULE = "ansible_collections.microsoft.scvmm.plugins.modules.scvmm_host"


def _load_doc():
    mod = importlib.import_module(MODULE)
    return yaml.safe_load(mod.DOCUMENTATION)


class TestScvmmHostArgSpec:
    """Validate the scvmm_host DOCUMENTATION-based argument specification."""

    def test_module_has_documentation(self):
        mod = importlib.import_module(MODULE)
        assert hasattr(mod, "DOCUMENTATION")
        assert hasattr(mod, "EXAMPLES")
        assert hasattr(mod, "RETURN")

    def test_documentation_is_valid_yaml(self):
        doc = _load_doc()
        assert isinstance(doc, dict)
        assert doc["module"] == "scvmm_host"

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

    def test_credential_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["credential"]["type"] == "str"
        assert doc["options"]["credential"].get("required") is not True

    def test_host_group_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["host_group"]["type"] == "str"
        assert doc["options"]["host_group"].get("required") is not True

    def test_reassociate_is_bool_default_false(self):
        doc = _load_doc()
        opt = doc["options"]["reassociate"]
        assert opt["type"] == "bool"
        assert opt["default"] is False

    def test_extends_scvmm_connection_fragment(self):
        doc = _load_doc()
        assert "microsoft.scvmm.scvmm_connection" in doc["extends_documentation_fragment"]

    def test_version_added(self):
        doc = _load_doc()
        assert doc.get("version_added") is not None

    def test_all_options_have_type(self):
        doc = _load_doc()
        for opt_name, opt_def in doc["options"].items():
            assert "type" in opt_def, f"Option {opt_name!r} missing type"
