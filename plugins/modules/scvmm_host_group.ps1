#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        description = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        parent = @{ type = 'str'; default = 'All Hosts' }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$parent = $module.Params.parent
$description = $module.Params.description

try {
    $vmmServer = Connect-SCVMM -Module $module

    $hostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($hostGroup) {
        @{
            name = $hostGroup.Name
            description = $hostGroup.Description
            parent = $hostGroup.ParentHostGroup.Path
        }
    }
    else {
        @{}
    }

    if ($state -eq "present") {
        if (-not $hostGroup) {
            $parentGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $parent -ErrorAction Stop

            if (-not $module.CheckMode) {
                $params = @{
                    VMMServer = $vmmServer
                    Name = $name
                    ParentHostGroup = $parentGroup
                }
                if ($description) {
                    $params.Description = $description
                }
                $hostGroup = New-SCVMHostGroup @params -ErrorAction Stop
            }
            $module.Result.changed = $true
        }
        else {
            $changed = $false

            if ($description -and $hostGroup.Description -ne $description) {
                $changed = $true
            }

            $parentGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $parent -ErrorAction Stop
            if ($hostGroup.ParentHostGroup.ID -ne $parentGroup.ID) {
                $changed = $true
            }

            if ($changed -and -not $module.CheckMode) {
                $params = @{
                    VMMServer = $vmmServer
                    VMHostGroup = $hostGroup
                }
                if ($description) {
                    $params.Description = $description
                }
                $params.ParentHostGroup = $parentGroup
                $hostGroup = Set-SCVMHostGroup @params -ErrorAction Stop
            }
            $module.Result.changed = $changed
        }

        $module.Diff.after = @{
            name = $name
            description = $description
            parent = $parent
        }

        if ($hostGroup) {
            $props = @('Name', 'Description', 'Path', 'ParentHostGroup', 'CreationTime', 'ID')
            $module.Result.host_group = ConvertTo-SCVMMDict -InputObject $hostGroup -Properties $props
        }
    }
    else {
        if ($hostGroup) {
            if (-not $module.CheckMode) {
                Remove-SCVMHostGroup -VMHostGroup $hostGroup -ErrorAction Stop
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = @{}
    }

}

catch {
    $module.FailJson("Failed to manage host group: $($_.Exception.Message)", $_)
}

$module.ExitJson()
