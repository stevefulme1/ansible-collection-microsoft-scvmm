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
  - stevefulme1.svcmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific cloud. Omit to list all clouds.
    type: str
"""

EXAMPLES = r"""
- name: List all clouds
  stevefulme1.svcmm.scvmm_cloud_info:
    scvmm_server: scvmm01.example.com
  register: clouds

- name: Get details of a specific cloud
  stevefulme1.svcmm.scvmm_cloud_info:
    scvmm_server: scvmm01.example.com
    name: Production Cloud
  register: prod_cloud

- name: List clouds using WinRM credentials
  stevefulme1.svcmm.scvmm_cloud_info:
    scvmm_server: scvmm01.example.com
    scvmm_username: svc_ansible@contoso.com
    scvmm_password: "{{ vault_scvmm_password }}"
  register: clouds
"""

RETURN = r"""
clouds:
  description: List of cloud dictionaries.
  returned: always
  type: list
  elements: dict
"""
