#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_rating_info
short_description: Get host placement ratings for VM deployment in SCVMM
description:
  - Retrieve placement ratings that rank Hyper-V hosts for deploying a virtual machine.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of an existing virtual machine to evaluate placement for.
      - At least one of I(vm_name), I(template), or I(hardware_profile) is required.
    type: str
  template:
    description:
      - Name of the VM template to evaluate placement for.
      - At least one of I(vm_name), I(template), or I(hardware_profile) is required.
    type: str
  hardware_profile:
    description:
      - Name of the hardware profile to evaluate placement for.
      - At least one of I(vm_name), I(template), or I(hardware_profile) is required.
    type: str
  host_group:
    description:
      - Host group path to limit rating evaluation to.
    type: str
"""

EXAMPLES = r"""
- name: Get host ratings for a VM template
  microsoft.scvmm.scvmm_host_rating_info:
    scvmm_server: scvmm01.example.com
    template: Windows2022-Standard
    host_group: All Hosts\\Production
  register: ratings

- name: Get host ratings for an existing VM
  microsoft.scvmm.scvmm_host_rating_info:
    scvmm_server: scvmm01.example.com
    vm_name: webserver01
  register: ratings

- name: Get host ratings using a hardware profile
  microsoft.scvmm.scvmm_host_rating_info:
    scvmm_server: scvmm01.example.com
    hardware_profile: 4CPU-8GB
  register: ratings
"""

RETURN = r"""
ratings:
  description: List of host rating dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - host_name: hyperv01.example.com
      rating: 5
    - host_name: hyperv02.example.com
      rating: 3
"""
