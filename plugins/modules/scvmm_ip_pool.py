#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_ip_pool
short_description: Manage SCVMM static IP address pools
description:
  - Create, modify, and remove static IP address pools in SCVMM.
  - IP pools are associated with logical network definitions.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the IP pool.
    type: str
    required: true
  state:
    description:
      - Desired state of the IP pool.
    type: str
    choices: [present, absent]
    default: present
  logical_network:
    description:
      - Name of the logical network this pool belongs to.
      - Required when I(state=present).
    type: str
  subnet:
    description:
      - IP subnet in CIDR notation (e.g. C(192.168.1.0/24)).
      - Required when I(state=present).
    type: str
  ip_range_start:
    description:
      - Start of the IP address range.
    type: str
  ip_range_end:
    description:
      - End of the IP address range.
    type: str
  gateway:
    description:
      - Default gateway address.
    type: list
    elements: str
  dns_servers:
    description:
      - List of DNS server addresses.
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: Create an IP pool
  microsoft.scvmm.scvmm_ip_pool:
    scvmm_server: scvmm01.example.com
    name: Prod-Pool
    logical_network: Corp-Network
    subnet: 192.168.1.0/24
    ip_range_start: 192.168.1.100
    ip_range_end: 192.168.1.200
    gateway:
      - 192.168.1.1
    dns_servers:
      - 10.0.0.1
      - 10.0.0.2

- name: Remove an IP pool
  microsoft.scvmm.scvmm_ip_pool:
    scvmm_server: scvmm01.example.com
    name: Prod-Pool
    state: absent
"""

RETURN = r"""
ip_pool:
  description: IP pool details.
  returned: when state is present
  type: dict
  sample:
    name: Prod-Pool
    subnet: 192.168.1.0/24
    ip_range_start: 192.168.1.100
    ip_range_end: 192.168.1.200
"""
