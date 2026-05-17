#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_cloud
short_description: Manage SCVMM clouds
description:
  - Create, modify, and remove private clouds in SCVMM.
  - Clouds are resource pools that abstract compute, network, and storage.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the cloud.
    type: str
    required: true
  state:
    description:
      - Desired state of the cloud.
    type: str
    choices: [present, absent]
    default: present
  host_group:
    description:
      - Host group to associate with the cloud.
    type: str
  description:
    description:
      - Description of the cloud.
    type: str
"""

EXAMPLES = r"""
- name: Create a cloud
  microsoft.scvmm.scvmm_cloud:
    scvmm_server: scvmm01.example.com
    name: Production
    host_group: All Hosts\\Production
    description: Production workloads

- name: Remove a cloud
  microsoft.scvmm.scvmm_cloud:
    scvmm_server: scvmm01.example.com
    name: Production
    state: absent
"""

RETURN = r"""
cloud:
  description: Cloud details.
  returned: when state is present
  type: dict
"""
