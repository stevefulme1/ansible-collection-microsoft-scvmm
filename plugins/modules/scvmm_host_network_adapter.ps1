#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        vm_host = @{ required = $true; type = "str" }
        name = @{ required = $true; type = "str" }
        logical_network = @{ type = "str" }
        uplink_port_profile = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$vmHostName = $module.Params.vm_host
$name = $module.Params.name
$logicalNetwork = $module.Params.logical_network
$uplinkPortProfile = $module.Params.uplink_port_profile

try {
    $vmmServer = Connect-SCVMM -Module $module

    $vmHost = Get-SCVMHost -VMMServer $vmmServer -ComputerName $vmHostName -ErrorAction Stop

    $adapter = Get-SCVMHostNetworkAdapter -VMHost $vmHost -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -eq $name -or $_.ConnectionName -eq $name
    }

    if (-not $adapter) {
        $module.FailJson("Network adapter '$name' not found on host '$vmHostName'")
    }

    $module.Diff.before = @{
        name = $adapter.Name
        logical_network = if ($adapter.LogicalNetwork) { $adapter.LogicalNetwork.Name } else { $null }
    }

    $changed = $false
    $params = @{
        VMHostNetworkAdapter = $adapter
    }

    if ($logicalNetwork) {
        $logNet = Get-SCLogicalNetwork -VMMServer $vmmServer -Name $logicalNetwork -ErrorAction Stop
        if ($adapter.LogicalNetwork.ID -ne $logNet.ID) {
            $changed = $true
            $params.LogicalNetwork = $logNet
        }
    }

    if ($uplinkPortProfile) {
        $profile = Get-SCUplinkPortProfile -VMMServer $vmmServer -Name $uplinkPortProfile -ErrorAction Stop
        $params.UplinkPortProfileSet = $profile
        $changed = $true
    }

    if ($changed -and -not $module.CheckMode) {
        $adapter = Set-SCVMHostNetworkAdapter @params -ErrorAction Stop
    }

    $module.Result.changed = $changed

    $module.Diff.after = @{
        name = $name
        logical_network = $logicalNetwork
    }

    $module.Result.network_adapter = ConvertTo-SCVMMDict -InputObject $adapter -Properties @(
        'Name', 'ConnectionName', 'VMHost', 'LogicalNetwork', 'MaxBandwidth', 'ID'
    )

}

catch {
    $module.FailJson("Failed to manage host network adapter: $($_.Exception.Message)", $_)
}

$module.ExitJson()
