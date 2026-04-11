#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_logical_network_info
short_description: Gather information about SCVMM logical networks
description:
  - Retrieve details of logical networks in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific logical network. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all logical networks
  microsoft.scvmm.scvmm_logical_network_info:
    scvmm_server: scvmm01.example.com
  register: networks
"""

RETURN = r"""
logical_networks:
  description: List of logical network dictionaries.
  returned: always
  type: list
  elements: dict
"""
