# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for the scvmm_template module argument specification."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib

import yaml


MODULE = "ansible_collections.microsoft.scvmm.plugins.modules.scvmm_template"


def _load_doc():
    mod = importlib.import_module(MODULE)
    return yaml.safe_load(mod.DOCUMENTATION)


class TestScvmmTemplateArgSpec:
    """Validate the scvmm_template DOCUMENTATION-based argument specification."""

    def test_module_has_documentation(self):
        mod = importlib.import_module(MODULE)
        assert hasattr(mod, "DOCUMENTATION")
        assert hasattr(mod, "EXAMPLES")
        assert hasattr(mod, "RETURN")

    def test_documentation_is_valid_yaml(self):
        doc = _load_doc()
        assert isinstance(doc, dict)
        assert doc["module"] == "scvmm_template"

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

    def test_source_vm_and_vhd_mutual_exclusivity_documented(self):
        """source_vm and vhd descriptions should mention mutual exclusivity."""
        doc = _load_doc()
        source_desc = " ".join(doc["options"]["source_vm"]["description"])
        vhd_desc = " ".join(doc["options"]["vhd"]["description"])
        assert "vhd" in source_desc.lower(), (
            "source_vm description should reference mutual exclusivity with vhd"
        )
        assert "source_vm" in vhd_desc.lower(), (
            "vhd description should reference mutual exclusivity with source_vm"
        )

    def test_source_vm_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["source_vm"]["type"] == "str"
        assert doc["options"]["source_vm"].get("required") is not True

    def test_vhd_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["vhd"]["type"] == "str"
        assert doc["options"]["vhd"].get("required") is not True

    def test_cpu_count_is_int(self):
        doc = _load_doc()
        assert doc["options"]["cpu_count"]["type"] == "int"

    def test_memory_mb_is_int(self):
        doc = _load_doc()
        assert doc["options"]["memory_mb"]["type"] == "int"

    def test_library_server_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["library_server"]["type"] == "str"

    def test_os_type_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["os_type"]["type"] == "str"

    def test_extends_scvmm_connection_fragment(self):
        doc = _load_doc()
        assert "microsoft.scvmm.scvmm_connection" in doc["extends_documentation_fragment"]
