#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        cloud = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $cloud = Get-SCCloud -VMMServer $vmmServer -Name $module.Params.cloud -ErrorAction Stop

    $capacity = Get-SCCloudCapacity -Cloud $cloud -ErrorAction SilentlyContinue

    $module.Result.cloud_capacity = if ($capacity) {
        ConvertTo-SCVMMDict -InputObject $capacity -Properties @(
            'CPUCount', 'MemoryMB', 'StorageGB', 'VMCount', 'CustomQuotaCount', 'ID'
        )
    } else {
        @{}
    }

    $module.ExitJson()
} catch {
    $module.FailJson("Failed to retrieve cloud capacity: $($_.Exception.Message)", $_)
}
