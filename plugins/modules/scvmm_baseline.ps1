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
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $existing = Get-SCBaseline -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'BaselineType', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCBaseline -Baseline $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    else {
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
                $existing = New-SCBaseline @newParams
            }
            $needsChange = $true
        }
        else {
            $setParams = @{}
            if ($module.Params.description -and $existing.Description -ne $module.Params.description) {
                $setParams.Description = $module.Params.description
                $needsChange = $true
            }
            if ($setParams.Count -gt 0 -and -not $module.CheckMode) {
                Set-SCBaseline -Baseline $existing @setParams -ErrorAction Stop
                $existing = Get-SCBaseline -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
            }
        }

        $module.Result.changed = $needsChange
        $module.Diff.after = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'BaselineType', 'ID')
        }
        else {
            @{
                Name = $module.Params.name
                Description = $module.Params.description
            }
        }
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage baseline: $($_.Exception.Message)", $_)
}
