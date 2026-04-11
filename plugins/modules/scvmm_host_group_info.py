#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_group_info
short_description: Gather information about SCVMM host groups
description:
  - Retrieve details of host groups in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific host group. Omit to list all.
    type: str
  path:
    description:
      - Full path of the host group (e.g. C(All Hosts\\Production)).
    type: str
"""

EXAMPLES = r"""
- name: List all host groups
  microsoft.scvmm.scvmm_host_group_info:
    scvmm_server: scvmm01.example.com
  register: host_groups

- name: Get a specific host group by path
  microsoft.scvmm.scvmm_host_group_info:
    scvmm_server: scvmm01.example.com
    path: All Hosts\Production
  register: prod_group
"""

RETURN = r"""
host_groups:
  description: List of host group dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Production
      path: All Hosts\Production
      host_count: 5
"""
