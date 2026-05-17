#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_job_info
short_description: Gather VMM job history and status
description:
  - Retrieve details of VMM jobs including their status, progress, and error information.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  recent:
    description:
      - Number of recent jobs to retrieve.
    type: int
  status:
    description:
      - Filter jobs by status.
    type: str
    choices: [Running, Completed, Failed, Canceled]
  job_id:
    description:
      - ID of a specific job to retrieve.
    type: str
"""

EXAMPLES = r"""
- name: Get the 10 most recent jobs
  microsoft.scvmm.scvmm_job_info:
    scvmm_server: scvmm01.example.com
    recent: 10
  register: recent_jobs

- name: Get all failed jobs
  microsoft.scvmm.scvmm_job_info:
    scvmm_server: scvmm01.example.com
    status: Failed
  register: failed_jobs

- name: Get a specific job by ID
  microsoft.scvmm.scvmm_job_info:
    scvmm_server: scvmm01.example.com
    job_id: "12345678-abcd-1234-efgh-123456789012"
  register: job
"""

RETURN = r"""
jobs:
  description: List of job dictionaries.
  returned: always
  type: list
  elements: dict
  contains:
    name:
      description: Name of the job.
      type: str
    status:
      description: Current status of the job.
      type: str
    start_time:
      description: When the job started.
      type: str
    end_time:
      description: When the job ended.
      type: str
    progress:
      description: Job progress percentage.
      type: int
    error_info:
      description: Error details if the job failed.
      type: str
"""
