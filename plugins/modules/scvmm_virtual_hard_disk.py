#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_virtual_hard_disk
short_description: Manage SCVMM virtual hard disks
description:
  - Create and remove virtual hard disks (VHD/VHDX) in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the virtual hard disk.
    type: str
    required: true
  state:
    description:
      - Desired state of the VHD.
    type: str
    choices: [present, absent]
    default: present
  path:
    description:
      - Path on the library server or host where the VHD is stored.
    type: str
  size_gb:
    description:
      - Size of the VHD in gigabytes.
      - Required when creating a new VHD.
    type: int
  disk_type:
    description:
      - Type of virtual hard disk.
    type: str
    choices: [Dynamic, Fixed]
    default: Dynamic
  format:
    description:
      - VHD format.
    type: str
    choices: [VHD, VHDX]
    default: VHDX
"""

EXAMPLES = r"""
- name: Create a dynamic VHDX
  microsoft.scvmm.scvmm_virtual_hard_disk:
    scvmm_server: scvmm01.example.com
    name: data-disk-01
    size_gb: 100
    disk_type: Dynamic
    format: VHDX
"""

RETURN = r"""
virtual_hard_disk:
  description: VHD details.
  returned: when state is present
  type: dict
"""
