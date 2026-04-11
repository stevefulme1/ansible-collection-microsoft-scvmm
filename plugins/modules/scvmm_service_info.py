#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_service_info
short_description: Gather information about SCVMM service instances
description:
  - Retrieve details of deployed service instances in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific service instance. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all service instances
  microsoft.scvmm.scvmm_service_info:
    scvmm_server: scvmm01.example.com
  register: services

- name: Get a specific service instance
  microsoft.scvmm.scvmm_service_info:
    scvmm_server: scvmm01.example.com
    name: prod-web-app
  register: service
"""

RETURN = r"""
services:
  description: List of service instance dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: prod-web-app
      status: Running
      service_template: Three-Tier-App
      cloud: Production-Cloud
"""
