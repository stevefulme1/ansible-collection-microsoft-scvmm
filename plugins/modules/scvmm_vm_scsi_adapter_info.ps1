#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        vm_name = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$vmName = $module.Params.vm_name

$vmmServer = Connect-SCVMM -Module $module

$vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $vmName -ErrorAction SilentlyContinue
if (-not $vm) {
    $module.FailJson("VM '$vmName' not found.")
}

$scsiAdapters = @(Get-SCVirtualSCSIAdapter -VM $vm -ErrorAction Stop)

$module.Result.scsi_adapters = @($scsiAdapters | ForEach-Object {
        $adapter = $_
        @{
            vm_name = $vmName
            scsi_bus = $adapter.BusNumber
            adapter_type = $adapter.AdapterType
            max_luns = 64
            id = $adapter.ID
        }
    })

$module.ExitJson()
