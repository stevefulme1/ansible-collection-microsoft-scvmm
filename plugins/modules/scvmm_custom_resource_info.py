#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_custom_resource_info
short_description: Gather information about custom resources in the SCVMM library
description:
  - Retrieve details of custom resources stored in the SCVMM library.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific custom resource. Omit to list all.
    type: str
  library_server:
    description:
      - Filter custom resources by library server FQDN.
    type: str
"""

EXAMPLES = r"""
- name: List all custom resources
  microsoft.scvmm.scvmm_custom_resource_info:
    scvmm_server: scvmm01.example.com
  register: resources

- name: Get custom resources on a specific library server
  microsoft.scvmm.scvmm_custom_resource_info:
    scvmm_server: scvmm01.example.com
    library_server: lib01.example.com
  register: server_resources

- name: Get a specific custom resource
  microsoft.scvmm.scvmm_custom_resource_info:
    scvmm_server: scvmm01.example.com
    name: dsc-configs.cr
  register: resource
"""

RETURN = r"""
resources:
  description: List of custom resource dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: dsc-configs.cr
      path: "\\\\lib01.example.com\\MSSCVMMLibrary\\CustomResources\\dsc-configs.cr"
      library_server: lib01.example.com
"""
