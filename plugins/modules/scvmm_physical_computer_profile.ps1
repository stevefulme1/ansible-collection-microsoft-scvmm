#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        computer_access_credential = @{ type = 'str' }
        description = @{ type = 'str' }
        hardware_profile = @{ type = 'str' }
        host_group = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        operating_system = @{ type = 'str' }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name
$state = $module.Params.state
$description = $module.Params.description
$bootOrder = $module.Params.boot_order
$biosGuid = $module.Params.bios_guid

$current = Get-SCPhysicalComputerProfile -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

if ($state -eq 'present') {
    if ($null -eq $current) {
        $module.Diff.before = @{}
        $params = @{
            VMMServer = $vmmServer
            Name = $name
            ErrorAction = 'Stop'
        }
        if ($null -ne $description) { $params.Description = $description }
        if ($null -ne $bootOrder) { $params.BootOrder = $bootOrder }
        if ($null -ne $biosGuid) { $params.BiosGuid = $biosGuid }

        if (-not $module.CheckMode) {
            $result = New-SCPhysicalComputerProfile @params
            $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'BootOrder', 'BiosGuid', 'ID')
        }
        else {
            $module.Diff.after = @{ Name = $name }
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'BootOrder', 'BiosGuid', 'ID')
        $needsUpdate = $false
        $params = @{ ErrorAction = 'Stop' }

        if ($null -ne $description -and $current.Description -ne $description) {
            $needsUpdate = $true
            $params.Description = $description
        }

        if ($needsUpdate) {
            if (-not $module.CheckMode) {
                $result = Set-SCPhysicalComputerProfile -PhysicalComputerProfile $current @params
                $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'BootOrder', 'BiosGuid', 'ID')
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
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'BootOrder', 'BiosGuid', 'ID')
        $module.Diff.after = @{}

        if (-not $module.CheckMode) {
            Remove-SCPhysicalComputerProfile -PhysicalComputerProfile $current -ErrorAction Stop
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = @{}
        $module.Diff.after = @{}
    }
}

$module.ExitJson()
