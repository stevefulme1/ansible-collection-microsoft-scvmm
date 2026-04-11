#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_checkpoint_info
short_description: Gather information about SCVMM VM checkpoints
description:
  - Retrieve details of virtual machine checkpoints (snapshots) in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_name:
    description:
      - Name of the virtual machine to query checkpoints for.
    type: str
    required: true
  name:
    description:
      - Name of a specific checkpoint. Omit to list all checkpoints for the VM.
    type: str
"""

EXAMPLES = r"""
- name: List all checkpoints for a VM
  microsoft.scvmm.scvmm_vm_checkpoint_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
  register: checkpoints

- name: Get a specific checkpoint
  microsoft.scvmm.scvmm_vm_checkpoint_info:
    scvmm_server: scvmm01.example.com
    vm_name: web-server-01
    name: pre-upgrade
  register: checkpoint
"""

RETURN = r"""
checkpoints:
  description: List of checkpoint dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: pre-upgrade
      description: Before applying patches
      created: "2026-04-11T10:30:00"
"""
