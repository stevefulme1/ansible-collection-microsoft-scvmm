#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_library_resource_info
short_description: Gather information about resources in the SCVMM library
description:
  - Retrieve details of resources (ISOs, VHDs, scripts, etc.) stored in SCVMM library shares.
  - Can filter by name, library share, or resource type.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - stevefulme1.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific library resource. Omit to list all resources.
    type: str
  library_share:
    description:
      - Filter resources by library share name or UNC path.
    type: str
  resource_type:
    description:
      - Filter resources by type.
    type: str
    choices: [ISO, VHD, VHDX, Script, CustomResource, All]
    default: All
"""

EXAMPLES = r"""
- name: List all library resources
  stevefulme1.scvmm.scvmm_library_resource_info:
    scvmm_server: scvmm01.example.com
  register: resources

- name: List ISOs in a specific share
  stevefulme1.scvmm.scvmm_library_resource_info:
    scvmm_server: scvmm01.example.com
    library_share: "\\\\lib01.example.com\\MSSCVMMLibrary"
    resource_type: ISO
  register: isos

- name: Find a specific resource
  stevefulme1.scvmm.scvmm_library_resource_info:
    scvmm_server: scvmm01.example.com
    name: rhel-9.4-x86_64-dvd.iso
  register: resource
"""

RETURN = r"""
resources:
  description: List of library resource dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: rhel-9.4-x86_64-dvd.iso
      path: "\\\\lib01.example.com\\MSSCVMMLibrary\\rhel-9.4-x86_64-dvd.iso"
      library_share: "\\\\lib01.example.com\\MSSCVMMLibrary"
      resource_type: ISO
      size_mb: 9216
"""
