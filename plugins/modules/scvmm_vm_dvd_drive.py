#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_dvd_drive
short_description: Manage virtual DVD drives and ISO mounts on SCVMM VMs
description:
  - Add, configure, and remove virtual DVD drives on virtual machines in SCVMM.
  - Mount and unmount ISO images to virtual DVD drives.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine.
    type: str
    required: true
  state:
    description:
      - Desired state of the virtual DVD drive.
    type: str
    choices: [present, absent]
    default: present
  iso:
    description:
      - Path to the ISO image in the SCVMM library to mount.
      - Omit to create an empty DVD drive or to unmount.
    type: str
  bus:
    description:
      - Bus number for the DVD drive.
    type: int
    default: 0
  lun:
    description:
      - LUN number for the DVD drive on the specified bus.
    type: int
    default: 0
"""

EXAMPLES = r"""
- name: Add a DVD drive with an ISO mounted
  microsoft.scvmm.scvmm_vm_dvd_drive:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    iso: "WindowsServer2022.iso"
    bus: 0
    lun: 0

- name: Add an empty DVD drive
  microsoft.scvmm.scvmm_vm_dvd_drive:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    bus: 0
    lun: 1

- name: Remove a DVD drive
  microsoft.scvmm.scvmm_vm_dvd_drive:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    state: absent
    bus: 0
    lun: 1
"""

RETURN = r"""
dvd_drive:
  description: Details of the virtual DVD drive.
  returned: when state is present
  type: dict
  sample:
    vm_name: web-server-01
    bus: 0
    lun: 0
    iso: WindowsServer2022.iso
changed:
  description: Whether the DVD drive was created, modified, or removed.
  returned: always
  type: bool
"""
