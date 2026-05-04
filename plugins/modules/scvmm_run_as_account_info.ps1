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
    $accounts = if ($module.Params.name) {
        Get-SCRunAsAccount -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        Get-SCRunAsAccount -VMMServer $vmmServer
    }

    $result = @()
    foreach ($account in $accounts) {
        $result += ConvertTo-SCVMMDict -InputObject $account -Properties @('Name', 'Description', 'CredentialType', 'UserName', 'ID')
    }

    $module.Result.run_as_accounts = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve Run As accounts: $($_.Exception.Message)", $_)
}
