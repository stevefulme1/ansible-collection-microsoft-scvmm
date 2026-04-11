#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_service_template
short_description: Manage SCVMM service templates
description:
  - Create, modify, and remove service templates in SCVMM.
  - Service templates define multi-tier application deployments.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the service template.
    type: str
    required: true
  state:
    description:
      - Desired state of the service template.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the service template.
    type: str
  release:
    description:
      - Release version string for the service template.
    type: str
"""

EXAMPLES = r"""
- name: Create a service template
  microsoft.scvmm.scvmm_service_template:
    scvmm_server: scvmm01.example.com
    name: Three-Tier-App
    description: Three-tier web application template
    release: "1.0.0"

- name: Update service template release
  microsoft.scvmm.scvmm_service_template:
    scvmm_server: scvmm01.example.com
    name: Three-Tier-App
    release: "1.1.0"

- name: Remove a service template
  microsoft.scvmm.scvmm_service_template:
    scvmm_server: scvmm01.example.com
    name: Three-Tier-App
    state: absent
"""

RETURN = r"""
service_template:
  description: Service template details.
  returned: when state is present
  type: dict
  sample:
    name: Three-Tier-App
    description: Three-tier web application template
    release: "1.0.0"
"""
