#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_library_share
short_description: Manage SCVMM library shares
description:
  - Add or remove library shares in SCVMM.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  path:
    description:
      - UNC path of the library share (e.g. C(\\\\server\\share)).
    type: str
    required: true
  state:
    description:
      - Desired state of the library share.
    type: str
    choices: [present, absent]
    default: present
  library_server:
    description:
      - FQDN of the library server that hosts this share.
    type: str
    required: true
  description:
    description:
      - Description of the library share.
    type: str
  add_default_resources:
    description:
      - Whether to add default resources to the share when creating it.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Add a library share
  microsoft.scvmm.scvmm_library_share:
    scvmm_server: scvmm01.example.com
    path: "\\\\lib01.example.com\\ISOs"
    library_server: lib01.example.com
    description: ISO image library share
    add_default_resources: true

- name: Remove a library share
  microsoft.scvmm.scvmm_library_share:
    scvmm_server: scvmm01.example.com
    path: "\\\\lib01.example.com\\ISOs"
    library_server: lib01.example.com
    state: absent
"""

RETURN = r"""
library_share:
  description: Library share details.
  returned: when state is present
  type: dict
  sample:
    path: "\\\\lib01.example.com\\ISOs"
    library_server: lib01.example.com
    description: ISO image library share
"""
