#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_storage_classification_info
short_description: Gather information about SCVMM storage classifications
description:
  - Retrieve details of storage classifications defined in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific storage classification. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all storage classifications
  microsoft.scvmm.scvmm_storage_classification_info:
    scvmm_server: scvmm01.example.com
  register: classifications

- name: Get a specific storage classification
  microsoft.scvmm.scvmm_storage_classification_info:
    scvmm_server: scvmm01.example.com
    name: Gold-Storage
  register: gold_class
"""

RETURN = r"""
classifications:
  description: List of storage classification dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Gold-Storage
      description: High-performance SSD storage
"""
