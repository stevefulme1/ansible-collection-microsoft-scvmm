#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        host_groups = @{ type = 'list'; elements = 'str' }
        logical_network = @{ type = 'str'; required = $true }
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        subnet_vlans = @{ type = 'list'; elements = 'dict' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$logicalNetworkName = $module.Params.logical_network
$state = $module.Params.state
$hostGroups = $module.Params.host_groups
$subnetVlans = $module.Params.subnet_vlans

$vmmServer = Connect-SCVMM -Module $module

$logicalNetwork = Get-SCLogicalNetwork -VMMServer $vmmServer `
    -Name $logicalNetworkName -ErrorAction Stop

$definition = Get-SCLogicalNetworkDefinition -VMMServer $vmmServer `
    -Name $name -LogicalNetwork $logicalNetwork -ErrorAction SilentlyContinue

$props = @('Name', 'LogicalNetwork', 'HostGroups', 'SubnetVLans', 'ID')

$before = @{}
if ($definition) {
    $before = ConvertTo-SCVMMDict -InputObject $definition -Properties $props
}

if ($state -eq "present") {
    if (-not $definition) {
        $params = @{
            VMMServer = $vmmServer
            Name = $name
            LogicalNetwork = $logicalNetwork
            ErrorAction = "Stop"
        }

        if ($hostGroups) {
            $vmHostGroups = @()
            foreach ($hg in $hostGroups) {
                $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer `
                    -Name $hg -ErrorAction Stop
                $vmHostGroups += $vmHostGroup
            }
            $params.VMHostGroup = $vmHostGroups
        }

        if ($subnetVlans) {
            $subnetVlanList = @()
            foreach ($sv in $subnetVlans) {
                $subnetVlan = New-SCSubnetVLan -Subnet $sv.subnet `
                    -VLanID $sv.vlan_id
                $subnetVlanList += $subnetVlan
            }
            $params.SubnetVLan = $subnetVlanList
        }

        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $definition = New-SCLogicalNetworkDefinition @params
        }
    }
    else {
        $changed = $false
        $setParams = @{
            LogicalNetworkDefinition = $definition
            ErrorAction = "Stop"
        }

        if ($hostGroups) {
            $vmHostGroups = @()
            foreach ($hg in $hostGroups) {
                $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer `
                    -Name $hg -ErrorAction Stop
                $vmHostGroups += $vmHostGroup
            }
            $setParams.VMHostGroup = $vmHostGroups
            $changed = $true
        }

        if ($subnetVlans) {
            $subnetVlanList = @()
            foreach ($sv in $subnetVlans) {
                $subnetVlan = New-SCSubnetVLan -Subnet $sv.subnet `
                    -VLanID $sv.vlan_id
                $subnetVlanList += $subnetVlan
            }
            $setParams.SubnetVLan = $subnetVlanList
            $changed = $true
        }

        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                $definition = Set-SCLogicalNetworkDefinition @setParams
            }
        }
    }

    $after = @{}
    if ($definition) {
        $after = ConvertTo-SCVMMDict -InputObject $definition -Properties $props
        $module.Result.logical_network_definition = $after
    }
}
else {
    if ($definition) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            Remove-SCLogicalNetworkDefinition `
                -LogicalNetworkDefinition $definition -ErrorAction Stop
        }
    }
    $after = @{}
}

if ($module.DiffMode) {
    $module.Diff.before = $before
    $module.Diff.after = $after
}

$module.ExitJson()
