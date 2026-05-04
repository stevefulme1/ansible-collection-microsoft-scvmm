#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        force = @{ type = 'bool'; default = $false }
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; required = $true; choices = @('started', 'stopped', 'paused', 'saved', 'restarted') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.name -ErrorAction Stop

    $currentStatus = $vm.Status

    $needsChange = $false
    $actionTaken = $null

    if ($module.CheckMode) {
        if ($module.Params.state -eq 'restarted') {
            $needsChange = $true
            $actionTaken = 'would_restart'
        }
        elseif ($module.Params.state -eq 'started' -and $currentStatus -ne 'Running') {
            $needsChange = $true
            $actionTaken = 'would_start'
        }
        elseif ($module.Params.state -eq 'stopped' -and $currentStatus -ne 'PowerOff') {
            $needsChange = $true
            $actionTaken = 'would_stop'
        }
        elseif ($module.Params.state -eq 'paused' -and $currentStatus -ne 'Paused') {
            $needsChange = $true
            $actionTaken = 'would_pause'
        }
        elseif ($module.Params.state -eq 'saved' -and $currentStatus -ne 'Saved') {
            $needsChange = $true
            $actionTaken = 'would_save'
        }
    }
    else {
        switch ($module.Params.state) {
            'started' {
                if ($currentStatus -ne 'Running') {
                    Start-SCVirtualMachine -VM $vm -ErrorAction Stop | Out-Null
                    $needsChange = $true
                    $actionTaken = 'started'
                }
            }
            'stopped' {
                if ($currentStatus -ne 'PowerOff') {
                    if ($module.Params.force) {
                        Stop-SCVirtualMachine -VM $vm -Force -ErrorAction Stop | Out-Null
                    }
                    else {
                        Stop-SCVirtualMachine -VM $vm -ErrorAction Stop | Out-Null
                    }
                    $needsChange = $true
                    $actionTaken = 'stopped'
                }
            }
            'paused' {
                if ($currentStatus -ne 'Paused') {
                    Suspend-SCVirtualMachine -VM $vm -ErrorAction Stop | Out-Null
                    $needsChange = $true
                    $actionTaken = 'paused'
                }
            }
            'saved' {
                if ($currentStatus -ne 'Saved') {
                    Save-SCVirtualMachine -VM $vm -ErrorAction Stop | Out-Null
                    $needsChange = $true
                    $actionTaken = 'saved'
                }
            }
            'restarted' {
                if ($currentStatus -ne 'PowerOff') {
                    if ($module.Params.force) {
                        Stop-SCVirtualMachine -VM $vm -Force -ErrorAction Stop | Out-Null
                    }
                    else {
                        Stop-SCVirtualMachine -VM $vm -ErrorAction Stop | Out-Null
                    }
                }
                Start-SCVirtualMachine -VM $vm -ErrorAction Stop | Out-Null
                $needsChange = $true
                $actionTaken = 'restarted'
            }
        }

        $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.name -ErrorAction Stop
    }

    $module.Result.changed = $needsChange
    $module.Result.vm = ConvertTo-SCVMMDict -InputObject $vm -Properties @('Name', 'Status', 'ID')
    if ($actionTaken) {
        $module.Result.action = $actionTaken
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage VM state: $($_.Exception.Message)", $_)
}
