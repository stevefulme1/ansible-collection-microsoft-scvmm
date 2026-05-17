#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_script_info
short_description: Gather information about script resources in the SCVMM library
description:
  - Retrieve details of script resources stored in the SCVMM library.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific script resource. Omit to list all.
    type: str
  script_type:
    description:
      - Filter scripts by their type.
    type: str
    choices: [PreInstall, PostInstall, SaveState, RestoreState, PreService, PostService]
"""

EXAMPLES = r"""
- name: List all script resources
  microsoft.scvmm.scvmm_script_info:
    scvmm_server: scvmm01.example.com
  register: scripts

- name: Get post-install scripts only
  microsoft.scvmm.scvmm_script_info:
    scvmm_server: scvmm01.example.com
    script_type: PostInstall
  register: post_scripts

- name: Get a specific script
  microsoft.scvmm.scvmm_script_info:
    scvmm_server: scvmm01.example.com
    name: configure-network.ps1
  register: script
"""

RETURN = r"""
scripts:
  description: List of script resource dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: configure-network.ps1
      script_type: PostInstall
      path: "\\\\lib01.example.com\\MSSCVMMLibrary\\Scripts\\configure-network.ps1"
"""
