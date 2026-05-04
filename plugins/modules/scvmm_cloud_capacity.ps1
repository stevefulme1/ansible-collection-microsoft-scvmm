#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        cloud = @{ type = 'str'; required = $true }
        cpu_count = @{ type = 'int' }
        custom_quota_count = @{ type = 'int' }
        memory_mb = @{ type = 'int' }
        storage_gb = @{ type = 'int' }
        vm_count = @{ type = 'int' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $cloud = Get-SCCloud -VMMServer $vmmServer -Name $module.Params.cloud -ErrorAction Stop

    $existing = Get-SCCloudCapacity -Cloud $cloud -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('CPUCount', 'MemoryMB', 'StorageGB', 'VMCount', 'CustomQuotaCount', 'ID')
    }
    else { @{} }

    $needsChange = $false
    $setParams = @{}

    if ($null -ne $module.Params.cpu_count -and $existing.CPUCount -ne $module.Params.cpu_count) {
        $setParams.CPUCount = $module.Params.cpu_count
        $needsChange = $true
    }
    if ($null -ne $module.Params.memory_mb -and $existing.MemoryMB -ne $module.Params.memory_mb) {
        $setParams.MemoryMB = $module.Params.memory_mb
        $needsChange = $true
    }
    if ($null -ne $module.Params.storage_gb -and $existing.StorageGB -ne $module.Params.storage_gb) {
        $setParams.StorageGB = $module.Params.storage_gb
        $needsChange = $true
    }
    if ($null -ne $module.Params.vm_count -and $existing.VMCount -ne $module.Params.vm_count) {
        $setParams.VMCount = $module.Params.vm_count
        $needsChange = $true
    }
    if ($null -ne $module.Params.custom_quota_count -and $existing.CustomQuotaCount -ne $module.Params.custom_quota_count) {
        $setParams.CustomQuotaCount = $module.Params.custom_quota_count
        $needsChange = $true
    }

    if ($needsChange -and -not $module.CheckMode) {
        Set-SCCloudCapacity -CloudCapacity $existing @setParams -ErrorAction Stop
        $existing = Get-SCCloudCapacity -Cloud $cloud -ErrorAction SilentlyContinue
    }

    $module.Result.changed = $needsChange
    $module.Result.cloud_capacity = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('CPUCount', 'MemoryMB', 'StorageGB', 'VMCount', 'CustomQuotaCount', 'ID')
    }
    else {
        @{
            CPUCount = $module.Params.cpu_count
            MemoryMB = $module.Params.memory_mb
            StorageGB = $module.Params.storage_gb
            VMCount = $module.Params.vm_count
            CustomQuotaCount = $module.Params.custom_quota_count
        }
    }
    $module.Diff.after = $module.Result.cloud_capacity

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage cloud capacity: $($_.Exception.Message)", $_)
}
