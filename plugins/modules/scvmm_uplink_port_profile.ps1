#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        load_balancing_algorithm = @{ type = 'str'; choices = @('HostDefault', 'HyperVPort', 'Dynamic', 'TransportPorts', 'IPAddresses', 'MACAddresses') }
        logical_network_definitions = @{ type = 'list'; elements = 'str' }
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$props = @("Name", "Description", "LoadBalancingAlgorithm", "TeamingMode", "ID")
$vmmServer = Connect-SCVMM -Module $module

$uplinkProfile = Get-SCNativeUplinkPortProfile -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue
$before = @{}
if ($uplinkProfile) { $before = ConvertTo-SCVMMDict -InputObject $uplinkProfile -Properties $props }

if ($state -eq "present") {
    if (-not $uplinkProfile) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{ VMMServer = $vmmServer; Name = $name; ErrorAction = "Stop" }
            if ($module.Params.description) { $params.Description = $module.Params.description }
            if ($module.Params.load_balancing_algorithm) { $params.LoadBalancingAlgorithm = $module.Params.load_balancing_algorithm }
            if ($module.Params.teaming_mode) { $params.TeamingMode = $module.Params.teaming_mode }
            try { $uplinkProfile = New-SCNativeUplinkPortProfile @params }
            catch { $module.FailJson("Failed to create uplink profile '$name': $($_.Exception.Message)", $_) }
        }
    }
    else {
        $changed = $false
        $setParams = @{ NativeUplinkPortProfile = $uplinkProfile; ErrorAction = "Stop" }
        if ($module.Params.description -and $uplinkProfile.Description -ne $module.Params.description) {
            $setParams.Description = $module.Params.description; $changed = $true
        }
        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                try { $uplinkProfile = Set-SCNativeUplinkPortProfile @setParams }
                catch { $module.FailJson("Failed to update uplink profile '$name': $($_.Exception.Message)", $_) }
            }
        }
    }
    $after = @{}
    if ($uplinkProfile) { $after = ConvertTo-SCVMMDict -InputObject $uplinkProfile -Properties $props }
    $module.Result.uplink_profile = $after
}
else {
    if ($uplinkProfile) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try { Remove-SCNativeUplinkPortProfile -NativeUplinkPortProfile $uplinkProfile -ErrorAction Stop }
            catch { $module.FailJson("Failed to remove uplink profile '$name': $($_.Exception.Message)", $_) }
        }
    }
    $after = @{}
}

if ($module.DiffMode) { $module.Diff.before = $before; $module.Diff.after = $after }
$module.ExitJson()
