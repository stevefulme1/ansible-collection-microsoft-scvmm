#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name

try {
    $vmmServer = Connect-SCVMM -Module $module

    if ($name) {
        $logicalNetworks = @(Get-SCLogicalNetwork -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue)
    } else {
        $logicalNetworks = @(Get-SCLogicalNetwork -VMMServer $vmmServer -ErrorAction SilentlyContinue)
    }

    $module.Result.logical_networks = @($logicalNetworks | ForEach-Object {
        ConvertTo-SCVMMDict -InputObject $_ -Properties @(
            'Name', 'Description', 'IsNetworkVirtualizationEnabled', 'ID'
        )
    })

} catch {
    $module.FailJson("Failed to retrieve logical networks: $($_.Exception.Message)", $_)
}

$module.ExitJson()
