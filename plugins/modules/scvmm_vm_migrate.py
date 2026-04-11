#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_vm_migrate
short_description: Live or storage migration of SCVMM virtual machines
description:
  - Perform live, storage, or combined live-and-storage migration of virtual machines in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the virtual machine to migrate.
    type: str
    required: true
  destination_host:
    description:
      - Target Hyper-V host for the migration.
      - Required when I(migration_type) is C(Live) or C(LiveAndStorage).
    type: str
  destination_storage:
    description:
      - Target storage path for the VM files.
      - Required when I(migration_type) is C(Storage) or C(LiveAndStorage).
    type: str
  migration_type:
    description:
      - Type of migration to perform.
      - C(Live) moves the VM to a different host.
      - C(Storage) moves the VM storage to a different location on the same host.
      - C(LiveAndStorage) moves both the VM and its storage simultaneously.
    type: str
    choices: [Live, Storage, LiveAndStorage]
    default: Live
"""

EXAMPLES = r"""
- name: Live migrate a VM to a different host
  microsoft.scvmm.scvmm_vm_migrate:
    scvmm_server: scvmm01.example.com
    name: web-server-01
    destination_host: hyperv02.example.com
    migration_type: Live

- name: Storage migrate a VM to a new datastore path
  microsoft.scvmm.scvmm_vm_migrate:
    scvmm_server: scvmm01.example.com
    name: db-server-01
    destination_storage: "C:\\ClusterStorage\\Volume2\\VMs"
    migration_type: Storage

- name: Perform a combined live and storage migration
  microsoft.scvmm.scvmm_vm_migrate:
    scvmm_server: scvmm01.example.com
    name: app-server-01
    destination_host: hyperv03.example.com
    destination_storage: "C:\\ClusterStorage\\Volume3\\VMs"
    migration_type: LiveAndStorage
"""

RETURN = r"""
vm:
  description: Details of the migrated virtual machine.
  returned: success
  type: dict
  sample:
    name: web-server-01
    destination_host: hyperv02.example.com
    migration_type: Live
    status: Completed
changed:
  description: Whether the migration was performed.
  returned: always
  type: bool
"""
