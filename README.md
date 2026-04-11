# Microsoft SCVMM Collection for Ansible

This collection provides 97 Ansible modules for managing Microsoft System Center Virtual Machine Manager (SCVMM). It enables automation of VM lifecycle management, networking, storage, templates, and infrastructure configuration via PowerShell over WinRM or SSH.

## Requirements

- **Ansible**: >= 2.16.0
- **Python**: >= 3.12
- **Target host**: Windows Server with the `VirtualMachineManager` PowerShell module installed
- **Connectivity**: WinRM (via `pywinrm` or `pypsrp`) or SSH (OpenSSH on Windows Server 2019+)

## Installation

```bash
ansible-galaxy collection install microsoft.scvmm
```

Or from source:

```bash
ansible-galaxy collection build
ansible-galaxy collection install microsoft-scvmm-*.tar.gz
```

## Modules (97)

### VM Lifecycle (7 modules)

| Module | Description |
|--------|-------------|
| `scvmm_vm` | Create, modify, and remove virtual machines |
| `scvmm_vm_info` | Gather information about virtual machines |
| `scvmm_vm_state` | Manage VM power state (start, stop, suspend, resume) |
| `scvmm_vm_checkpoint` | Manage VM checkpoints (create, delete, restore) |
| `scvmm_vm_checkpoint_info` | Gather information about VM checkpoints |
| `scvmm_vm_migrate` | Live and storage migration of VMs |
| `scvmm_vm_clone` | Clone an existing virtual machine |

### VM Peripherals (4 modules)

| Module | Description |
|--------|-------------|
| `scvmm_vm_disk` | Attach and detach virtual hard disks to VMs |
| `scvmm_vm_nic` | Manage virtual network adapters on VMs |
| `scvmm_vm_dvd_drive` | Manage virtual DVD drives and mount ISOs |
| `scvmm_vm_scsi_adapter` | Manage SCSI controllers on VMs |

### Templates (2 modules)

| Module | Description |
|--------|-------------|
| `scvmm_template` | Create, modify, and remove VM templates |
| `scvmm_template_info` | Gather information about VM templates |

### Profiles (8 modules)

| Module | Description |
|--------|-------------|
| `scvmm_hardware_profile` | Manage hardware profiles |
| `scvmm_hardware_profile_info` | Gather information about hardware profiles |
| `scvmm_guest_os_profile` | Manage guest OS profiles |
| `scvmm_guest_os_profile_info` | Gather information about guest OS profiles |
| `scvmm_application_profile` | Manage application profiles |
| `scvmm_application_profile_info` | Gather information about application profiles |
| `scvmm_capability_profile` | Manage capability profiles |
| `scvmm_capability_profile_info` | Gather information about capability profiles |

### Cloud and Host Management (11 modules)

| Module | Description |
|--------|-------------|
| `scvmm_cloud` | Create, modify, and remove SCVMM clouds |
| `scvmm_cloud_info` | Gather information about SCVMM clouds |
| `scvmm_cloud_capacity` | Set cloud capacity limits |
| `scvmm_cloud_capacity_info` | Gather cloud capacity and usage information |
| `scvmm_host` | Add, configure, and remove Hyper-V hosts |
| `scvmm_host_info` | Gather information about Hyper-V hosts |
| `scvmm_host_group` | Manage host groups |
| `scvmm_host_group_info` | Gather information about host groups |
| `scvmm_host_cluster` | Manage Hyper-V host clusters |
| `scvmm_host_cluster_info` | Gather information about host clusters |
| `scvmm_host_rating_info` | Get placement ratings for VM deployment |

### Networking (22 modules)

| Module | Description |
|--------|-------------|
| `scvmm_logical_network` | Create, modify, and remove logical networks |
| `scvmm_logical_network_info` | Gather information about logical networks |
| `scvmm_logical_network_definition` | Manage logical network definitions (sites) |
| `scvmm_logical_network_definition_info` | Gather logical network definition info |
| `scvmm_vm_network` | Create, modify, and remove VM networks |
| `scvmm_vm_network_info` | Gather information about VM networks |
| `scvmm_vm_subnet` | Manage VM subnets |
| `scvmm_vm_subnet_info` | Gather information about VM subnets |
| `scvmm_logical_switch` | Manage logical switches |
| `scvmm_logical_switch_info` | Gather information about logical switches |
| `scvmm_ip_pool` | Manage static IP address pools |
| `scvmm_ip_pool_info` | Gather IP pool information |
| `scvmm_port_classification` | Manage port classifications |
| `scvmm_port_classification_info` | Gather port classification information |
| `scvmm_uplink_port_profile` | Manage uplink port profiles |
| `scvmm_uplink_port_profile_info` | Gather uplink port profile information |
| `scvmm_mac_address_pool` | Manage MAC address pools |
| `scvmm_mac_address_pool_info` | Gather MAC address pool information |
| `scvmm_network_adapter_info` | Gather detailed VM network adapter info |
| `scvmm_load_balancer` | Manage load balancers |
| `scvmm_host_network_adapter` | Configure host physical network adapters |
| `scvmm_host_network_adapter_info` | Gather information about host network adapters |

