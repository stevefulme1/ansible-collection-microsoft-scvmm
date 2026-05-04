#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        user_role = @{ type = 'str'; required = $true }
        cloud = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        cpu_count = @{ type = 'int' }
        memory_mb = @{ type = 'int' }
        storage_gb = @{ type = 'int' }
        vm_count = @{ type = 'int' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $role = Get-SCUserRole -VMMServer $vmmServer -Name $module.Params.user_role -ErrorAction Stop
    $cloudObj = Get-SCCloud -VMMServer $vmmServer -Name $module.Params.cloud -ErrorAction Stop

    $existing = Get-SCUserRoleQuota -VMMServer $vmmServer -UserRole $role -Cloud $cloudObj -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('UserRole', 'Cloud', 'CPUCount', 'MemoryMB', 'StorageGB', 'VMCount', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Set-SCUserRoleQuota -UserRoleQuota $existing -CPUCount 0 -MemoryMB 0 -StorageGB 0 -VMCount 0 -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    else {
        $needsChange = $false
        $setParams = @{}

        if ($null -ne $module.Params.cpu_count) {
            if (-not $existing -or $existing.CPUCount -ne $module.Params.cpu_count) {
                $setParams.CPUCount = $module.Params.cpu_count
                $needsChange = $true
            }
        }
        if ($null -ne $module.Params.memory_mb) {
            if (-not $existing -or $existing.MemoryMB -ne $module.Params.memory_mb) {
                $setParams.MemoryMB = $module.Params.memory_mb
                $needsChange = $true
            }
        }
        if ($null -ne $module.Params.storage_gb) {
            if (-not $existing -or $existing.StorageGB -ne $module.Params.storage_gb) {
                $setParams.StorageGB = $module.Params.storage_gb
                $needsChange = $true
            }
        }
        if ($null -ne $module.Params.vm_count) {
            if (-not $existing -or $existing.VMCount -ne $module.Params.vm_count) {
                $setParams.VMCount = $module.Params.vm_count
                $needsChange = $true
            }
        }

        if ($needsChange -and -not $module.CheckMode) {
            if ($existing) {
                Set-SCUserRoleQuota -UserRoleQuota $existing @setParams -ErrorAction Stop
            }
            else {
                $setParams.UserRole = $role
                $setParams.Cloud = $cloudObj
                Set-SCUserRoleQuota @setParams -ErrorAction Stop
            }
            $existing = Get-SCUserRoleQuota -VMMServer $vmmServer -UserRole $role -Cloud $cloudObj -ErrorAction SilentlyContinue
        }

        $module.Result.changed = $needsChange
        $module.Diff.after = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @('UserRole', 'Cloud', 'CPUCount', 'MemoryMB', 'StorageGB', 'VMCount', 'ID')
        }
        else {
            @{
                UserRole = $module.Params.user_role
                Cloud = $module.Params.cloud
                CPUCount = $module.Params.cpu_count
                MemoryMB = $module.Params.memory_mb
                StorageGB = $module.Params.storage_gb
                VMCount = $module.Params.vm_count
            }
        }
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage user role quota: $($_.Exception.Message)", $_)
}
