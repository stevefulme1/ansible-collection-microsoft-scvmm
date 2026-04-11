#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_service_template_info
short_description: Gather information about SCVMM service templates
description:
  - Retrieve details of service templates in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific service template. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all service templates
  microsoft.scvmm.scvmm_service_template_info:
    scvmm_server: scvmm01.example.com
  register: service_templates

- name: Get a specific service template
  microsoft.scvmm.scvmm_service_template_info:
    scvmm_server: scvmm01.example.com
    name: Three-Tier-App
  register: template
"""

RETURN = r"""
templates:
  description: List of service template dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: Three-Tier-App
      description: Three-tier web application template
      release: "1.0.0"
"""
