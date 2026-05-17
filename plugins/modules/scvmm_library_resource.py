#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_library_resource
short_description: Import resources into the SCVMM library
description:
  - Import physical resources (ISOs, VHDs, scripts, etc.) into an SCVMM library share.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  source_path:
    description:
      - Local or UNC path to the resource file to import.
    type: str
    required: true
  library_share:
    description:
      - Name or UNC path of the destination library share.
    type: str
    required: true
  overwrite:
    description:
      - Whether to overwrite an existing resource with the same name.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Import an ISO into the library
  microsoft.scvmm.scvmm_library_resource:
    scvmm_server: scvmm01.example.com
    source_path: "\\\\fileserver\\staging\\rhel-9.4-x86_64-dvd.iso"
    library_share: "\\\\lib01.example.com\\MSSCVMMLibrary"

- name: Import a VHD and overwrite if it exists
  microsoft.scvmm.scvmm_library_resource:
    scvmm_server: scvmm01.example.com
    source_path: "C:\\Exports\\base-image.vhdx"
    library_share: "\\\\lib01.example.com\\MSSCVMMLibrary"
    overwrite: true
"""

RETURN = r"""
resource:
  description: Imported resource details.
  returned: always
  type: dict
  sample:
    name: rhel-9.4-x86_64-dvd.iso
    path: "\\\\lib01.example.com\\MSSCVMMLibrary\\rhel-9.4-x86_64-dvd.iso"
    library_share: "\\\\lib01.example.com\\MSSCVMMLibrary"
"""
