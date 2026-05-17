#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_state
short_description: Manage the power state of an SCVMM virtual machine
description:
  - Start, stop, pause, resume, or restart a virtual machine in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the virtual machine.
    type: str
    required: true
  state:
    description:
      - Desired power state.
    type: str
    required: true
    choices: [started, stopped, paused, saved, restarted]
  force:
    description:
      - Force the power state change without waiting for guest OS.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Start a VM
  microsoft.scvmm.scvmm_vm_state:
    scvmm_server: scvmm01.example.com
    name: web-server-01
    state: started

- name: Gracefully stop a VM
  microsoft.scvmm.scvmm_vm_state:
    scvmm_server: scvmm01.example.com
    name: web-server-01
    state: stopped

- name: Force stop a VM
  microsoft.scvmm.scvmm_vm_state:
    scvmm_server: scvmm01.example.com
    name: web-server-01
    state: stopped
    force: true
"""

RETURN = r"""
status:
  description: The resulting power state of the VM.
  returned: always
  type: str
  sample: Running
"""
