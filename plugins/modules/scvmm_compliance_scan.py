#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_compliance_scan
short_description: Trigger compliance scans on SCVMM hosts
description:
  - Start a compliance scan against hosts or clusters to evaluate update baseline adherence.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  vm_host:
    description:
      - Name of the VMM host to scan.
    type: str
  host_cluster:
    description:
      - Name of the host cluster to scan.
    type: str
  baseline:
    description:
      - Name of the baseline to evaluate during the scan.
    type: str
"""

EXAMPLES = r"""
- name: Scan a single host for compliance
  microsoft.scvmm.scvmm_compliance_scan:
    scvmm_server: scvmm01.example.com
    vm_host: hyperv01.example.com

- name: Scan a cluster against a specific baseline
  microsoft.scvmm.scvmm_compliance_scan:
    scvmm_server: scvmm01.example.com
    host_cluster: ProductionCluster
    baseline: Security Updates Q1
"""

RETURN = r"""
scan:
  description: Compliance scan result details.
  returned: always
  type: dict
"""
