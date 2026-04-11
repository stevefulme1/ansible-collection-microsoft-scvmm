#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_port_classification
short_description: Manage SCVMM port classifications
description:
  - Create and remove port classifications in SCVMM.
  - Port classifications define network policies applied to virtual network adapters.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the port classification.
    type: str
    required: true
  state:
    description:
      - Desired state of the port classification.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the port classification.
    type: str
"""

EXAMPLES = r"""
- name: Create a port classification
  microsoft.scvmm.scvmm_port_classification:
    scvmm_server: scvmm01.example.com
    name: High-Bandwidth
    description: Port classification for high-bandwidth workloads

- name: Remove a port classification
  microsoft.scvmm.scvmm_port_classification:
    scvmm_server: scvmm01.example.com
    name: High-Bandwidth
    state: absent
"""

RETURN = r"""
port_classification:
  description: Port classification details.
  returned: when state is present
  type: dict
  sample:
    name: High-Bandwidth
    description: Port classification for high-bandwidth workloads
"""
