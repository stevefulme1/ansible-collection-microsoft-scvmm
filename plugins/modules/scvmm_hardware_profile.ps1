#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        cpu_count = @{ type = 'int' }
        memory_mb = @{ type = 'int' }
        description = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name
$state = $module.Params.state
$cpuCount = $module.Params.cpu_count
$memoryMB = $module.Params.memory_mb
$description = $module.Params.description

$current = Get-SCHardwareProfile -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

if ($state -eq 'present') {
    if ($null -eq $current) {
        $module.Diff.before = @{}
        $params = @{
            VMMServer = $vmmServer
            Name = $name
            ErrorAction = 'Stop'
        }
        if ($null -ne $cpuCount) { $params.CPUCount = $cpuCount }
        if ($null -ne $memoryMB) { $params.MemoryMB = $memoryMB }
        if ($null -ne $description) { $params.Description = $description }

        if (-not $module.CheckMode) {
            $result = New-SCHardwareProfile @params
            $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'CPUCount', 'MemoryMB', 'ID')
        }
        else {
            $module.Diff.after = @{ Name = $name }
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'CPUCount', 'MemoryMB', 'ID')
        $needsUpdate = $false
        $params = @{ ErrorAction = 'Stop' }

        if ($null -ne $cpuCount -and $current.CPUCount -ne $cpuCount) {
            $needsUpdate = $true
            $params.CPUCount = $cpuCount
        }
        if ($null -ne $memoryMB -and $current.MemoryMB -ne $memoryMB) {
            $needsUpdate = $true
            $params.MemoryMB = $memoryMB
        }
        if ($null -ne $description -and $current.Description -ne $description) {
            $needsUpdate = $true
            $params.Description = $description
        }

        if ($needsUpdate) {
            if (-not $module.CheckMode) {
                $result = Set-SCHardwareProfile -HardwareProfile $current @params
                $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'CPUCount', 'MemoryMB', 'ID')
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
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'CPUCount', 'MemoryMB', 'ID')
        $module.Diff.after = @{}

        if (-not $module.CheckMode) {
            Remove-SCHardwareProfile -HardwareProfile $current -ErrorAction Stop
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = @{}
        $module.Diff.after = @{}
    }
}

$module.ExitJson()
