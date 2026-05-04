#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        disk_type = @{ type = 'str'; default = 'Dynamic'; choices = @('Dynamic', 'Fixed') }
        format = @{ type = 'str'; default = 'VHDX'; choices = @('VHD', 'VHDX') }
        name = @{ type = 'str'; required = $true }
        path = @{ type = 'str' }
        size_gb = @{ type = 'int' }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name
$state = $module.Params.state
$description = $module.Params.description
$vhdType = $module.Params.vhd_type
$sizeGB = $module.Params.size_gb

$current = Get-SCVirtualHardDisk -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

if ($state -eq 'present') {
    if ($null -eq $current) {
        $module.Diff.before = @{}
        $params = @{
            VMMServer = $vmmServer
            Name = $name
            ErrorAction = 'Stop'
        }
        if ($null -ne $description) { $params.Description = $description }
        if ($null -ne $vhdType) { $params.VHDType = $vhdType }
        if ($null -ne $sizeGB) { $params.MaximumSize = $sizeGB }

        if (-not $module.CheckMode) {
            $result = New-SCVirtualHardDisk @params
            $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'VHDType', 'MaximumSize', 'Location', 'ID')
        }
        else {
            $module.Diff.after = @{ Name = $name }
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'VHDType', 'MaximumSize', 'Location', 'ID')
        $needsUpdate = $false
        $params = @{ ErrorAction = 'Stop' }

        if ($null -ne $description -and $current.Description -ne $description) {
            $needsUpdate = $true
            $params.Description = $description
        }

        if ($needsUpdate) {
            if (-not $module.CheckMode) {
                $result = Set-SCVirtualHardDisk -VirtualHardDisk $current @params
                $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'VHDType', 'MaximumSize', 'Location', 'ID')
            }
            else {
                $module.Diff.after = $module.Diff.before.Clone()
                foreach ($key in $params.Keys) {
                    if ($key -ne 'ErrorAction') {
                        $module.Diff.after[$key] = $params[$key]
                    }
                }
            }
            $module.Result.changed = $true
        }
        else {
            $module.Diff.after = $module.Diff.before
        }
    }
}
else {
    if ($null -ne $current) {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'VHDType', 'MaximumSize', 'Location', 'ID')
        $module.Diff.after = @{}

        if (-not $module.CheckMode) {
            Remove-SCVirtualHardDisk -VirtualHardDisk $current -ErrorAction Stop
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = @{}
        $module.Diff.after = @{}
    }
}

$module.ExitJson()
