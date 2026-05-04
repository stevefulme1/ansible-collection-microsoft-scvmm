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
        mac_range_start = @{ type = "str" }
        mac_range_end = @{ type = "str" }
        description = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$poolProps = @("Name", "Description", "MACAddressRangeStart", "MACAddressRangeEnd", "ID")

$vmmServer = Connect-SCVMM -Module $module

$pool = Get-SCMACAddressPool -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

$before = @{}
if ($pool) { $before = ConvertTo-SCVMMDict -InputObject $pool -Properties $poolProps }

if ($state -eq "present") {
    if (-not $pool) {
        if (-not $module.Params.mac_range_start -or -not $module.Params.mac_range_end) {
            $module.FailJson("mac_range_start and mac_range_end are required when creating a MAC pool.")
        }
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{
                VMMServer = $vmmServer
                Name = $name
                MACAddressRangeStart = $module.Params.mac_range_start
                MACAddressRangeEnd = $module.Params.mac_range_end
                ErrorAction = "Stop"
            }
            if ($module.Params.description) { $params.Description = $module.Params.description }
            try { $pool = New-SCMACAddressPool @params }
            catch { $module.FailJson("Failed to create MAC pool '$name': $($_.Exception.Message)", $_) }
        }
    }
    else {
        $changed = $false
        $setParams = @{ MACAddressPool = $pool; ErrorAction = "Stop" }
        if ($module.Params.description -and $pool.Description -ne $module.Params.description) {
            $setParams.Description = $module.Params.description; $changed = $true
        }
        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                try { $pool = Set-SCMACAddressPool @setParams }
                catch { $module.FailJson("Failed to update MAC pool '$name': $($_.Exception.Message)", $_) }
            }
        }
    }
    $after = @{}
    if ($pool) { $after = ConvertTo-SCVMMDict -InputObject $pool -Properties $poolProps }
    $module.Result.mac_pool = $after
}
else {
    if ($pool) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try { Remove-SCMACAddressPool -MACAddressPool $pool -ErrorAction Stop }
            catch { $module.FailJson("Failed to remove MAC pool '$name': $($_.Exception.Message)", $_) }
        }
    }
    $after = @{}
}

if ($module.DiffMode) { $module.Diff.before = $before; $module.Diff.after = $after }
$module.ExitJson()
