#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_network_adapter_info
short_description: Gather information about host network adapters in SCVMM
description:
  - Retrieve details of physical network adapters on a Hyper-V host managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_host:
    description:
      - FQDN of the Hyper-V host to query for network adapters.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: List all network adapters on a host
  microsoft.scvmm.scvmm_host_network_adapter_info:
    scvmm_server: scvmm01.example.com
    vm_host: hyperv01.example.com
  register: adapters
"""

RETURN = r"""
adapters:
  description: List of network adapter dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Ethernet1
      mac_address: "00:15:5D:01:02:03"
      logical_network: Management
      connection_state: Connected
"""
