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
    $baselines = if ($module.Params.name) {
        Get-SCBaseline -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        Get-SCBaseline -VMMServer $vmmServer
    }

    $result = @()
    foreach ($baseline in $baselines) {
        $result += ConvertTo-SCVMMDict -InputObject $baseline -Properties @('Name', 'Description', 'BaselineType', 'ID')
    }

    $module.Result.baselines = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve baselines: $($_.Exception.Message)", $_)
}
