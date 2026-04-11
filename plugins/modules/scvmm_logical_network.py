#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_logical_network
short_description: Manage SCVMM logical networks
description:
  - Create, modify, and remove logical networks in SCVMM.
  - Logical networks represent physical network infrastructure.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the logical network.
    type: str
    required: true
  state:
    description:
      - Desired state of the logical network.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the logical network.
    type: str
  network_virtualization_enabled:
    description:
      - Enable network virtualization on this logical network.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Create a logical network
  microsoft.scvmm.scvmm_logical_network:
    scvmm_server: scvmm01.example.com
    name: Corp-Network
    description: Corporate network backbone

- name: Remove a logical network
  microsoft.scvmm.scvmm_logical_network:
    scvmm_server: scvmm01.example.com
    name: Corp-Network
    state: absent
"""

RETURN = r"""
logical_network:
  description: Logical network details.
  returned: when state is present
  type: dict
"""
