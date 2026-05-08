# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for the scvmm_vm module argument specification.

These tests validate the DOCUMENTATION string that defines the argument spec.
Actual CRUD logic lives in the companion PowerShell file and is exercised by
integration tests against a live SCVMM server.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib

import yaml


MODULE = "ansible_collections.microsoft.scvmm.plugins.modules.scvmm_vm"


def _load_doc():
    mod = importlib.import_module(MODULE)
    return yaml.safe_load(mod.DOCUMENTATION)


class TestScvmmVmArgSpec:
    """Validate the scvmm_vm DOCUMENTATION-based argument specification."""

    def test_module_has_documentation(self):
        mod = importlib.import_module(MODULE)
        assert hasattr(mod, "DOCUMENTATION"), "Module must define DOCUMENTATION"
        assert hasattr(mod, "EXAMPLES"), "Module must define EXAMPLES"
        assert hasattr(mod, "RETURN"), "Module must define RETURN"

    def test_documentation_is_valid_yaml(self):
        doc = _load_doc()
        assert isinstance(doc, dict)
        assert doc["module"] == "scvmm_vm"

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

    def test_state_type_is_str(self):
        doc = _load_doc()
        assert doc["options"]["state"]["type"] == "str"

    def test_cloud_and_vm_host_documented(self):
        """cloud and vm_host should both be optional str parameters."""
        doc = _load_doc()
        assert doc["options"]["cloud"]["type"] == "str"
        assert doc["options"]["vm_host"]["type"] == "str"
        # Neither should be required on its own
        assert doc["options"]["cloud"].get("required") is not True
        assert doc["options"]["vm_host"].get("required") is not True

    def test_vm_host_mutual_exclusivity_documented(self):
        """The description of vm_host should mention mutual exclusivity
        with cloud."""
        doc = _load_doc()
        desc = " ".join(doc["options"]["vm_host"]["description"])
        assert "cloud" in desc.lower(), (
            "vm_host description should reference mutual exclusivity with cloud"
        )

    def test_cpu_count_is_int(self):
        doc = _load_doc()
        assert doc["options"]["cpu_count"]["type"] == "int"

    def test_memory_mb_is_int(self):
        doc = _load_doc()
        assert doc["options"]["memory_mb"]["type"] == "int"

    def test_start_action_choices(self):
        doc = _load_doc()
        expected = {"NeverAutoTurnOnVM", "AlwaysAutoTurnOnVM",
                    "TurnOnVMIfRunningWhenVSStopped"}
        assert set(doc["options"]["start_action"]["choices"]) == expected

    def test_stop_action_choices(self):
        doc = _load_doc()
        expected = {"SaveVM", "TurnOffVM", "ShutdownGuestOS"}
        assert set(doc["options"]["stop_action"]["choices"]) == expected

    def test_template_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["template"]["type"] == "str"
        assert doc["options"]["template"].get("required") is not True

    def test_extends_scvmm_connection_fragment(self):
        doc = _load_doc()
        assert "microsoft.scvmm.scvmm_connection" in doc["extends_documentation_fragment"]

    def test_description_is_optional_str(self):
        doc = _load_doc()
        assert doc["options"]["description"]["type"] == "str"
        assert doc["options"]["description"].get("required") is not True
