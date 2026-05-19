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
  - Retrieve details of virtual DVD drives attached to a virtual machine in SCVMM.
  - Returns bus/LUN assignment and mounted ISO information for each drive.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine to query DVD drives for.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: List all DVD drives on a VM
  stevefulme1.scvmm.scvmm_vm_dvd_drive_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: dvd_drives

- name: Check if any ISO is mounted
  stevefulme1.scvmm.scvmm_vm_dvd_drive_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: dvd_drives

- name: Display mounted ISOs
  ansible.builtin.debug:
    msg: "Drive bus {{ item.bus }} lun {{ item.lun }} has ISO {{ item.iso }}"
  loop: "{{ dvd_drives.dvd_drives | selectattr('iso', 'defined') }}"
"""

RETURN = r"""
dvd_drives:
  description: List of virtual DVD drive dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - vm_name: web-server-01
      bus: 0
      lun: 0
      iso: WindowsServer2022.iso
    - vm_name: web-server-01
      bus: 0
      lun: 1
      iso: null
"""