### Storage (9 modules)

| Module | Description |
|--------|-------------|
| `scvmm_virtual_hard_disk` | Create and remove virtual hard disks (VHD/VHDX) |
| `scvmm_virtual_hard_disk_info` | Gather information about virtual hard disks |
| `scvmm_storage_classification` | Manage storage classifications |
| `scvmm_storage_classification_info` | Gather storage classification info |
| `scvmm_storage_pool` | Manage storage pools |
| `scvmm_storage_pool_info` | Gather storage pool information |
| `scvmm_storage_provider` | Register and manage storage providers |
| `scvmm_storage_provider_info` | Gather storage provider information |
| `scvmm_storage_file_share_info` | Gather file share information |

### Library (7 modules)

| Module | Description |
|--------|-------------|
| `scvmm_library_server_info` | Gather information about library servers |
| `scvmm_library_share` | Manage library shares |
| `scvmm_library_share_info` | Gather library share information |
| `scvmm_iso_info` | Gather ISO image information from library |
| `scvmm_script_info` | Gather script resources from library |
| `scvmm_custom_resource_info` | Gather custom resources from library |
| `scvmm_library_resource` | Import resources into library |

### Credentials and RBAC (6 modules)

| Module | Description |
|--------|-------------|
| `scvmm_user_role` | Manage user roles |
| `scvmm_user_role_info` | Gather information about user roles |
| `scvmm_run_as_account` | Manage RunAs accounts |
| `scvmm_run_as_account_info` | Gather RunAs account information |
| `scvmm_user_role_quota` | Set user role quotas per cloud |
| `scvmm_user_role_quota_info` | Gather user role quota information |

### Service Templates (6 modules)

| Module | Description |
|--------|-------------|
| `scvmm_service_template` | Manage service templates |
| `scvmm_service_template_info` | Gather service template information |
| `scvmm_service` | Deploy and manage service instances |
| `scvmm_service_info` | Gather service instance information |
| `scvmm_sql_profile` | Manage SQL Server profiles |
| `scvmm_sql_profile_info` | Gather SQL profile information |

### Update and Compliance (6 modules)

| Module | Description |
|--------|-------------|
| `scvmm_update_server` | Register and remove WSUS update servers |
| `scvmm_update_server_info` | Gather update server information |
| `scvmm_baseline` | Manage update baselines |
| `scvmm_baseline_info` | Gather baseline information |
| `scvmm_compliance_scan` | Trigger compliance scans on hosts |
| `scvmm_compliance_info` | Gather compliance status |

### Bare Metal Provisioning (4 modules)

| Module | Description |
|--------|-------------|
| `scvmm_pxe_server` | Register PXE servers |
| `scvmm_pxe_server_info` | Gather PXE server information |
| `scvmm_physical_computer_profile` | Manage bare metal deployment profiles |
| `scvmm_physical_computer_profile_info` | Gather bare metal profile information |

### Infrastructure and Configuration (5 modules)

| Module | Description |
|--------|-------------|
| `scvmm_custom_property` | Manage custom property definitions |
| `scvmm_custom_property_info` | Gather custom property information |
| `scvmm_servicing_window` | Manage maintenance servicing windows |
| `scvmm_servicing_window_info` | Gather servicing window information |
| `scvmm_job_info` | Gather VMM job history and status |

## Usage

All modules require connection details for the SCVMM management server:

```yaml
- name: Get all VMs
  microsoft.scvmm.scvmm_vm_info:
    scvmm_server: scvmm01.example.com
  register: all_vms

- name: Create a VM
  microsoft.scvmm.scvmm_vm:
    scvmm_server: scvmm01.example.com
    name: web-server-01
    template: Windows2022-Base
    cloud: Production
    cpu_count: 4
    memory_mb: 8192

- name: Create a logical network
  microsoft.scvmm.scvmm_logical_network:
    scvmm_server: scvmm01.example.com
    name: Corp-Network
    description: Corporate network backbone
```

## Connection Methods

### WinRM (default)

```yaml
ansible_connection: winrm
ansible_winrm_transport: ntlm
```

Requires `pywinrm` or `pypsrp` on the Ansible controller.

### SSH

```yaml
ansible_connection: ssh
ansible_shell_type: powershell
```

Requires OpenSSH server enabled on the Windows host (Windows Server 2019+).

## License

GPL-3.0-or-later

## Author

Steve Fulmer ([@stevefulme1](https://github.com/stevefulme1))
