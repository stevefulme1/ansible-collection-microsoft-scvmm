#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_host_cluster_info
short_description: Gather information about SCVMM host clusters
description:
  - Retrieve details of Hyper-V failover clusters managed by SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific host cluster. Omit to list all clusters.
    type: str
"""

EXAMPLES = r"""
- name: List all host clusters
  microsoft.scvmm.scvmm_host_cluster_info:
    scvmm_server: scvmm01.example.com
  register: clusters

- name: Get a specific host cluster
  microsoft.scvmm.scvmm_host_cluster_info:
    scvmm_server: scvmm01.example.com
    name: cluster01.example.com
  register: cluster
"""

RETURN = r"""
clusters:
  description: List of host cluster dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: cluster01.example.com
      status: OK
      host_count: 4
      cluster_reserve: 1
"""
