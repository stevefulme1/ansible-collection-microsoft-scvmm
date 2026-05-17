#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_physical_computer_profile
short_description: Manage bare metal deployment profiles in SCVMM
description:
  - Create, modify, and remove physical computer profiles used for bare metal host provisioning.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the physical computer profile.
    type: str
    required: true
  state:
    description:
      - Desired state of the profile.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the profile.
    type: str
  operating_system:
    description:
      - Operating system to deploy on bare metal hosts.
    type: str
  hardware_profile:
    description:
      - Hardware profile to associate with the deployment.
    type: str
  host_group:
    description:
      - Host group where provisioned hosts will be placed.
    type: str
  computer_access_credential:
    description:
      - Credential name or run-as account for accessing the provisioned computer.
    type: str
"""

EXAMPLES = r"""
- name: Create a bare metal deployment profile
  microsoft.scvmm.scvmm_physical_computer_profile:
    scvmm_server: scvmm01.example.com
    name: HyperV-Server-2025
    description: Standard Hyper-V host deployment
    operating_system: Windows Server 2025 Datacenter
    hardware_profile: Standard-2Socket
    host_group: All Hosts\\Production
    computer_access_credential: deploy-runas

- name: Remove a deployment profile
  microsoft.scvmm.scvmm_physical_computer_profile:
    scvmm_server: scvmm01.example.com
    name: HyperV-Server-2025
    state: absent
"""

RETURN = r"""
profile:
  description: Physical computer profile details.
  returned: when state is present
  type: dict
"""
