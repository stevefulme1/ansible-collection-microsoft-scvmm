#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_library_server_info
short_description: Gather information about SCVMM library servers
description:
  - Retrieve details of library servers and their shares in SCVMM.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of a specific library server. Omit to list all.
    type: str
"""

EXAMPLES = r"""
- name: List all library servers
  microsoft.scvmm.scvmm_library_server_info:
    scvmm_server: scvmm01.example.com
  register: library_servers

- name: Get a specific library server
  microsoft.scvmm.scvmm_library_server_info:
    scvmm_server: scvmm01.example.com
    name: lib01.example.com
  register: lib_server
"""

RETURN = r"""
library_servers:
  description: List of library server dictionaries.
  returned: always
  type: list
  elements: dict
  sample:
    - name: lib01.example.com
      status: Responding
      library_shares:
        - name: MSSCVMMLibrary
          path: "\\\\lib01.example.com\\MSSCVMMLibrary"
"""
