#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_load_balancer
short_description: Manage SCVMM load balancers
description:
  - Register, modify, and remove load balancers in SCVMM.
  - Load balancers provide network traffic distribution for services managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the load balancer.
    type: str
    required: true
  state:
    description:
      - Desired state of the load balancer.
    type: str
    choices: [present, absent]
    default: present
  address:
    description:
      - IP address or FQDN of the load balancer.
      - Required when I(state=present).
    type: str
  port:
    description:
      - Management port of the load balancer.
    type: int
  manufacturer:
    description:
      - Manufacturer of the load balancer (e.g. C(F5), C(Citrix)).
    type: str
  model:
    description:
      - Model of the load balancer.
    type: str
  credential:
    description:
      - Name of the SCVMM Run As account to use for load balancer authentication.
    type: str
"""

EXAMPLES = r"""
- name: Register a load balancer
  microsoft.scvmm.scvmm_load_balancer:
    scvmm_server: scvmm01.example.com
    name: Prod-LB-01
    address: lb01.example.com
    port: 443
    manufacturer: F5
    model: BIG-IP
    credential: LB-RunAs

- name: Remove a load balancer
  microsoft.scvmm.scvmm_load_balancer:
    scvmm_server: scvmm01.example.com
    name: Prod-LB-01
    state: absent
"""

RETURN = r"""
load_balancer:
  description: Load balancer details.
  returned: when state is present
  type: dict
  sample:
    name: Prod-LB-01
    address: lb01.example.com
    port: 443
    manufacturer: F5
    model: BIG-IP
"""
