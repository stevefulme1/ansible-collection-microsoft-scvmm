#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        description = @{ type = 'str' }
        members = @{ type = 'list'; elements = 'str' }
        name = @{ type = 'str'; required = $true }
        profile = @{ type = 'str'; choices = @('Administrator', 'DelegatedAdmin', 'ReadOnlyAdmin', 'SelfServiceUser', 'TenantAdmin') }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    required_if = @(
        @('state', 'present', @('profile'))
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $existing = Get-SCUserRole -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'Profile', 'Members', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCUserRole -UserRole $existing -ErrorAction Stop
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
                    VMMServer = $vmmServer
                    Name = $module.Params.name
                    UserRoleProfile = $module.Params.profile
                    ErrorAction = 'Stop'
                }
                if ($module.Params.description) {
                    $newParams.Description = $module.Params.description
                }
                if ($module.Params.members) {
                    $newParams.UserName = $module.Params.members
                }
                $existing = New-SCUserRole @newParams
            }
            $needsChange = $true
        }
        else {
            $setParams = @{}
            if ($module.Params.description -and $existing.Description -ne $module.Params.description) {
                $setParams.Description = $module.Params.description
                $needsChange = $true
            }
            if ($module.Params.members) {
                $currentMembers = @($existing.Members)
                $desiredMembers = @($module.Params.members)
                $membersDiffer = ($currentMembers.Count -ne $desiredMembers.Count) -or
                                 ($currentMembers | Where-Object { $_ -notin $desiredMembers }).Count -gt 0
                if ($membersDiffer) {
                    $setParams.AddMember = $desiredMembers
                    $needsChange = $true
                }
            }
            if ($setParams.Count -gt 0 -and -not $module.CheckMode) {
                Set-SCUserRole -UserRole $existing @setParams -ErrorAction Stop
                $existing = Get-SCUserRole -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
            }
        }

        $module.Result.changed = $needsChange
        $module.Diff.after = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'Profile', 'Members', 'ID')
        }
        else {
            @{
                Name = $module.Params.name
                Description = $module.Params.description
                Profile = $module.Params.profile
                Members = $module.Params.members
            }
        }
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage user role: $($_.Exception.Message)", $_)
}
