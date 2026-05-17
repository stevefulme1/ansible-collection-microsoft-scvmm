#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_iso_info
short_description: Gather information about ISO images in the SCVMM library
description:
  - Retrieve details of ISO images stored in the SCVMM library.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific ISO image. Omit to list all.
    type: str
  library_server:
    description:
      - Filter ISO images by library server FQDN.
    type: str
"""

EXAMPLES = r"""
- name: List all ISO images
  microsoft.scvmm.scvmm_iso_info:
    scvmm_server: scvmm01.example.com
  register: isos

- name: Get ISOs on a specific library server
  microsoft.scvmm.scvmm_iso_info:
    scvmm_server: scvmm01.example.com
    library_server: lib01.example.com
  register: server_isos

- name: Get a specific ISO image
  microsoft.scvmm.scvmm_iso_info:
    scvmm_server: scvmm01.example.com
    name: rhel-9.4-x86_64-dvd.iso
  register: iso
"""

RETURN = r"""
isos:
  description: List of ISO image dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: rhel-9.4-x86_64-dvd.iso
      path: "\\\\lib01.example.com\\MSSCVMMLibrary\\ISOs\\rhel-9.4-x86_64-dvd.iso"
      size: 10737418240
      library_server: lib01.example.com
"""
