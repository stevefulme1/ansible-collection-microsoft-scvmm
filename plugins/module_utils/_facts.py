# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Structured fact extraction for SCVMM objects.

Modelled after ``vmware.vmware.plugins.module_utils._facts``, this
module converts raw PowerShell JSON output into well-structured fact
dictionaries suitable for Ansible return values.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class VmFacts:
    """Extract structured facts from a raw SCVMM VM dictionary."""

    def __init__(self, vm_dict):
        self.vm = vm_dict

    def all_facts(self):
        return {
            **self.identifier_facts(),
            **self.hw_facts(),
            **self.status_facts(),
            **self.placement_facts(),
            **self.network_facts(),
            **self.checkpoint_facts(),
        }

    def identifier_facts(self):
        return {
            "name": self.vm.get("Name"),
            "id": self.vm.get("ID") or self.vm.get("VMId"),
            "description": self.vm.get("Description"),
        }

    def hw_facts(self):
        return {
            "cpu_count": self.vm.get("CPUCount"),
            "memory_mb": self.vm.get("Memory"),
            "dynamic_memory_enabled": self.vm.get("DynamicMemoryEnabled"),
            "dynamic_memory_min_mb": self.vm.get("DynamicMemoryMinimumMB"),
            "dynamic_memory_max_mb": self.vm.get("DynamicMemoryMaximumMB"),
            "generation": self.vm.get("Generation"),
            "is_highly_available": self.vm.get("IsHighlyAvailable"),
        }

    def status_facts(self):
        return {
            "status": self.vm.get("Status"),
            "status_string": self.vm.get("StatusString"),
            "vm_addition_time": self.vm.get("AddedTime"),
            "most_recent_task": self.vm.get("MostRecentTask"),
            "most_recent_task_id": self.vm.get("MostRecentTaskID"),
        }

    def placement_facts(self):
        return {
            "cloud": self.vm.get("Cloud", {}).get("Name")
            if isinstance(self.vm.get("Cloud"), dict)
            else self.vm.get("Cloud"),
            "host_name": self.vm.get("HostName")
            or self.vm.get("VMHost", {}).get("Name")
            if isinstance(self.vm.get("VMHost"), dict)
            else self.vm.get("VMHost"),
            "host_group_path": self.vm.get("HostGroupPath"),
            "vm_path": self.vm.get("VMCPath") or self.vm.get("Location"),
        }

    def network_facts(self):
        adapters = self.vm.get("VirtualNetworkAdapters", []) or []
        nics = []
        for nic in adapters:
            if isinstance(nic, dict):
                nics.append({
                    "name": nic.get("Name"),
                    "mac_address": nic.get("MACAddress"),
                    "mac_type": nic.get("MACAddressType"),
                    "vm_network": nic.get("VMNetwork", {}).get("Name")
                    if isinstance(nic.get("VMNetwork"), dict)
                    else nic.get("VMNetwork"),
                    "ipv4_addresses": nic.get("IPv4Addresses", []),
                })
        return {"network_adapters": nics}

    def checkpoint_facts(self):
        checkpoints = self.vm.get("VMCheckpoints", []) or []
        snaps = []
        for cp in checkpoints:
            if isinstance(cp, dict):
                snaps.append({
                    "name": cp.get("Name"),
                    "id": cp.get("ID"),
                    "description": cp.get("Description"),
                    "added_time": cp.get("AddedTime"),
                })
        return {"checkpoints": snaps}


class CloudFacts:
    """Extract structured facts from a raw SCVMM cloud dictionary."""

    def __init__(self, cloud_dict):
        self.cloud = cloud_dict

    def all_facts(self):
        return {
            "name": self.cloud.get("Name"),
            "id": self.cloud.get("ID"),
            "description": self.cloud.get("Description"),
            "vm_count": self.cloud.get("VMCount"),
            "capacity_cpu": self.cloud.get("CapacityCPUCount"),
            "capacity_memory_mb": self.cloud.get("CapacityMemoryMB"),
            "capacity_storage_gb": self.cloud.get("CapacityStorageGB"),
            "used_cpu": self.cloud.get("UsedCPUCount"),
            "used_memory_mb": self.cloud.get("UsedMemoryMB"),
            "used_storage_gb": self.cloud.get("UsedStorageGB"),
        }


