#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_cloud_info
short_description: Gather information about SCVMM clouds
description:
  - Retrieve details of private clouds in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific cloud. Omit to list all clouds.
    type: str
"""

EXAMPLES = r"""
- name: List all clouds
  microsoft.scvmm.scvmm_cloud_info:
    scvmm_server: scvmm01.example.com
  register: clouds
"""

RETURN = r"""
clouds:
  description: List of cloud dictionaries.
  returned: always
  type: list
  elements: dict
"""
