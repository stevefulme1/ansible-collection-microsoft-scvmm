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
        description = @{ type = 'str' }
        os_type = @{ type = 'str' }
        computer_name = @{ type = 'str' }
        admin_password = @{ type = 'str'; no_log = $true }
        timezone = @{ type = 'int' }
        domain = @{ type = 'str' }
        domain_admin_credential = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name
$state = $module.Params.state
$description = $module.Params.description
$osType = $module.Params.os_type
$computerName = $module.Params.computer_name
$adminPassword = $module.Params.admin_password
$timezone = $module.Params.timezone
$domain = $module.Params.domain
$domainAdminCredential = $module.Params.domain_admin_credential

$current = Get-SCGuestOSProfile -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

if ($state -eq 'present') {
    if ($null -eq $current) {
        $module.Diff.before = @{}
        $params = @{
            VMMServer = $vmmServer
            Name = $name
            ErrorAction = 'Stop'
        }
        if ($null -ne $description) { $params.Description = $description }
        if ($null -ne $osType) { $params.OperatingSystem = $osType }
        if ($null -ne $computerName) { $params.ComputerName = $computerName }
        if ($null -ne $timezone) { $params.TimeZone = $timezone }
        if ($null -ne $domain) { $params.Domain = $domain }

        if (-not $module.CheckMode) {
            $result = New-SCGuestOSProfile @params
            $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'OperatingSystem', 'ComputerName', 'TimeZone', 'ID')
        } else {
            $module.Diff.after = @{ Name = $name }
        }
        $module.Result.changed = $true
    } else {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'OperatingSystem', 'ComputerName', 'TimeZone', 'ID')
        $needsUpdate = $false
        $params = @{ ErrorAction = 'Stop' }

        if ($null -ne $description -and $current.Description -ne $description) {
            $needsUpdate = $true
            $params.Description = $description
        }
        if ($null -ne $computerName -and $current.ComputerName -ne $computerName) {
            $needsUpdate = $true
            $params.ComputerName = $computerName
        }
        if ($null -ne $timezone -and $current.TimeZone -ne $timezone) {
            $needsUpdate = $true
            $params.TimeZone = $timezone
        }

        if ($needsUpdate) {
            if (-not $module.CheckMode) {
                $result = Set-SCGuestOSProfile -GuestOSProfile $current @params
                $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'OperatingSystem', 'ComputerName', 'TimeZone', 'ID')
            } else {
                $module.Diff.after = $module.Diff.before.Clone()
                foreach ($key in $params.Keys) {
                    if ($key -ne 'ErrorAction') {
                        $module.Diff.after[$key] = $params[$key]
                    }
                }
            }
            $module.Result.changed = $true
        } else {
            $module.Diff.after = $module.Diff.before
        }
    }
} else {
    if ($null -ne $current) {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'OperatingSystem', 'ComputerName', 'TimeZone', 'ID')
        $module.Diff.after = @{}

        if (-not $module.CheckMode) {
            Remove-SCGuestOSProfile -GuestOSProfile $current -ErrorAction Stop
        }
        $module.Result.changed = $true
    } else {
        $module.Diff.before = @{}
        $module.Diff.after = @{}
    }
}

$module.ExitJson()
