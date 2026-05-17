#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_network_adapter
short_description: Configure host physical network adapters in SCVMM
description:
  - Configure physical network adapters on Hyper-V hosts managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_host:
    description:
      - FQDN of the Hyper-V host that owns the adapter.
    type: str
    required: true
  name:
    description:
      - Name of the physical network adapter to configure.
    type: str
    required: true
  logical_network:
    description:
      - Logical network to associate with the adapter.
    type: str
  uplink_port_profile:
    description:
      - Uplink port profile to assign to the adapter.
    type: str
"""

EXAMPLES = r"""
- name: Associate a NIC with a logical network
  microsoft.scvmm.scvmm_host_network_adapter:
    scvmm_server: scvmm01.example.com
    vm_host: hyperv01.example.com
    name: Ethernet1
    logical_network: Management

- name: Assign an uplink port profile to a NIC
  microsoft.scvmm.scvmm_host_network_adapter:
    scvmm_server: scvmm01.example.com
    vm_host: hyperv01.example.com
    name: Ethernet2
    logical_network: Tenant
    uplink_port_profile: UplinkProfile-Tenant
"""

RETURN = r"""
adapter:
  description: Network adapter details after configuration.
  returned: always
  type: dict
"""
