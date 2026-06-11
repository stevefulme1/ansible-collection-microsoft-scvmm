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
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific load balancer. Omit to list all load balancers.
    type: str
"""

EXAMPLES = r"""
- name: List all load balancers
  stevefulme1.scvmm.scvmm_load_balancer_info:
    scvmm_server: scvmm01.example.com
  register: load_balancers

- name: Get details of a specific load balancer
  stevefulme1.scvmm.scvmm_load_balancer_info:
    scvmm_server: scvmm01.example.com
    name: Prod-LB-01
  register: lb_info

- name: List load balancers using WinRM credentials
  stevefulme1.scvmm.scvmm_load_balancer_info:
    scvmm_server: scvmm01.example.com
    scvmm_username: svc_ansible@contoso.com
    scvmm_password: "{{ vault_scvmm_password }}"
  register: load_balancers
"""

RETURN = r"""
load_balancers:
  description: List of load balancer dictionaries.
  returned: always
  type: list
  elements: dict
  contains:
    name:
      description: Name of the load balancer.
      type: str
    address:
      description: IP address or FQDN of the load balancer.
      type: str
    port:
      description: Management port of the load balancer.
      type: int
    manufacturer:
      description: Manufacturer of the load balancer.
      type: str
    model:
      description: Model of the load balancer.
      type: str
    credential:
      description: Name of the SCVMM Run As account.
      type: str
"""
