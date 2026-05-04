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
        description = @{ type = 'str' }
        start_date = @{ type = 'str' }
        end_date = @{ type = 'str' }
        time_zone = @{ type = 'str' }
        category = @{ type = 'str'; choices = @('None', 'OwnerServiceAgreement', 'ChangeRequestTicket') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $existing = Get-SCServicingWindow -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'StartDate', 'EndDate', 'TimeZone', 'Category', 'ID')
    } else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCServicingWindow -ServicingWindow $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    } else {
        $needsChange = $false

        if (-not $existing) {
            if (-not $module.CheckMode) {
                $newParams = @{
                    VMMServer = $vmmServer
                    Name = $module.Params.name
                    ErrorAction = 'Stop'
                }
                if ($module.Params.description) {
                    $newParams.Description = $module.Params.description
                }
                if ($module.Params.start_date) {
                    $newParams.StartDate = [DateTime]::Parse($module.Params.start_date)
                }
                if ($module.Params.end_date) {
                    $newParams.EndDate = [DateTime]::Parse($module.Params.end_date)
                }
                if ($module.Params.time_zone) {
                    $newParams.TimeZone = $module.Params.time_zone
                }
                if ($module.Params.category) {
                    $newParams.Category = $module.Params.category
                }
                $existing = New-SCServicingWindow @newParams
            }
            $needsChange = $true
        } else {
            $setParams = @{}
            if ($module.Params.description -and $existing.Description -ne $module.Params.description) {
                $setParams.Description = $module.Params.description
                $needsChange = $true
            }
            if ($module.Params.start_date) {
                $desiredStart = [DateTime]::Parse($module.Params.start_date)
                if ($existing.StartDate -ne $desiredStart) {
                    $setParams.StartDate = $desiredStart
                    $needsChange = $true
                }
            }
            if ($module.Params.end_date) {
                $desiredEnd = [DateTime]::Parse($module.Params.end_date)
                if ($existing.EndDate -ne $desiredEnd) {
                    $setParams.EndDate = $desiredEnd
                    $needsChange = $true
                }
            }
            if ($setParams.Count -gt 0 -and -not $module.CheckMode) {
                Set-SCServicingWindow -ServicingWindow $existing @setParams -ErrorAction Stop
                $existing = Get-SCServicingWindow -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
            }
        }

        $module.Result.changed = $needsChange
        $module.Diff.after = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'StartDate', 'EndDate', 'TimeZone', 'Category', 'ID')
        } else {
            @{
                Name = $module.Params.name
                Description = $module.Params.description
                StartDate = $module.Params.start_date
                EndDate = $module.Params.end_date
                TimeZone = $module.Params.time_zone
                Category = $module.Params.category
            }
        }
    }

    $module.ExitJson()
} catch {
    $module.FailJson("Failed to manage servicing window: $($_.Exception.Message)", $_)
}
