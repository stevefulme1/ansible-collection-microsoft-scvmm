#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_disk
short_description: Manage virtual hard disk attachments on SCVMM VMs
description:
  - Attach and detach virtual hard disks to/from virtual machines in SCVMM.
  - Manages the SCSI or IDE bus/LUN assignment for the disk.
version_added: "0.1.0"
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
  vhd_name:
    description:
      - Name of the virtual hard disk to attach or detach.
    type: str
    required: true
  state:
    description:
      - Desired state of the disk attachment.
    type: str
    choices: [attached, detached]
    default: attached
  bus_type:
    description:
      - Bus type for the disk attachment.
    type: str
    choices: [SCSI, IDE]
    default: SCSI
  bus:
    description:
      - Bus number for the disk.
    type: int
    default: 0
  lun:
    description:
      - LUN number for the disk on the specified bus.
    type: int
"""

EXAMPLES = r"""
- name: Attach a VHD to a VM
  microsoft.scvmm.scvmm_vm_disk:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    vhd_name: data-disk-01
    bus_type: SCSI
    bus: 0
    lun: 1

- name: Detach a VHD from a VM
  microsoft.scvmm.scvmm_vm_disk:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    vhd_name: data-disk-01
    state: detached
"""

RETURN = r"""
disk_attachment:
  description: Disk attachment details.
  returned: when state is attached
  type: dict
  sample:
    vm_name: web-server-01
    vhd_name: data-disk-01
    bus_type: SCSI
    bus: 0
    lun: 1
"""
