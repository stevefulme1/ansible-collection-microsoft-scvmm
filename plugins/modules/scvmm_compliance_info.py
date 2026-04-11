#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_compliance_info
short_description: Gather compliance status from SCVMM
description:
  - Retrieve the compliance status of hosts or clusters against update baselines.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_host:
    description:
      - Name of the VMM host to query compliance for.
    type: str
  host_cluster:
    description:
      - Name of the host cluster to query compliance for.
    type: str
"""

EXAMPLES = r"""
- name: Get compliance status for a host
  microsoft.scvmm.scvmm_compliance_info:
    scvmm_server: scvmm01.example.com
    vm_host: hyperv01.example.com
  register: compliance

- name: Get compliance status for a cluster
  microsoft.scvmm.scvmm_compliance_info:
    scvmm_server: scvmm01.example.com
    host_cluster: ProductionCluster
  register: compliance
"""

RETURN = r"""
compliance:
  description: List of compliance status dictionaries per host.
  returned: always
  type: list
  elements: dict
"""
