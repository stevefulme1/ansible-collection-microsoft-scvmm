#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_checkpoint
short_description: Manage SCVMM virtual machine checkpoints
description:
  - Create, delete, and restore virtual machine checkpoints (snapshots) in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine.
    type: str
    required: true
  name:
    description:
      - Name of the checkpoint.
    type: str
  state:
    description:
      - Desired state of the checkpoint.
    type: str
    choices: [present, absent, restored]
    default: present
  description:
    description:
      - Description for the checkpoint.
    type: str
"""

EXAMPLES = r"""
- name: Create a checkpoint
  microsoft.scvmm.scvmm_vm_checkpoint:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: pre-upgrade
    description: Before applying patches

- name: Restore a checkpoint
  microsoft.scvmm.scvmm_vm_checkpoint:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: pre-upgrade
    state: restored

- name: Delete a checkpoint
  microsoft.scvmm.scvmm_vm_checkpoint:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: pre-upgrade
    state: absent
"""

RETURN = r"""
checkpoint:
  description: Checkpoint details.
  returned: when state is present
  type: dict
  sample:
    name: pre-upgrade
    description: Before applying patches
    created: "2026-04-11T10:30:00"
"""
