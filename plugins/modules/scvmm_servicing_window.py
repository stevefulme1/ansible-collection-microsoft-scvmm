#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_servicing_window
short_description: Manage servicing windows in SCVMM
description:
  - Create, modify, and remove maintenance servicing windows that control when updates can be applied.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the servicing window.
    type: str
    required: true
  state:
    description:
      - Desired state of the servicing window.
    type: str
    choices: [present, absent]
    default: present
  description:
    description:
      - Description of the servicing window.
    type: str
  start_date:
    description:
      - Start date and time of the servicing window in ISO 8601 format.
    type: str
  end_date:
    description:
      - End date and time of the servicing window in ISO 8601 format.
    type: str
  time_zone:
    description:
      - Time zone for the servicing window schedule.
    type: str
  minutes_duration:
    description:
      - Duration of the servicing window in minutes.
    type: int
  category:
    description:
      - Category of the servicing window.
    type: str
    choices: [None, Runbook, WindowsUpdateAgent]
"""

EXAMPLES = r"""
- name: Create a servicing window
  microsoft.scvmm.scvmm_servicing_window:
    scvmm_server: scvmm01.example.com
    name: Sunday Maintenance
    description: Weekly Sunday maintenance window
    start_date: "2026-04-12T02:00:00"
    end_date: "2026-04-12T06:00:00"
    time_zone: Eastern Standard Time
    minutes_duration: 240
    category: WindowsUpdateAgent

- name: Remove a servicing window
  microsoft.scvmm.scvmm_servicing_window:
    scvmm_server: scvmm01.example.com
    name: Sunday Maintenance
    state: absent
"""

RETURN = r"""
servicing_window:
  description: Servicing window details.
  returned: when state is present
  type: dict
"""
