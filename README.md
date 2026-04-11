# Microsoft SCVMM Collection for Ansible

This collection provides Ansible modules for managing Microsoft System Center Virtual Machine Manager (SCVMM). It enables automation of VM lifecycle management, networking, storage, templates, and infrastructure configuration via PowerShell over WinRM or SSH.

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

## Modules

### VM Lifecycle

| Module | Description |
|--------|-------------|
| `scvmm_vm` | Create, modify, and remove virtual machines |
| `scvmm_vm_info` | Gather information about virtual machines |
| `scvmm_vm_state` | Manage VM power state (start, stop, suspend, resume) |
| `scvmm_vm_checkpoint` | Manage VM checkpoints (create, delete, restore) |
| `scvmm_vm_checkpoint_info` | Gather information about VM checkpoints |

### VM Peripherals

| Module | Description |
|--------|-------------|
| `scvmm_vm_disk` | Attach and detach virtual hard disks to VMs |
| `scvmm_vm_nic` | Manage virtual network adapters on VMs |

### Templates

| Module | Description |
|--------|-------------|
| `scvmm_template` | Create, modify, and remove VM templates |
| `scvmm_template_info` | Gather information about VM templates |

### Cloud and Host Management

| Module | Description |
|--------|-------------|
| `scvmm_cloud` | Create, modify, and remove SCVMM clouds |
| `scvmm_cloud_info` | Gather information about SCVMM clouds |
| `scvmm_host_group` | Manage host groups |
| `scvmm_host_group_info` | Gather information about host groups |
| `scvmm_host_info` | Gather information about Hyper-V hosts |

### Networking

| Module | Description |
|--------|-------------|
| `scvmm_logical_network` | Create, modify, and remove logical networks |
| `scvmm_logical_network_info` | Gather information about logical networks |
| `scvmm_vm_network` | Create, modify, and remove VM networks |
| `scvmm_vm_network_info` | Gather information about VM networks |
| `scvmm_ip_pool` | Manage static IP address pools |
| `scvmm_port_classification` | Manage port classifications |

### Storage

| Module | Description |
|--------|-------------|
| `scvmm_virtual_hard_disk` | Create and remove virtual hard disks (VHD/VHDX) |
| `scvmm_virtual_hard_disk_info` | Gather information about virtual hard disks |
| `scvmm_storage_classification` | Manage storage classifications |

### Infrastructure

| Module | Description |
|--------|-------------|
| `scvmm_library_server_info` | Gather information about library servers |

### RBAC

| Module | Description |
|--------|-------------|
| `scvmm_user_role` | Manage user roles |
| `scvmm_user_role_info` | Gather information about user roles |

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
