#!/usr/bin/python
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scvmm_service
short_description: Deploy and manage SCVMM service instances
description:
  - Deploy, modify, start, stop, and remove multi-tier service instances in SCVMM.
  - Services are deployed from service templates into a cloud or host group.
  - Uses PowerShell cmdlets from the C(VirtualMachineManager) module.
version_added: "0.2.0"
author:
  - Steve Fulmer (@stevefulme1)
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the service instance.
    type: str
    required: true
  state:
    description:
      - Desired state of the service instance.
      - C(present) ensures the service exists.
      - C(absent) removes the service.
      - C(started) ensures the service is running.
      - C(stopped) ensures the service is stopped.
    type: str
    choices: [present, absent, started, stopped]
    default: present
  service_template:
    description:
      - Name of the service template to deploy from.
      - Required when I(state=present) and the service does not yet exist.
    type: str
  cloud:
    description:
      - Name of the cloud to deploy the service into.
    type: str
  vm_host_group:
    description:
      - Name of the VM host group for service placement.
    type: str
  description:
    description:
      - Description of the service instance.
    type: str
"""

EXAMPLES = r"""
- name: Deploy a service from a template
  microsoft.scvmm.scvmm_service:
    scvmm_server: scvmm01.example.com
    name: prod-web-app
    service_template: Three-Tier-App
    cloud: Production-Cloud
    description: Production three-tier web application

- name: Stop a service
  microsoft.scvmm.scvmm_service:
    scvmm_server: scvmm01.example.com
    name: prod-web-app
    state: stopped

- name: Start a service
  microsoft.scvmm.scvmm_service:
    scvmm_server: scvmm01.example.com
    name: prod-web-app
    state: started

- name: Remove a service
  microsoft.scvmm.scvmm_service:
    scvmm_server: scvmm01.example.com
    name: prod-web-app
    state: absent
"""

RETURN = r"""
service:
  description: Service instance details.
  returned: when state is present, started, or stopped
  type: dict
  sample:
    name: prod-web-app
    status: Running
    service_template: Three-Tier-App
    cloud: Production-Cloud
    description: Production three-tier web application
"""
