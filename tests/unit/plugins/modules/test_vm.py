# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for scvmm_vm module documentation stub."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
import yaml

from conftest import (
    SENSITIVE_PARAM_PATTERNS,
    load_module_doc,
    parse_documentation,
)

MODULE = "scvmm_vm"


@pytest.fixture(scope="module")
def module_docs():
    return load_module_doc(MODULE)


@pytest.fixture(scope="module")
def parsed_doc(module_docs):
    raw_doc, _, _ = module_docs
    assert raw_doc is not None, f"{MODULE}: DOCUMENTATION string is missing"
    return parse_documentation(raw_doc)


# -- DOCUMENTATION -----------------------------------------------------------


class TestDocumentation:
    def test_documentation_is_valid_yaml(self, module_docs):
        raw_doc, _, _ = module_docs
        assert raw_doc is not None
        doc = yaml.safe_load(raw_doc)
        assert isinstance(doc, dict)

    def test_module_name_matches(self, parsed_doc):
        assert parsed_doc["module"] == MODULE

    def test_short_description_present(self, parsed_doc):
        assert "short_description" in parsed_doc
        assert len(parsed_doc["short_description"]) > 0

    def test_description_present(self, parsed_doc):
        assert "description" in parsed_doc

    def test_version_added(self, parsed_doc):
        assert "version_added" in parsed_doc

    def test_author_present(self, parsed_doc):
        assert "author" in parsed_doc
        assert len(parsed_doc["author"]) > 0

    def test_extends_documentation_fragment(self, parsed_doc):
        assert "extends_documentation_fragment" in parsed_doc
        fragments = parsed_doc["extends_documentation_fragment"]
        assert any("scvmm_connection" in f for f in fragments)


# -- argument_spec (options) -------------------------------------------------


class TestArgumentSpec:
    def test_name_option_required(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "name" in opts, "Missing required option: name"
        assert opts["name"].get("required") is True

    def test_name_option_type_str(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert opts["name"]["type"] == "str"

    def test_state_option_present(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "state" in opts
        assert set(opts["state"]["choices"]) == {"present", "absent"}
        assert opts["state"]["default"] == "present"

    def test_template_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "template" in opts
        assert opts["template"]["type"] == "str"

    def test_cloud_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "cloud" in opts

    def test_cpu_count_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "cpu_count" in opts
        assert opts["cpu_count"]["type"] == "int"

    def test_memory_mb_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "memory_mb" in opts
        assert opts["memory_mb"]["type"] == "int"

    def test_start_action_choices(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "start_action" in opts
        assert "NeverAutoTurnOnVM" in opts["start_action"]["choices"]

    def test_stop_action_choices(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "stop_action" in opts
        assert "ShutdownGuestOS" in opts["stop_action"]["choices"]


# -- RETURN ------------------------------------------------------------------


class TestReturn:
    def test_return_section_exists(self, module_docs):
        _, _, returns = module_docs
        assert returns is not None, f"{MODULE}: RETURN string is missing"

    def test_return_is_valid_yaml(self, module_docs):
        _, _, returns = module_docs
        parsed = yaml.safe_load(returns)
        assert isinstance(parsed, dict)

    def test_return_has_vm_key(self, module_docs):
        _, _, returns = module_docs
        parsed = yaml.safe_load(returns)
        assert "vm" in parsed


# -- EXAMPLES ----------------------------------------------------------------


class TestExamples:
    def test_examples_section_exists(self, module_docs):
        _, examples, _ = module_docs
        assert examples is not None, f"{MODULE}: EXAMPLES string is missing"

    def test_examples_is_valid_yaml(self, module_docs):
        _, examples, _ = module_docs
        parsed = yaml.safe_load(examples)
        assert isinstance(parsed, list)
        assert len(parsed) > 0

    def test_examples_contain_module_name(self, module_docs):
        _, examples, _ = module_docs
        assert MODULE in examples


# -- Security ----------------------------------------------------------------


class TestSecurity:
    def test_no_log_on_sensitive_fields(self, parsed_doc):
        """Any option whose name contains a sensitive pattern must have no_log."""
        opts = parsed_doc.get("options", {})
        for opt_name, opt_spec in opts.items():
            for pattern in SENSITIVE_PARAM_PATTERNS:
                if pattern in opt_name.lower():
                    assert opt_spec.get("no_log") is True, (
                        f"Option '{opt_name}' looks sensitive but lacks no_log: true"
                    )
