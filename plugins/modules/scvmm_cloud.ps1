#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        description = @{ type = 'str' }
        host_group = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$hostGroup = $module.Params.host_group
$description = $module.Params.description

$cloudProps = @("Name", "Description", "HostGroup", "CreationTime", "ModifiedTime", "ID")

$vmmServer = Connect-SCVMM -Module $module

$cloud = Get-SCCloud -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

$before = @{}
if ($cloud) {
    $before = ConvertTo-SCVMMDict -InputObject $cloud -Properties $cloudProps
}

if ($state -eq "present") {
    if (-not $cloud) {
        if (-not $hostGroup) {
            $module.FailJson("host_group is required when creating a new cloud.")
        }

        $hg = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hostGroup -ErrorAction SilentlyContinue
        if (-not $hg) {
            $module.FailJson("Host group '$hostGroup' not found.")
        }

        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{
                VMMServer = $vmmServer
                Name = $name
                VMHostGroup = $hg
                ErrorAction = "Stop"
            }
            if ($description) {
                $params.Description = $description
            }
            try {
                $cloud = New-SCCloud @params
            }
            catch {
                $module.FailJson("Failed to create cloud '$name': $($_.Exception.Message)", $_)
            }
        }
    }
    else {
        $changed = $false
        $setParams = @{
            Cloud = $cloud
            ErrorAction = "Stop"
        }

        if ($description -and $cloud.Description -ne $description) {
            $setParams.Description = $description
            $changed = $true
        }

        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                try {
                    $cloud = Set-SCCloud @setParams
                }
                catch {
                    $module.FailJson("Failed to update cloud '$name': $($_.Exception.Message)", $_)
                }
            }
        }
    }

    $after = @{}
    if ($cloud) {
        $after = ConvertTo-SCVMMDict -InputObject $cloud -Properties $cloudProps
    }
    $module.Result.cloud = $after
}
else {
    if ($cloud) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try {
                Remove-SCCloud -Cloud $cloud -ErrorAction Stop
            }
            catch {
                $module.FailJson("Failed to remove cloud '$name': $($_.Exception.Message)", $_)
            }
        }
    }
    $after = @{}
}

if ($module.DiffMode) {
    $module.Diff.before = $before
    $module.Diff.after = $after
}

$module.ExitJson()
