#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_baseline_info
short_description: Gather information about SCVMM update baselines
description:
  - Retrieve details of update baselines configured in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific baseline. Omit to list all baselines.
    type: str
"""

EXAMPLES = r"""
- name: List all baselines
  microsoft.scvmm.scvmm_baseline_info:
    scvmm_server: scvmm01.example.com
  register: baselines

- name: Get a specific baseline
  microsoft.scvmm.scvmm_baseline_info:
    scvmm_server: scvmm01.example.com
    name: Security Updates Q1
  register: baseline
"""

RETURN = r"""
baselines:
  description: List of baseline dictionaries.
  returned: always
  type: list
  elements: dict
"""
