#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        logical_network = @{ type = 'str' }
        name = @{ type = 'str' }
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

    if ($name) {
        $params.Name = $name
    }

    $vmNetworks = @(Get-SCVMNetwork @params)

    if ($logicalNetworkName) {
        $logicalNetwork = Get-SCLogicalNetwork -VMMServer $vmmServer -Name $logicalNetworkName -ErrorAction Stop
        $vmNetworks = @($vmNetworks | Where-Object { $_.LogicalNetwork.ID -eq $logicalNetwork.ID })
    }

    $module.Result.vm_networks = @($vmNetworks | ForEach-Object {
            ConvertTo-SCVMMDict -InputObject $_ -Properties @(
            'Name', 'Description', 'LogicalNetwork', 'IsolationType', 'VMSubnet', 'ID'
            )
        })

}

catch {
    $module.FailJson("Failed to retrieve VM networks: $($_.Exception.Message)", $_)
}

$module.ExitJson()
