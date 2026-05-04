#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        subnet = @{ type = 'str' }
        vm_network = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$vmNetworkName = $module.Params.vm_network
$state = $module.Params.state
$subnet = $module.Params.subnet
$vlanId = $module.Params.vlan_id

try {
    $vmmServer = Connect-SCVMM -Module $module

    $vmNetwork = Get-SCVMNetwork -VMMServer $vmmServer -Name $vmNetworkName -ErrorAction Stop

    $vmSubnet = Get-SCVMSubnet -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue | Where-Object {
        $_.VMNetwork.ID -eq $vmNetwork.ID
    }

    $module.Diff.before = if ($vmSubnet) {
        @{
            name = $vmSubnet.Name
            vm_network = $vmSubnet.VMNetwork.Name
            subnet = $vmSubnet.Subnet
            vlan_id = $vmSubnet.VLanID
        }
    }
    else {
        @{}
    }

    if ($state -eq "present") {
        if (-not $vmSubnet) {
            $params = @{
                VMMServer = $vmmServer
                Name = $name
                VMNetwork = $vmNetwork
            }

            if ($subnet) {
                $params.Subnet = $subnet
            }

            if ($vlanId) {
                $params.VLanID = $vlanId
            }

            if (-not $module.CheckMode) {
                $vmSubnet = New-SCVMSubnet @params -ErrorAction Stop
            }
            $module.Result.changed = $true
        }
        else {
            $changed = $false
            $params = @{
                VMSubnet = $vmSubnet
            }

            if ($subnet -and $vmSubnet.Subnet -ne $subnet) {
                $changed = $true
                $params.Subnet = $subnet
            }

            if ($vlanId -and $vmSubnet.VLanID -ne $vlanId) {
                $changed = $true
                $params.VLanID = $vlanId
            }

            if ($changed -and -not $module.CheckMode) {
                $vmSubnet = Set-SCVMSubnet @params -ErrorAction Stop
            }

            $module.Result.changed = $changed
        }

        $module.Diff.after = @{
            name = $name
            vm_network = $vmNetworkName
            subnet = $subnet
            vlan_id = $vlanId
        }

        if ($vmSubnet) {
            $module.Result.vm_subnet = ConvertTo-SCVMMDict -InputObject $vmSubnet -Properties @('Name', 'VMNetwork', 'Subnet', 'VLanID', 'ID')
        }
    }
    else {
        if ($vmSubnet) {
            if (-not $module.CheckMode) {
                Remove-SCVMSubnet -VMSubnet $vmSubnet -ErrorAction Stop
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = @{}
    }

}

catch {
    $module.FailJson("Failed to manage VM subnet: $($_.Exception.Message)", $_)
}

$module.ExitJson()
