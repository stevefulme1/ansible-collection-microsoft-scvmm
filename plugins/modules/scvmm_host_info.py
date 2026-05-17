#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_info
short_description: Gather information about SCVMM hosts
description:
  - Retrieve details of Hyper-V hosts managed by SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific host. Omit to list all hosts.
    type: str
  host_group:
    description:
      - Filter hosts by host group path.
    type: str
"""

EXAMPLES = r"""
- name: List all Hyper-V hosts
  microsoft.scvmm.scvmm_host_info:
    scvmm_server: scvmm01.example.com
  register: hosts

- name: Get hosts in a specific group
  microsoft.scvmm.scvmm_host_info:
    scvmm_server: scvmm01.example.com
    host_group: All Hosts\\Production-DC1
  register: prod_hosts
"""

RETURN = r"""
hosts:
  description: List of host dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: hyperv01.example.com
      status: Responding
      vm_count: 12
      host_group: Production-DC1
"""
