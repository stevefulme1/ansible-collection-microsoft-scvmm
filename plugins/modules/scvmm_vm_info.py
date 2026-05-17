#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_info
short_description: Gather information about SCVMM virtual machines
description:
  - Retrieve details of virtual machines managed by SCVMM.
  - Can filter by name, cloud, host, or host group.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific VM to retrieve. Omit to list all VMs.
    type: str
  cloud:
    description:
      - Filter VMs by cloud name.
    type: str
  vm_host:
    description:
      - Filter VMs by Hyper-V host name.
    type: str
"""

EXAMPLES = r"""
- name: Get all VMs
  microsoft.scvmm.scvmm_vm_info:
    scvmm_server: scvmm01.example.com
  register: all_vms

- name: Get a specific VM
  microsoft.scvmm.scvmm_vm_info:
    scvmm_server: scvmm01.example.com
    name: web-server-01
  register: vm_details

- name: List VMs in a cloud
  microsoft.scvmm.scvmm_vm_info:
    scvmm_server: scvmm01.example.com
    cloud: Production
  register: prod_vms
"""

RETURN = r"""
vms:
  description: List of VM dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: web-server-01
      status: Running
      cpu_count: 4
      memory_mb: 8192
      cloud: Production
      host: hyperv01.example.com
"""
