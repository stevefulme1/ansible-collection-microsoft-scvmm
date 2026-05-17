#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_servicing_window_info
short_description: Gather information about SCVMM servicing windows
description:
  - Retrieve details of servicing windows configured in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific servicing window. Omit to list all servicing windows.
    type: str
"""

EXAMPLES = r"""
- name: List all servicing windows
  microsoft.scvmm.scvmm_servicing_window_info:
    scvmm_server: scvmm01.example.com
  register: windows

- name: Get a specific servicing window
  microsoft.scvmm.scvmm_servicing_window_info:
    scvmm_server: scvmm01.example.com
    name: Sunday Maintenance
  register: window
"""

RETURN = r"""
windows:
  description: List of servicing window dictionaries.
  returned: always
  type: list
  elements: dict
"""
