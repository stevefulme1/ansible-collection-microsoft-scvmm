# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  scvmm_server:
    description:
      - Hostname or IP address of the SCVMM management server.
    type: str
    required: true
  scvmm_port:
    description:
      - TCP port for the SCVMM management service.
    type: int
    default: 8100
requirements:
  - The target host must be a Windows machine with the
    C(VirtualMachineManager) PowerShell module installed.
  - WinRM connectivity from the Ansible controller to the SCVMM server.
notes:
  - All modules in this collection execute PowerShell cmdlets from the
    C(VirtualMachineManager) module via WinRM.
  - Run these modules against the SCVMM management server or a host that
    has the VMM console installed.
"""
