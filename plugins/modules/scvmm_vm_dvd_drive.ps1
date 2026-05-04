#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        bus = @{ type = 'int'; default = 0 }
        iso = @{ type = 'str' }
        lun = @{ type = 'int'; default = 0 }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        vm_name = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.vm_name -ErrorAction Stop

    $existing = Get-SCVirtualDVDDrive -VM $vm | Where-Object {
        $_.Bus -eq $module.Params.bus -and $_.Lun -eq $module.Params.lun
    }

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Bus', 'Lun', 'ISO', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCVirtualDVDDrive -VirtualDVDDrive $existing -ErrorAction Stop
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
                    VM = $vm
                    Bus = $module.Params.bus
                    Lun = $module.Params.lun
                    ErrorAction = 'Stop'
                }

                if ($module.Params.iso_path) {
                    $iso = Get-SCISO -VMMServer $vmmServer | Where-Object { $_.SharePath -eq $module.Params.iso_path }
                    if ($iso) {
                        $newParams.ISO = $iso
                    }
                }

                $existing = New-SCVirtualDVDDrive @newParams
            }
            $needsChange = $true
        }
        else {
            if ($module.Params.iso_path) {
                $currentISO = if ($existing.ISO) { $existing.ISO.SharePath } else { $null }
                if ($currentISO -ne $module.Params.iso_path) {
                    if (-not $module.CheckMode) {
                        $iso = Get-SCISO -VMMServer $vmmServer | Where-Object { $_.SharePath -eq $module.Params.iso_path }
                        if ($iso) {
                            Set-SCVirtualDVDDrive -VirtualDVDDrive $existing -ISO $iso -ErrorAction Stop
                            $existing = Get-SCVirtualDVDDrive -VM $vm | Where-Object {
                                $_.Bus -eq $module.Params.bus -and $_.Lun -eq $module.Params.lun
                            }
                        }
                    }
                    $needsChange = $true
                }
            }
        }

        $module.Result.changed = $needsChange
        $module.Result.dvd_drive = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @(
                'Bus', 'Lun', 'ISO', 'ID'
            )
        }
        else {
            @{
                Bus = $module.Params.bus
                Lun = $module.Params.lun
                ISO = $module.Params.iso_path
            }
        }
        $module.Diff.after = $module.Result.dvd_drive
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage VM DVD drive: $($_.Exception.Message)", $_)
}
