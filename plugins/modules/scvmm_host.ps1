#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        credential = @{ type = 'str' }
        host_group = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        reassociate = @{ type = 'bool'; default = $false }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$credential = $module.Params.credential
$hostGroup = $module.Params.host_group
$reassociate = $module.Params.reassociate

try {
    $vmmServer = Connect-SCVMM -Module $module

    $vmHost = Get-SCVMHost -VMMServer $vmmServer -ComputerName $name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($vmHost) {
        @{
            name = $vmHost.Name
            computer_name = $vmHost.ComputerName
            host_group = $vmHost.VMHostGroup.Path
            overall_state = $vmHost.OverallState
        }
    }
    else {
        @{}
    }

    if ($state -eq "present") {
        if (-not $vmHost) {
            $params = @{
                VMMServer = $vmmServer
                ComputerName = $name
            }

            if ($credential) {
                $runAsAccount = Get-SCRunAsAccount -VMMServer $vmmServer -Name $credential -ErrorAction Stop
                $params.Credential = $runAsAccount
            }

            if ($hostGroup) {
                $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hostGroup -ErrorAction Stop
                $params.VMHostGroup = $vmHostGroup
            }

            if (-not $module.CheckMode) {
                $vmHost = Add-SCVMHost @params -ErrorAction Stop
            }
            $module.Result.changed = $true
        }
        else {
            $changed = $false

            if ($hostGroup) {
                $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hostGroup -ErrorAction Stop
                if ($vmHost.VMHostGroup.ID -ne $vmHostGroup.ID) {
                    $changed = $true
                    if (-not $module.CheckMode) {
                        $vmHost = Set-SCVMHost -VMHost $vmHost -VMHostGroup $vmHostGroup -ErrorAction Stop
                    }
                }
            }

            if ($reassociate) {
                $changed = $true
                if (-not $module.CheckMode) {
                    $params = @{
                        VMHost = $vmHost
                        Reassociate = $true
                    }
                    if ($credential) {
                        $runAsAccount = Get-SCRunAsAccount -VMMServer $vmmServer -Name $credential -ErrorAction Stop
                        $params.Credential = $runAsAccount
                    }
                    $vmHost = Set-SCVMHost @params -ErrorAction Stop
                }
            }

            $module.Result.changed = $changed
        }

        $module.Diff.after = @{
            name = $name
            computer_name = $name
            host_group = $hostGroup
        }

        if ($vmHost) {
            $props = @('Name', 'ComputerName', 'OperatingSystem', 'VMHostGroup', 'OverallState', 'CommunicationState', 'ID')
            $module.Result.host = ConvertTo-SCVMMDict -InputObject $vmHost -Properties $props
        }
    }
    else {
        if ($vmHost) {
            if (-not $module.CheckMode) {
                Remove-SCVMHost -VMHost $vmHost -ErrorAction Stop
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = @{}
    }

}

catch {
    $module.FailJson("Failed to manage VM host: $($_.Exception.Message)", $_)
}

$module.ExitJson()
