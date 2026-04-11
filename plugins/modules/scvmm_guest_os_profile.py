#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_guest_os_profile
short_description: Manage SCVMM guest OS profiles
description:
  - Create, update, and remove guest OS profiles in SCVMM.
  - Guest OS profiles define operating system settings used during VM provisioning.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the guest OS profile.
    type: str
    required: true
  state:
    description:
      - Desired state of the guest OS profile.
    type: str
    choices: [present, absent]
    default: present
  operating_system:
    description:
      - Operating system identifier, such as C(Windows Server 2022 Datacenter) or C(CentOS Linux 8 (64 bit)).
    type: str
  computer_name_pattern:
    description:
      - Pattern used to generate computer names during deployment.
      - Supports SCVMM name patterns such as C(###) for sequential numbering.
    type: str
  admin_password:
    description:
      - Local administrator password for the guest OS.
    type: str
    no_log: true
  domain:
    description:
      - Active Directory domain to join during deployment.
    type: str
  description:
    description:
      - Description of the guest OS profile.
    type: str
"""

EXAMPLES = r"""
- name: Create a Windows guest OS profile
  microsoft.scvmm.scvmm_guest_os_profile:
    scvmm_server: scvmm01.example.com
    name: Windows2022-Standard
    operating_system: Windows Server 2022 Datacenter
    computer_name_pattern: "WEB-###"
    admin_password: "{{ vault_admin_password }}"
    domain: example.com
    description: Standard Windows Server 2022 guest profile

- name: Create a Linux guest OS profile
  microsoft.scvmm.scvmm_guest_os_profile:
    scvmm_server: scvmm01.example.com
    name: RHEL9-Standard
    operating_system: "Red Hat Enterprise Linux 9 (64 bit)"
    computer_name_pattern: "LNX-###"
    description: Standard RHEL 9 guest profile

- name: Remove a guest OS profile
  microsoft.scvmm.scvmm_guest_os_profile:
    scvmm_server: scvmm01.example.com
    name: Windows2022-Standard
    state: absent
"""

RETURN = r"""
profile:
  description: Details of the guest OS profile.
  returned: when state is present
  type: dict
  sample:
    name: Windows2022-Standard
    operating_system: Windows Server 2022 Datacenter
    computer_name_pattern: "WEB-###"
    domain: example.com
    description: Standard Windows Server 2022 guest profile
changed:
  description: Whether the guest OS profile was created, updated, or removed.
  returned: always
  type: bool
"""
