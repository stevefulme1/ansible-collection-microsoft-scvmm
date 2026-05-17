#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_baseline
short_description: Manage SCVMM update baselines
description:
  - Create, modify, and remove update baselines used for compliance management in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the update baseline.
    type: str
    required: true
  state:
    description:
      - Desired state of the baseline.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the baseline.
    type: str
  updates:
    description:
      - List of KB article IDs to include in the baseline.
    type: list
    elements: str
  scope:
    description:
      - Scope of the baseline assignment.
    type: str
    choices: [Host, Cluster, VMHost]
"""

EXAMPLES = r"""
- name: Create an update baseline
  microsoft.scvmm.scvmm_baseline:
    scvmm_server: scvmm01.example.com
    name: Security Updates Q1
    description: Quarterly security updates
    updates:
      - KB5012345
      - KB5012346
    scope: Host

- name: Remove a baseline
  microsoft.scvmm.scvmm_baseline:
    scvmm_server: scvmm01.example.com
    name: Security Updates Q1
    state: absent
"""

RETURN = r"""
baseline:
  description: Baseline details.
  returned: when state is present
  type: dict
"""
