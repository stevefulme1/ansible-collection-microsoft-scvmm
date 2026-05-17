#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_template_info
short_description: Gather information about SCVMM VM templates
description:
  - Retrieve details of VM templates in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific template. Omit to list all templates.
    type: str
"""

EXAMPLES = r"""
- name: List all VM templates
  microsoft.scvmm.scvmm_template_info:
    scvmm_server: scvmm01.example.com
  register: templates

- name: Get details of a specific Windows template
  microsoft.scvmm.scvmm_template_info:
    scvmm_server: scvmm01.example.com
    name: Windows2022-Template
  register: win_template

- name: Get a Linux template using explicit credentials
  microsoft.scvmm.scvmm_template_info:
    scvmm_server: scvmm01.example.com
    scvmm_username: svc_ansible@contoso.com
    scvmm_password: "{{ vault_scvmm_password }}"
    name: Ubuntu2204-Template
  register: linux_template
"""

RETURN = r"""
templates:
  description: List of template dictionaries.
  returned: always
  type: list
  elements: dict
"""
