# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Indirect query helpers for SCVMM modules.

Modelled after the vmware.vmware collection's indirect lookup pattern,
this module provides a base class that lets any SCVMM module resolve
objects by **name** or **ID** without knowing which identifier the user
supplied.  Each ``get_*_by_name_or_id`` method builds a PowerShell
pipeline, executes it on the SCVMM server, and returns the parsed
result.  Modules inherit from ``ScvmmQuery`` and call these helpers
instead of building raw PowerShell themselves.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.microsoft.scvmm.plugins.module_utils.scvmm import (
    build_connect_script,
    SCVMM_COMMON_ARGS,
)


# ---------------------------------------------------------------------------
# PowerShell output helpers
# ---------------------------------------------------------------------------

def _ps_select_json(properties=None):
    """Return a PS snippet that converts objects to JSON.

    If *properties* is given, only those properties are included via
    ``Select-Object``.  Otherwise all properties are serialised.
    """
    select = ""
    if properties:
        cols = ", ".join(f"'{p}'" for p in properties)
        select = f" | Select-Object {cols}"
    return f"{select} | ConvertTo-Json -Depth 4 -Compress"


def _parse_ps_json(raw_stdout):
    """Parse PowerShell JSON output into a Python list of dicts.

    PowerShell's ``ConvertTo-Json`` returns a single object (dict) when
    there is exactly one result and a JSON array when there are several.
    This normalises the output to always return a list.
    """
    text = raw_stdout.strip()
    if not text:
        return []
    data = json.loads(text)
    if isinstance(data, list):
        return data
    return [data]


# ---------------------------------------------------------------------------
# Core query builder
# ---------------------------------------------------------------------------

