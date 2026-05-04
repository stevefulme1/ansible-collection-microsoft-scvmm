#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        vm_name = @{ type = 'str'; required = $true }
        bus = @{ type = 'int'; required = $true }
        lun = @{ type = 'int'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        size_gb = @{ type = 'int' }
        dynamic = @{ type = 'bool'; default = $false }
        file_name = @{ type = 'str' }
    }
    required_if = @(
        @('state', 'present', @('size_gb'))
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.vm_name -ErrorAction Stop

    $existing = Get-SCVirtualDiskDrive -VM $vm | Where-Object {
        $_.Bus -eq $module.Params.bus -and $_.Lun -eq $module.Params.lun
    }

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Bus', 'Lun', 'Size', 'FileName', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCVirtualDiskDrive -VirtualDiskDrive $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    else {
        if (-not $existing) {
            if (-not $module.CheckMode) {
                $newParams = @{
                    VM = $vm
                    Bus = $module.Params.bus
                    Lun = $module.Params.lun
                    VHDSizeGB = $module.Params.size_gb
                    Dynamic = $module.Params.dynamic
                    ErrorAction = 'Stop'
                }
                if ($module.Params.file_name) {
                    $newParams.FileName = $module.Params.file_name
                }
                $existing = New-SCVirtualDiskDrive @newParams
            }
            $module.Result.changed = $true
        }

        $module.Result.disk = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @(
                'Bus', 'Lun', 'Size', 'FileName', 'ID'
            )
        }
        else {
            @{
                Bus = $module.Params.bus
                Lun = $module.Params.lun
                Size = $module.Params.size_gb
                FileName = $module.Params.file_name
            }
        }
        $module.Diff.after = $module.Result.disk
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage VM disk: $($_.Exception.Message)", $_)
}
