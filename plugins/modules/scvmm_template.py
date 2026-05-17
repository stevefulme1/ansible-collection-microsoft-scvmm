#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_template
short_description: Manage SCVMM VM templates
description:
  - Create and remove virtual machine templates in SCVMM.
  - Templates can be created from existing VMs or from VHDs in the library.
version_added: "0.1.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the VM template.
    type: str
    required: true
  state:
    description:
      - Desired state of the template.
    type: str
    choices: [present, absent]
    default: present
  source_vm:
    description:
      - Name of a VM to clone as a template.
      - Mutually exclusive with I(vhd).
    type: str
  vhd:
    description:
      - Path to a VHD in the SCVMM library to use as template disk.
      - Mutually exclusive with I(source_vm).
    type: str
  library_server:
    description:
      - Library server where the template will be stored.
    type: str
  cpu_count:
    description:
      - Number of virtual CPUs for the template.
    type: int
  memory_mb:
    description:
      - Memory in megabytes for the template.
    type: int
  description:
    description:
      - Description of the template.
    type: str
  os_type:
    description:
      - Operating system type for the template.
    type: str
"""

EXAMPLES = r"""
- name: Create template from existing VM
  microsoft.scvmm.scvmm_template:
    scvmm_server: scvmm01.example.com
    name: Windows2022-Standard
    source_vm: golden-image-win2022
    library_server: lib01.example.com
    description: Windows Server 2022 Standard base image

- name: Remove a template
  microsoft.scvmm.scvmm_template:
    scvmm_server: scvmm01.example.com
    name: Windows2022-Standard
    state: absent
"""

RETURN = r"""
template:
  description: Template details.
  returned: when state is present
  type: dict
  sample:
    name: Windows2022-Standard
    cpu_count: 2
    memory_mb: 4096
"""
