#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_dvd_drive_info
short_description: Gather information about virtual DVD drives on SCVMM VMs
description:
  - Retrieve details of virtual DVD drives and ISO mounts on virtual machines in SCVMM.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: List all DVD drives on a VM
  stevefulme1.scvmm.scvmm_vm_dvd_drive_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: dvd_drives

- name: List DVD drives using WinRM credentials
  stevefulme1.scvmm.scvmm_vm_dvd_drive_info:
    scvmm_server: scvmm01.example.com
    scvmm_username: svc_ansible@contoso.com
    scvmm_password: "{{ vault_scvmm_password }}"
    vm_name: web-server-01
  register: dvd_drives
"""

RETURN = r"""
dvd_drives:
  description: List of virtual DVD drive dictionaries.
  returned: always
  type: list
  elements: dict
  contains:
    vm_name:
      description: Name of the virtual machine.
      type: str
    bus:
      description: Bus number for the DVD drive.
      type: int
    lun:
      description: LUN number for the DVD drive on the specified bus.
      type: int
    iso:
      description: Path to the mounted ISO image, if any.
      type: str
    iso_name:
      description: Name of the mounted ISO image, if any.
      type: str
"""
