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
        service_template = @{ type = 'str' }
        cloud = @{ type = 'str' }
        description = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name
$state = $module.Params.state
$serviceTemplate = $module.Params.service_template
$cloud = $module.Params.cloud
$description = $module.Params.description

$current = Get-SCService -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

if ($state -eq 'present') {
    if ($null -eq $current) {
        $module.Diff.before = @{}
        $params = @{
            VMMServer = $vmmServer
            Name = $name
            ErrorAction = 'Stop'
        }
        if ($null -ne $description) { $params.Description = $description }
        if ($null -ne $serviceTemplate) {
            $template = Get-SCServiceTemplate -VMMServer $vmmServer -Name $serviceTemplate -ErrorAction Stop
            $params.ServiceTemplate = $template
        }
        if ($null -ne $cloud) {
            $cloudObj = Get-SCCloud -VMMServer $vmmServer -Name $cloud -ErrorAction Stop
            $params.Cloud = $cloudObj
        }

        if (-not $module.CheckMode) {
            $result = New-SCService @params
            $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'Status', 'ID')
        }
        else {
            $module.Diff.after = @{ Name = $name }
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'Status', 'ID')
        $needsUpdate = $false
        $params = @{ ErrorAction = 'Stop' }

        if ($null -ne $description -and $current.Description -ne $description) {
            $needsUpdate = $true
            $params.Description = $description
        }

        if ($needsUpdate) {
            if (-not $module.CheckMode) {
                $result = Set-SCService -Service $current @params
                $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'Description', 'Status', 'ID')
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
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'Description', 'Status', 'ID')
        $module.Diff.after = @{}

        if (-not $module.CheckMode) {
            Remove-SCService -Service $current -ErrorAction Stop
        }
        $module.Result.changed = $true
    }
    else {
        $module.Diff.before = @{}
        $module.Diff.after = @{}
    }
}

$module.ExitJson()
