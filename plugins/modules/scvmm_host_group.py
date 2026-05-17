#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_group
short_description: Manage SCVMM host groups
description:
  - Create, modify, and remove host groups in SCVMM.
  - Host groups are logical containers for Hyper-V hosts.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the host group.
    type: str
    required: true
  state:
    description:
      - Desired state of the host group.
    type: str
    choices: [present, absent]
    default: present
  parent:
    description:
      - Path to the parent host group.
      - Defaults to C(All Hosts) if not specified.
    type: str
    default: All Hosts
  description:
    description:
      - Description of the host group.
    type: str
"""

EXAMPLES = r"""
- name: Create a host group
  microsoft.scvmm.scvmm_host_group:
    scvmm_server: scvmm01.example.com
    name: Production-DC1
    parent: All Hosts
    description: Production hosts in DC1

- name: Create a nested host group
  microsoft.scvmm.scvmm_host_group:
    scvmm_server: scvmm01.example.com
    name: Web-Tier
    parent: All Hosts\\Production-DC1
"""

RETURN = r"""
host_group:
  description: Host group details.
  returned: when state is present
  type: dict
"""
