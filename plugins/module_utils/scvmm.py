# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Shared utilities for SCVMM modules.

All modules in this collection execute PowerShell cmdlets from the
VirtualMachineManager module on a remote Windows host via WinRM.
This helper centralises the connection setup, command execution,
and result parsing so individual modules stay small.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


SCVMM_COMMON_ARGS = dict(
    scvmm_server=dict(type="str", required=True),
    scvmm_port=dict(type="int", default=8100),
)


def build_connect_script(server, port=8100):
    """Return a PowerShell snippet that imports the VMM module and connects."""
    return (
        "Import-Module VirtualMachineManager -ErrorAction Stop; "
        f"$vmmServer = Get-SCVMMServer -ComputerName '{server}' "
        f"-TCPPort {port} -ErrorAction Stop; "
    )
