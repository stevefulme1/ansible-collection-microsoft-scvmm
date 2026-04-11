#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_storage_classification
short_description: Manage SCVMM storage classifications
description:
  - Create and remove storage classifications in SCVMM.
  - Storage classifications categorize storage for use in clouds and templates.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the storage classification.
    type: str
    required: true
  state:
    description:
      - Desired state of the storage classification.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the storage classification.
    type: str
"""

EXAMPLES = r"""
- name: Create a storage classification
  microsoft.scvmm.scvmm_storage_classification:
    scvmm_server: scvmm01.example.com
    name: Gold-Storage
    description: High-performance SSD storage

- name: Remove a storage classification
  microsoft.scvmm.scvmm_storage_classification:
    scvmm_server: scvmm01.example.com
    name: Gold-Storage
    state: absent
"""

RETURN = r"""
storage_classification:
  description: Storage classification details.
  returned: when state is present
  type: dict
  sample:
    name: Gold-Storage
    description: High-performance SSD storage
"""
