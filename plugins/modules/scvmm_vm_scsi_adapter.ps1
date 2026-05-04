#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        vm_name = @{ type = 'str'; required = $true }
        adapter_id = @{ type = 'int'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        shared = @{ type = 'bool'; default = $false }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.vm_name -ErrorAction Stop

    $existing = Get-SCVirtualSCSIAdapter -VM $vm | Where-Object { $_.AdapterID -eq $module.Params.adapter_id }

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('AdapterID', 'Shared', 'ID')
    } else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCVirtualSCSIAdapter -VirtualSCSIAdapter $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    } else {
        $needsChange = $false

        if (-not $existing) {
            if (-not $module.CheckMode) {
                $newParams = @{
                    VM = $vm
                    AdapterID = $module.Params.adapter_id
                    Shared = $module.Params.shared
                    ErrorAction = 'Stop'
                }
                $existing = New-SCVirtualSCSIAdapter @newParams
            }
            $needsChange = $true
        } else {
            if ($existing.Shared -ne $module.Params.shared) {
                if (-not $module.CheckMode) {
                    Set-SCVirtualSCSIAdapter -VirtualSCSIAdapter $existing -Shared $module.Params.shared -ErrorAction Stop
                    $existing = Get-SCVirtualSCSIAdapter -VM $vm | Where-Object { $_.AdapterID -eq $module.Params.adapter_id }
                }
                $needsChange = $true
            }
        }

        $module.Result.changed = $needsChange
        $module.Result.scsi_adapter = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @(
                'AdapterID', 'Shared', 'ID'
            )
        } else {
            @{
                AdapterID = $module.Params.adapter_id
                Shared = $module.Params.shared
            }
        }
        $module.Diff.after = $module.Result.scsi_adapter
    }

    $module.ExitJson()
} catch {
    $module.FailJson("Failed to manage VM SCSI adapter: $($_.Exception.Message)", $_)
}
