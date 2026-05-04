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
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
)
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $existing = Get-SCPXEServer -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'ComputerName', 'State', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCPXEServer -PXEServer $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    else {
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
                $existing = Add-SCPXEServer @addParams
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'ComputerName', 'State', 'ID')
        }
        else {
            @{
                Name = $module.Params.name
                ComputerName = $module.Params.computer_name
            }
        }
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage PXE server: $($_.Exception.Message)", $_)
}
