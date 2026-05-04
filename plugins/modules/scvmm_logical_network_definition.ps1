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

try {
    $vmmServer = Connect-SCVMM -Module $module

    $logicalNetwork = Get-SCLogicalNetwork -VMMServer $vmmServer -Name $logicalNetworkName -ErrorAction Stop

    $definition = Get-SCLogicalNetworkDefinition -VMMServer $vmmServer -Name $name -LogicalNetwork $logicalNetwork -ErrorAction SilentlyContinue

    $module.Diff.before = if ($definition) {
        @{
            name = $definition.Name
            logical_network = $definition.LogicalNetwork.Name
            host_groups = @($definition.HostGroups | ForEach-Object { $_.Path })
                    }
                    }
                    else {
                    @{}
                    }

                    if ($state -eq "present") {
                    if (-not $definition) {
                    $params = @{
                    VMMServer = $vmmServer
                    Name = $name
                    LogicalNetwork = $logicalNetwork
                    }

                    if ($hostGroups) {
                    $vmHostGroups = @()
                    foreach ($hg in $hostGroups) {
                    $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hg -ErrorAction Stop
                    $vmHostGroups += $vmHostGroup
                    }
                    $params.VMHostGroup = $vmHostGroups
                    }

                    if ($subnetVlans) {
                    $subnetVlanList = @()
                    foreach ($sv in $subnetVlans) {
                    $subnetVlan = New-SCSubnetVLan -Subnet $sv.subnet -VLanID $sv.vlan_id
                    $subnetVlanList += $subnetVlan
                    }
                    $params.SubnetVLan = $subnetVlanList
                    }

                    if (-not $module.CheckMode) {
                    $definition = New-SCLogicalNetworkDefinition @params -ErrorAction Stop
                    }
                    $module.Result.changed = $true
                    }
                    else {
                    $changed = $false
                    $params = @{
                    LogicalNetworkDefinition = $definition
                    }

                    if ($hostGroups) {
                    $vmHostGroups = @()
                    foreach ($hg in $hostGroups) {
                    $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hg -ErrorAction Stop
                    $vmHostGroups += $vmHostGroup
                    }
                    $params.VMHostGroup = $vmHostGroups
                    $changed = $true
                    }

                    if ($subnetVlans) {
                    $subnetVlanList = @()
                    foreach ($sv in $subnetVlans) {
                    $subnetVlan = New-SCSubnetVLan -Subnet $sv.subnet -VLanID $sv.vlan_id
                    $subnetVlanList += $subnetVlan
                    }
                    $params.SubnetVLan = $subnetVlanList
                    $changed = $true
                    }

                    if ($changed -and -not $module.CheckMode) {
                    $definition = Set-SCLogicalNetworkDefinition @params -ErrorAction Stop
                    }

                    $module.Result.changed = $changed
                    }

                    $module.Diff.after = @{
                    name = $name
                    logical_network = $logicalNetworkName
                    host_groups = $hostGroups
                    }

                    if ($definition) {
                    $props = @('Name', 'LogicalNetwork', 'HostGroups', 'SubnetVLans', 'ID')
                    $module.Result.logical_network_definition = ConvertTo-SCVMMDict -InputObject $definition -Properties $props
                    }
                    }
                    else {
                    if ($definition) {
                    if (-not $module.CheckMode) {
                    Remove-SCLogicalNetworkDefinition -LogicalNetworkDefinition $definition -ErrorAction Stop
                    }
                    $module.Result.changed = $true
                    }

                    $module.Diff.after = @{}
                    }

                    }

                    catch {
                    $module.FailJson("Failed to manage logical network definition: $($_.Exception.Message)", $_)
                    }

                    $module.ExitJson()