class HostFacts:
    """Extract structured facts from a raw SCVMM host dictionary."""

    def __init__(self, host_dict):
        self.host = host_dict

    def all_facts(self):
        return {
            "name": self.host.get("Name"),
            "id": self.host.get("ID"),
            "fqdn": self.host.get("FQDN") or self.host.get("FullyQualifiedDomainName"),
            "overall_state": self.host.get("OverallState"),
            "operating_system": self.host.get("OperatingSystem", {}).get("Name")
            if isinstance(self.host.get("OperatingSystem"), dict)
            else self.host.get("OperatingSystem"),
            "cpu_count": self.host.get("PhysicalCPUCount"),
            "logical_cpu_count": self.host.get("LogicalCPUCount"),
            "total_memory_gb": self.host.get("TotalMemory"),
            "available_memory_gb": self.host.get("AvailableMemory"),
            "vm_count": self.host.get("VMCount"),
            "hyper_v_version": self.host.get("HyperVVersion"),
            "host_group": self.host.get("VMHostGroup", {}).get("Name")
            if isinstance(self.host.get("VMHostGroup"), dict)
            else self.host.get("VMHostGroup"),
        }


class TemplateFacts:
    """Extract structured facts from a raw SCVMM template dictionary."""

    def __init__(self, template_dict):
        self.template = template_dict

    def all_facts(self):
        return {
            "name": self.template.get("Name"),
            "id": self.template.get("ID"),
            "description": self.template.get("Description"),
            "cpu_count": self.template.get("CPUCount"),
            "memory_mb": self.template.get("Memory"),
            "generation": self.template.get("Generation"),
            "operating_system": self.template.get("OperatingSystem", {}).get("Name")
            if isinstance(self.template.get("OperatingSystem"), dict)
            else self.template.get("OperatingSystem"),
            "is_customizable": self.template.get("IsCustomizable"),
        }


class LogicalNetworkFacts:
    """Extract structured facts from a raw SCVMM logical network dict."""

    def __init__(self, net_dict):
        self.net = net_dict

    def all_facts(self):
        return {
            "name": self.net.get("Name"),
            "id": self.net.get("ID"),
            "description": self.net.get("Description"),
            "is_managed": self.net.get("IsManagedByNetworkController"),
            "network_virtualization_enabled":
                self.net.get("NetworkVirtualizationEnabled"),
        }


class VmNetworkFacts:
    """Extract structured facts from a raw SCVMM VM network dict."""

    def __init__(self, net_dict):
        self.net = net_dict

    def all_facts(self):
        return {
            "name": self.net.get("Name"),
            "id": self.net.get("ID"),
            "description": self.net.get("Description"),
            "logical_network": self.net.get("LogicalNetwork", {}).get("Name")
            if isinstance(self.net.get("LogicalNetwork"), dict)
            else self.net.get("LogicalNetwork"),
            "isolation_type": self.net.get("IsolationType"),
        }


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def extract_facts(raw_dict, keys):
    """Extract a subset of keys from a raw dictionary.

    Useful when the caller only wants specific properties and does not
    need a full ``*Facts`` class.
    """
    return {k: raw_dict.get(k) for k in keys}


def flatten_dict(dictionary, separator=".", parent_key=""):
    """Flatten a nested dict into dot-notation keys.

    ``{"a": {"b": 1}}`` becomes ``{"a.b": 1}``.
    """
    items = []
    for k, v in dictionary.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(
                flatten_dict(v, separator=separator, parent_key=new_key).items()
            )
        else:
            items.append((new_key, v))
    return dict(items)
