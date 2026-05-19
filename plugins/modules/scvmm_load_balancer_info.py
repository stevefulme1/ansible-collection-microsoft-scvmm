#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_load_balancer_info
short_description: Gather information about SCVMM load balancers
description:
  - Retrieve details of load balancers registered in SCVMM.
  - Can filter by name to retrieve a specific load balancer.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific load balancer. Omit to list all.
    type: str
  manufacturer:
    description:
      - Filter load balancers by manufacturer (e.g. C(F5), C(Citrix)).
    type: str
"""

EXAMPLES = r"""
- name: List all load balancers
  stevefulme1.scvmm.scvmm_load_balancer_info:
    scvmm_server: scvmm01.example.com
  register: load_balancers

- name: Get a specific load balancer
  stevefulme1.scvmm.scvmm_load_balancer_info:
    scvmm_server: scvmm01.example.com
    name: Prod-LB-01
  register: lb

- name: Filter load balancers by manufacturer
  stevefulme1.scvmm.scvmm_load_balancer_info:
    scvmm_server: scvmm01.example.com
    manufacturer: F5
  register: f5_lbs
"""

RETURN = r"""
load_balancers:
  description: List of load balancer dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Prod-LB-01
      address: lb01.example.com
      port: 443
      manufacturer: F5
      model: BIG-IP
      state: Responding
"""
