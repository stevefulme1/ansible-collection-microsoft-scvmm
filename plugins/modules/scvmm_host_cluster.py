#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_cluster
short_description: Manage Hyper-V host clusters in SCVMM
description:
  - Install, configure, and remove Hyper-V failover clusters managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the host cluster.
    type: str
    required: true
  state:
    description:
      - Desired state of the host cluster.
    type: str
    choices: [present, absent]
    default: present
  host_group:
    description:
      - Host group path where the cluster resides.
    type: str
  credential:
    description:
      - Name of the RunAs account used to manage the cluster.
    type: str
  cluster_reserve:
    description:
      - Number of host failures the cluster can sustain.
    type: int
"""

EXAMPLES = r"""
- name: Create a host cluster
  microsoft.scvmm.scvmm_host_cluster:
    scvmm_server: scvmm01.example.com
    name: cluster01.example.com
    host_group: All Hosts\\Production
    credential: ClusterRunAs
    cluster_reserve: 1

- name: Update cluster reserve setting
  microsoft.scvmm.scvmm_host_cluster:
    scvmm_server: scvmm01.example.com
    name: cluster01.example.com
    cluster_reserve: 2

- name: Remove a host cluster
  microsoft.scvmm.scvmm_host_cluster:
    scvmm_server: scvmm01.example.com
    name: cluster01.example.com
    state: absent
"""

RETURN = r"""
cluster:
  description: Host cluster details after the operation.
  returned: when state is present
  type: dict
"""
