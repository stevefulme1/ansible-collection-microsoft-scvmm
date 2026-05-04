#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        description = @{ type = 'str' }
        name = @{ type = 'str' }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent', 'restored') }
        vm_name = @{ type = 'str'; required = $true }
    }
)
        @('state', 'restored', @('name'))
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.vm_name -ErrorAction Stop

    $existing = if ($module.Params.name) {
        Get-SCVMCheckpoint -VM $vm -Name $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        $null
    }

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'VM', 'CreationTime', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCVMCheckpoint -VMCheckpoint $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    elseif ($module.Params.state -eq 'restored') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Restore-SCVMCheckpoint -VMCheckpoint $existing -ErrorAction Stop
                $existing = Get-SCVMCheckpoint -VM $vm -Name $module.Params.name -ErrorAction SilentlyContinue
            }
            $module.Result.changed = $true
            $module.Result.checkpoint = ConvertTo-SCVMMDict -InputObject $existing -Properties @(
                'Name', 'Description', 'VM', 'CreationTime', 'ID'
            )
            $module.Diff.after = $module.Result.checkpoint
        }
        else {
            $module.FailJson("Checkpoint '$($module.Params.name)' not found on VM '$($module.Params.vm_name)'")
        }
    }
    else {
        if (-not $existing) {
            if (-not $module.CheckMode) {
                $newParams = @{
                    VM = $vm
                    Name = $module.Params.name
                    ErrorAction = 'Stop'
                }
                if ($module.Params.description) {
                    $newParams.Description = $module.Params.description
                }
                $existing = New-SCVMCheckpoint @newParams
            }
            $module.Result.changed = $true
        }

        $module.Result.checkpoint = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @(
                'Name', 'Description', 'VM', 'CreationTime', 'ID'
            )
        }
        else {
            @{
                Name = $module.Params.name
                Description = $module.Params.description
                VM = $module.Params.vm_name
            }
        }
        $module.Diff.after = $module.Result.checkpoint
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage VM checkpoint: $($_.Exception.Message)", $_)
}
