#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_port_classification_info
short_description: Gather information about SCVMM port classifications
description:
  - Retrieve details of port classifications in SCVMM.
  - Port classifications label virtual network adapter policies for use in VM templates and logical switches.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific port classification. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all port classifications
  microsoft.scvmm.scvmm_port_classification_info:
    scvmm_server: scvmm01.example.com
  register: classifications

- name: Get a specific port classification
  microsoft.scvmm.scvmm_port_classification_info:
    scvmm_server: scvmm01.example.com
    name: High Performance
  register: hp_class
"""

RETURN = r"""
classifications:
  description: List of port classification dictionaries.
  returned: always
  type: list
  elements: dict
"""
