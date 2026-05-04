#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = "str" }
        logical_network = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$logicalNetworkName = $module.Params.logical_network

try {
    $vmmServer = Connect-SCVMM -Module $module

    $params = @{
        VMMServer = $vmmServer
        ErrorAction = "SilentlyContinue"
    }

    if ($logicalNetworkName) {
        $logicalNetwork = Get-SCLogicalNetwork -VMMServer $vmmServer -Name $logicalNetworkName -ErrorAction Stop
        $params.LogicalNetwork = $logicalNetwork
    }

    if ($name) {
        $params.Name = $name
    }

    $definitions = @(Get-SCLogicalNetworkDefinition @params)

    $module.Result.definitions = @($definitions | ForEach-Object {
        ConvertTo-SCVMMDict -InputObject $_ -Properties @(
            'Name', 'LogicalNetwork', 'HostGroups', 'SubnetVLans', 'ID'
        )
    })

} catch {
    $module.FailJson("Failed to retrieve logical network definitions: $($_.Exception.Message)", $_)
}

$module.ExitJson()
