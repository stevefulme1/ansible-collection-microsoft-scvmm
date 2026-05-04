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
    $servers = if ($module.Params.name) {
        Get-SCUpdateServer -VMMServer $vmmServer -ComputerName $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        Get-SCUpdateServer -VMMServer $vmmServer
    }

    $result = @()
    foreach ($server in $servers) {
        $result += ConvertTo-SCVMMDict -InputObject $server -Properties @(
            'Name', 'ComputerName', 'Port', 'IsConnectionSuccessful', 'ID'
        )
    }

    $module.Result.update_servers = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve update servers: $($_.Exception.Message)", $_)
}
