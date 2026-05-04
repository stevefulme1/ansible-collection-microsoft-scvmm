#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        name = @{ required = $true; type = "str" }
        state = @{ type = "str"; choices = @("present", "absent"); default = "present" }
        description = @{ type = "str" }
        switch_uplink_mode = @{ type = "str"; choices = @("NoTeam", "Team", "EmbeddedTeam") }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$switchProps = @("Name", "Description", "SwitchUplinkMode", "ID")

$vmmServer = Connect-SCVMM -Module $module

$switch = Get-SCLogicalSwitch -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

$before = @{}
if ($switch) {
    $before = ConvertTo-SCVMMDict -InputObject $switch -Properties $switchProps
}

if ($state -eq "present") {
    if (-not $switch) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{
                VMMServer = $vmmServer
                Name = $name
                ErrorAction = "Stop"
            }
            if ($module.Params.description) { $params.Description = $module.Params.description }
            if ($module.Params.switch_uplink_mode) { $params.SwitchUplinkMode = $module.Params.switch_uplink_mode }
            try {
                $switch = New-SCLogicalSwitch @params
            }
            catch {
                $module.FailJson("Failed to create logical switch '$name': $($_.Exception.Message)", $_)
            }
        }
    }
    else {
        $changed = $false
        $setParams = @{ LogicalSwitch = $switch; ErrorAction = "Stop" }
        if ($module.Params.description -and $switch.Description -ne $module.Params.description) {
            $setParams.Description = $module.Params.description; $changed = $true
        }
        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                try { $switch = Set-SCLogicalSwitch @setParams }
                catch { $module.FailJson("Failed to update logical switch '$name': $($_.Exception.Message)", $_) }
            }
        }
    }
    $after = @{}
    if ($switch) { $after = ConvertTo-SCVMMDict -InputObject $switch -Properties $switchProps }
    $module.Result.logical_switch = $after
}
else {
    if ($switch) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try { Remove-SCLogicalSwitch -LogicalSwitch $switch -ErrorAction Stop }
            catch { $module.FailJson("Failed to remove logical switch '$name': $($_.Exception.Message)", $_) }
        }
    }
    $after = @{}
}

if ($module.DiffMode) { $module.Diff.before = $before; $module.Diff.after = $after }
$module.ExitJson()
