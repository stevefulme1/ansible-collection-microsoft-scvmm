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
    }
    supports_check_mode = $true
}
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$props = @("Name", "Description", "ID")
$vmmServer = Connect-SCVMM -Module $module

$pc = Get-SCPortClassification -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue
$before = @{}
if ($pc) { $before = ConvertTo-SCVMMDict -InputObject $pc -Properties $props }

if ($state -eq "present") {
    if (-not $pc) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{ VMMServer = $vmmServer; Name = $name; ErrorAction = "Stop" }
            if ($module.Params.description) { $params.Description = $module.Params.description }
            try { $pc = New-SCPortClassification @params }
            catch { $module.FailJson("Failed to create port classification '$name': $($_.Exception.Message)", $_) }
        }
    } else {
        $changed = $false
        $setParams = @{ PortClassification = $pc; ErrorAction = "Stop" }
        if ($module.Params.description -and $pc.Description -ne $module.Params.description) {
            $setParams.Description = $module.Params.description; $changed = $true
        }
        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                try { $pc = Set-SCPortClassification @setParams }
                catch { $module.FailJson("Failed to update port classification '$name': $($_.Exception.Message)", $_) }
            }
        }
    }
    $after = @{}
    if ($pc) { $after = ConvertTo-SCVMMDict -InputObject $pc -Properties $props }
    $module.Result.port_classification = $after
} else {
    if ($pc) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try { Remove-SCPortClassification -PortClassification $pc -ErrorAction Stop }
            catch { $module.FailJson("Failed to remove port classification '$name': $($_.Exception.Message)", $_) }
        }
    }
    $after = @{}
}

if ($module.DiffMode) { $module.Diff.before = $before; $module.Diff.after = $after }
$module.ExitJson()
