#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_run_as_account
short_description: Manage SCVMM RunAs accounts
description:
  - Create, modify, and remove RunAs accounts in SCVMM.
  - RunAs accounts store credentials used by SCVMM for accessing managed resources.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the RunAs account.
    type: str
    required: true
  state:
    description:
      - Desired state of the RunAs account.
    type: str
    choices: [present, absent]
    default: present
  credential_type:
    description:
      - Type of credential stored in the RunAs account.
    type: str
    choices: [WindowsCredential, CertificateCredential, SSHKeyCredential]
  username:
    description:
      - Username for the RunAs account credential.
    type: str
  password:
    description:
      - Password for the RunAs account credential.
    type: str
    no_log: true
  description:
    description:
      - Description of the RunAs account.
    type: str
"""

EXAMPLES = r"""
- name: Create a Windows RunAs account
  microsoft.scvmm.scvmm_run_as_account:
    scvmm_server: scvmm01.example.com
    name: fabric-admin
    credential_type: WindowsCredential
    username: DOMAIN\\svc-fabric
    password: S3cureP@ss!
    description: Fabric administration credentials

- name: Create an SSH key RunAs account
  microsoft.scvmm.scvmm_run_as_account:
    scvmm_server: scvmm01.example.com
    name: linux-deploy
    credential_type: SSHKeyCredential
    username: deploy
    description: SSH key for Linux host management

- name: Remove a RunAs account
  microsoft.scvmm.scvmm_run_as_account:
    scvmm_server: scvmm01.example.com
    name: fabric-admin
    state: absent
"""

RETURN = r"""
run_as_account:
  description: RunAs account details.
  returned: when state is present
  type: dict
  sample:
    name: fabric-admin
    credential_type: WindowsCredential
    username: DOMAIN\\svc-fabric
    description: Fabric administration credentials
"""
