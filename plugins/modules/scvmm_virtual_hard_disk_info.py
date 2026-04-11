#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_virtual_hard_disk_info
short_description: Gather information about SCVMM virtual hard disks
description:
  - Retrieve details of virtual hard disks (VHD/VHDX) in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific VHD. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all virtual hard disks
  microsoft.scvmm.scvmm_virtual_hard_disk_info:
    scvmm_server: scvmm01.example.com
  register: vhds

- name: Get a specific VHD
  microsoft.scvmm.scvmm_virtual_hard_disk_info:
    scvmm_server: scvmm01.example.com
    name: data-disk-01
  register: vhd
"""

RETURN = r"""
virtual_hard_disks:
  description: List of VHD dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: data-disk-01
      size_gb: 100
      disk_type: Dynamic
      format: VHDX
"""
