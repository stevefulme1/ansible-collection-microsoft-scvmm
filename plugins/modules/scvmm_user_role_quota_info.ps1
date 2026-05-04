#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        cloud = @{ type = 'str' }
        user_role = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $quotas = @()

    if ($module.Params.user_role -and $module.Params.cloud) {
        $role = Get-SCUserRole -VMMServer $vmmServer -Name $module.Params.user_role -ErrorAction Stop
        $cloudObj = Get-SCCloud -VMMServer $vmmServer -Name $module.Params.cloud -ErrorAction Stop
        $quotas = @(Get-SCUserRoleQuota -VMMServer $vmmServer -UserRole $role -Cloud $cloudObj -ErrorAction SilentlyContinue)
    }
    elseif ($module.Params.user_role) {
        $role = Get-SCUserRole -VMMServer $vmmServer -Name $module.Params.user_role -ErrorAction Stop
        $quotas = Get-SCUserRoleQuota -VMMServer $vmmServer -UserRole $role
    }
    elseif ($module.Params.cloud) {
        $cloudObj = Get-SCCloud -VMMServer $vmmServer -Name $module.Params.cloud -ErrorAction Stop
        $quotas = Get-SCUserRoleQuota -VMMServer $vmmServer -Cloud $cloudObj
    }
    else {
        $quotas = Get-SCUserRoleQuota -VMMServer $vmmServer
    }

    $result = @()
    foreach ($quota in $quotas) {
        $result += ConvertTo-SCVMMDict -InputObject $quota -Properties @(
            'UserRole', 'Cloud', 'CPUCount', 'MemoryMB', 'StorageGB', 'VMCount', 'ID'
        )
    }

    $module.Result.quotas = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve user role quotas: $($_.Exception.Message)", $_)
}
