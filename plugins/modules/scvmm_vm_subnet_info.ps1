#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = "str" }
        vm_network = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$vmNetworkName = $module.Params.vm_network

try {
    $vmmServer = Connect-SCVMM -Module $module

    $params = @{
        VMMServer = $vmmServer
        ErrorAction = "SilentlyContinue"
    }

    if ($name) {
        $params.Name = $name
    }

    $vmSubnets = @(Get-SCVMSubnet @params)

    if ($vmNetworkName) {
        $vmNetwork = Get-SCVMNetwork -VMMServer $vmmServer -Name $vmNetworkName -ErrorAction Stop
        $vmSubnets = @($vmSubnets | Where-Object { $_.VMNetwork.ID -eq $vmNetwork.ID })
    }

    $module.Result.vm_subnets = @($vmSubnets | ForEach-Object {
        ConvertTo-SCVMMDict -InputObject $_ -Properties @(
            'Name', 'VMNetwork', 'Subnet', 'VLanID', 'ID'
        )
    })

} catch {
    $module.FailJson("Failed to retrieve VM subnets: $($_.Exception.Message)", $_)
}

$module.ExitJson()
