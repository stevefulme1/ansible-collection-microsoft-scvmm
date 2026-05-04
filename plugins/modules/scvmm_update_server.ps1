#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        credential = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        port = @{ type = 'int'; default = 8530 }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        use_ssl = @{ type = 'bool'; default = $false }
    }
    required_if = @(
        @('state', 'present', @('computer_name'))
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $existing = Get-SCUpdateServer -VMMServer $vmmServer -ComputerName $module.Params.name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'ComputerName', 'Port', 'IsConnectionSuccessful', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCUpdateServer -UpdateServer $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    else {
        $needsChange = $false

        if (-not $existing) {
            if (-not $module.CheckMode) {
                $addParams = @{
                    VMMServer = $vmmServer
                    ComputerName = $module.Params.computer_name
                    ErrorAction = 'Stop'
                }
                if ($module.Params.credential) {
                    $addParams.Credential = $module.Params.credential
                }
                if ($module.Params.port) {
                    $addParams.TCPPort = $module.Params.port
                }
                $existing = Add-SCUpdateServer @addParams
            }
            $needsChange = $true
        }
        else {
            $setParams = @{}
            if ($module.Params.port -and $existing.Port -ne $module.Params.port) {
                $setParams.TCPPort = $module.Params.port
                $needsChange = $true
            }
            if ($setParams.Count -gt 0 -and -not $module.CheckMode) {
                Set-SCUpdateServer -UpdateServer $existing @setParams -ErrorAction Stop
                $existing = Get-SCUpdateServer -VMMServer $vmmServer -ComputerName $module.Params.name -ErrorAction SilentlyContinue
            }
        }

        $module.Result.changed = $needsChange
        $module.Diff.after = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'ComputerName', 'Port', 'IsConnectionSuccessful', 'ID')
        }
        else {
            @{
                Name = $module.Params.name
                ComputerName = $module.Params.computer_name
                Port = $module.Params.port
            }
        }
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage update server: $($_.Exception.Message)", $_)
}