class ScvmmQuery:
    """Base class providing indirect-query helpers for SCVMM modules.

    Instantiate with an ``AnsibleModule`` instance.  The helper methods
    build PowerShell commands, but **do not execute them** — the calling
    module is responsible for running the script via its chosen transport
    (WinRM / SSH).  Each helper returns the full PowerShell string so
    modules can append it to their own pipeline.

    Usage inside a module::

        query = ScvmmQuery(module)
        ps_script = query.build_get_vm_script(name="web-01")
        # … execute ps_script via WinRM / SSH …
    """

    def __init__(self, module):
        self.module = module
        self.params = module.params
        self._connect = build_connect_script(
            server=self.params["scvmm_server"],
            port=self.params.get("scvmm_port", 8100),
        )

    # -- generic object lookup ----------------------------------------------

    @staticmethod
    def _build_get_cmd(cmdlet, name=None, obj_id=None, filters=None,
                       properties=None):
        """Build a ``Get-SC*`` command with optional name/ID filter.

        Args:
            cmdlet: The PowerShell cmdlet (e.g. ``Get-SCVirtualMachine``).
            name:   Human-readable name to search for.
            obj_id: SCVMM object ID (GUID) to search for.
            filters: Extra ``-ParameterName Value`` pairs as a dict.
            properties: List of property names to include in the JSON output.

        Returns:
            str: A complete PowerShell one-liner.
        """
        parts = [cmdlet, "-VMMServer $vmmServer"]

        if obj_id:
            parts.append(f"-ID '{obj_id}'")
        elif name:
            parts.append(f"-Name '{name}'")

        if filters:
            for key, value in filters.items():
                parts.append(f"-{key} '{value}'")

        cmd = " ".join(parts)
        cmd += _ps_select_json(properties)
        return cmd

    def _build_full_script(self, get_cmd):
        """Prepend the connection preamble to a Get command."""
        return self._connect + get_cmd

    # -- VM -----------------------------------------------------------------

    def build_get_vm_script(self, name=None, vm_id=None, cloud=None,
                            vm_host=None, properties=None):
        """Build a script to look up VMs by name, ID, or filters.

        At least one of *name*, *vm_id*, *cloud*, or *vm_host* should be
        supplied.  If none is given the cmdlet returns **all** VMs.
        """
        filters = {}
        if cloud:
            filters["Cloud"] = cloud
        if vm_host:
            filters["VMHost"] = vm_host
        cmd = self._build_get_cmd(
            "Get-SCVirtualMachine", name=name, obj_id=vm_id,
            filters=filters, properties=properties,
        )
        return self._build_full_script(cmd)

    def get_vm_using_params(self, name_param="name", id_param="vm_id",
                            fail_on_missing=False, properties=None):
        """Determine which VM identifier the user supplied and build a
        lookup script.  Mirrors the VMware ``get_vms_using_params`` pattern.

        Returns:
            tuple(str, str): ``(search_type, ps_script)``
        """
        search_type, search_value = self._determine_identifier(
            name_param, id_param, fail_on_missing,
        )
        if search_type is None:
            return None, None

        if search_type == "id":
            script = self.build_get_vm_script(vm_id=search_value,
                                              properties=properties)
        else:
            cloud = self.params.get("cloud")
            vm_host = self.params.get("vm_host")
            script = self.build_get_vm_script(name=search_value, cloud=cloud,
                                              vm_host=vm_host,
                                              properties=properties)
        return search_type, script

    # -- Template -----------------------------------------------------------

    def build_get_template_script(self, name=None, template_id=None,
                                  properties=None):
        cmd = self._build_get_cmd(
            "Get-SCVMTemplate", name=name, obj_id=template_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Cloud --------------------------------------------------------------

    def build_get_cloud_script(self, name=None, cloud_id=None,
                               properties=None):
        cmd = self._build_get_cmd(
            "Get-SCCloud", name=name, obj_id=cloud_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Host Group ---------------------------------------------------------

    def build_get_host_group_script(self, name=None, host_group_id=None,
                                    properties=None):
        cmd = self._build_get_cmd(
            "Get-SCVMHostGroup", name=name, obj_id=host_group_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Host ---------------------------------------------------------------

    def build_get_host_script(self, name=None, host_id=None,
                              properties=None):
        cmd = self._build_get_cmd(
            "Get-SCVMHost", name=name, obj_id=host_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Logical Network ----------------------------------------------------

    def build_get_logical_network_script(self, name=None, network_id=None,
                                         properties=None):
        cmd = self._build_get_cmd(
            "Get-SCLogicalNetwork", name=name, obj_id=network_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- VM Network ---------------------------------------------------------

    def build_get_vm_network_script(self, name=None, network_id=None,
                                    properties=None):
        cmd = self._build_get_cmd(
            "Get-SCVMNetwork", name=name, obj_id=network_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Virtual Hard Disk --------------------------------------------------

    def build_get_vhd_script(self, name=None, vhd_id=None,
                             properties=None):
        cmd = self._build_get_cmd(
            "Get-SCVirtualHardDisk", name=name, obj_id=vhd_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Checkpoint ---------------------------------------------------------

    def build_get_checkpoint_script(self, vm_name=None, vm_id=None,
                                    properties=None):
        """Build a script to retrieve checkpoints for a VM.

        Checkpoints are children of a VM, so we pipe ``Get-SCVirtualMachine``
        into ``Get-SCVMCheckpoint``.
        """
        if vm_id:
            vm_part = (f"Get-SCVirtualMachine -VMMServer $vmmServer "
                       f"-ID '{vm_id}'")
        elif vm_name:
            vm_part = (f"Get-SCVirtualMachine -VMMServer $vmmServer "
                       f"-Name '{vm_name}'")
        else:
            self.module.fail_json(
                msg="vm_name or vm_id is required to query checkpoints")
            return ""

        cmd = f"{vm_part} | Get-SCVMCheckpoint"
        cmd += _ps_select_json(properties)
        return self._build_full_script(cmd)

    # -- IP Pool ------------------------------------------------------------

    def build_get_ip_pool_script(self, name=None, pool_id=None,
                                 properties=None):
        cmd = self._build_get_cmd(
            "Get-SCStaticIPAddressPool", name=name, obj_id=pool_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Storage Classification ---------------------------------------------

    def build_get_storage_classification_script(self, name=None,
                                                classification_id=None,
                                                properties=None):
        cmd = self._build_get_cmd(
            "Get-SCStorageClassification", name=name,
            obj_id=classification_id, properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Port Classification ------------------------------------------------

    def build_get_port_classification_script(self, name=None,
                                             classification_id=None,
                                             properties=None):
        cmd = self._build_get_cmd(
            "Get-SCPortClassification", name=name,
            obj_id=classification_id, properties=properties,
        )
        return self._build_full_script(cmd)

    # -- Library Server -----------------------------------------------------

    def build_get_library_server_script(self, name=None, server_id=None,
                                        properties=None):
        cmd = self._build_get_cmd(
            "Get-SCLibraryServer", name=name, obj_id=server_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- User Role ----------------------------------------------------------

    def build_get_user_role_script(self, name=None, role_id=None,
                                   properties=None):
        cmd = self._build_get_cmd(
            "Get-SCUserRole", name=name, obj_id=role_id,
            properties=properties,
        )
        return self._build_full_script(cmd)

    # -- identifier resolution (mirrors VMware pattern) ---------------------

    def _determine_identifier(self, name_param, id_param, fail_on_missing):
        """Pick the best identifier from module params.

        Prefers ID over name (IDs are globally unique in SCVMM).

        Returns:
            tuple(str|None, str|None): ``("id"|"name", value)``
        """
        if self.params.get(id_param):
            return "id", self.params[id_param]
        if self.params.get(name_param):
            return "name", self.params[name_param]

        if fail_on_missing:
            self.module.fail_json(
                msg=(f"One of '{name_param}' or '{id_param}' is required "
                     "to identify the object."))
        return None, None

    # -- convenience: resolve related objects --------------------------------

    def resolve_cloud(self, fail_on_missing=False):
        """Return a PS script that resolves the cloud from params."""
        name = self.params.get("cloud")
        cloud_id = self.params.get("cloud_id")
        if not name and not cloud_id:
            if fail_on_missing:
                self.module.fail_json(
                    msg="'cloud' or 'cloud_id' is required.")
            return None
        return self.build_get_cloud_script(name=name, cloud_id=cloud_id)

    def resolve_template(self, fail_on_missing=False):
        """Return a PS script that resolves the template from params."""
        name = self.params.get("template")
        template_id = self.params.get("template_id")
        if not name and not template_id:
            if fail_on_missing:
                self.module.fail_json(
                    msg="'template' or 'template_id' is required.")
            return None
        return self.build_get_template_script(
            name=name, template_id=template_id)

    def resolve_host_group(self, fail_on_missing=False):
        """Return a PS script that resolves the host group from params."""
        name = self.params.get("host_group")
        hg_id = self.params.get("host_group_id")
        if not name and not hg_id:
            if fail_on_missing:
                self.module.fail_json(
                    msg="'host_group' or 'host_group_id' is required.")
            return None
        return self.build_get_host_group_script(
            name=name, host_group_id=hg_id)
