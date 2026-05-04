#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $roles = if ($module.Params.name) {
        Get-SCUserRole -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
    } else {
        Get-SCUserRole -VMMServer $vmmServer
    }

    $result = @()
    foreach ($role in $roles) {
        $result += ConvertTo-SCVMMDict -InputObject $role -Properties @(
            'Name', 'Description', 'Profile', 'Members', 'ID'
        )
    }

    $module.Result.user_roles = $result
    $module.ExitJson()
} catch {
    $module.FailJson("Failed to retrieve user roles: $($_.Exception.Message)", $_)
}
