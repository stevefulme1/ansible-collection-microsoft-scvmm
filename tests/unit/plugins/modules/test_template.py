# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for scvmm_template module documentation stub."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
import yaml

from conftest import (
    SENSITIVE_PARAM_PATTERNS,
    load_module_doc,
    parse_documentation,
)

MODULE = "scvmm_template"


@pytest.fixture(scope="module")
def module_docs():
    return load_module_doc(MODULE)


@pytest.fixture(scope="module")
def parsed_doc(module_docs):
    raw_doc, _, _ = module_docs
    assert raw_doc is not None
    return parse_documentation(raw_doc)


class TestDocumentation:
    def test_documentation_is_valid_yaml(self, module_docs):
        raw_doc, _, _ = module_docs
        doc = yaml.safe_load(raw_doc)
        assert isinstance(doc, dict)

    def test_module_name_matches(self, parsed_doc):
        assert parsed_doc["module"] == MODULE

    def test_short_description_present(self, parsed_doc):
        assert len(parsed_doc["short_description"]) > 0

    def test_extends_documentation_fragment(self, parsed_doc):
        fragments = parsed_doc.get("extends_documentation_fragment", [])
        assert any("scvmm_connection" in f for f in fragments)


class TestArgumentSpec:
    def test_name_option_required(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "name" in opts
        assert opts["name"].get("required") is True

    def test_state_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "state" in opts
        assert set(opts["state"]["choices"]) == {"present", "absent"}

    def test_source_vm_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "source_vm" in opts
        assert opts["source_vm"]["type"] == "str"

    def test_vhd_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "vhd" in opts

    def test_library_server_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "library_server" in opts

    def test_cpu_count_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "cpu_count" in opts
        assert opts["cpu_count"]["type"] == "int"

    def test_memory_mb_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "memory_mb" in opts
        assert opts["memory_mb"]["type"] == "int"

    def test_os_type_option(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        assert "os_type" in opts


class TestReturn:
    def test_return_section_exists(self, module_docs):
        _, _, returns = module_docs
        assert returns is not None

    def test_return_is_valid_yaml(self, module_docs):
        _, _, returns = module_docs
        parsed = yaml.safe_load(returns)
        assert isinstance(parsed, dict)

    def test_return_has_template_key(self, module_docs):
        _, _, returns = module_docs
        parsed = yaml.safe_load(returns)
        assert "template" in parsed


class TestExamples:
    def test_examples_section_exists(self, module_docs):
        _, examples, _ = module_docs
        assert examples is not None

    def test_examples_is_valid_yaml(self, module_docs):
        _, examples, _ = module_docs
        parsed = yaml.safe_load(examples)
        assert isinstance(parsed, list)
        assert len(parsed) > 0

    def test_examples_contain_module_name(self, module_docs):
        _, examples, _ = module_docs
        assert MODULE in examples


class TestSecurity:
    def test_no_log_on_sensitive_fields(self, parsed_doc):
        opts = parsed_doc.get("options", {})
        for opt_name, opt_spec in opts.items():
            for pattern in SENSITIVE_PARAM_PATTERNS:
                if pattern in opt_name.lower():
                    assert opt_spec.get("no_log") is True, (
                        f"Option '{opt_name}' looks sensitive but lacks no_log: true"
                    )
