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
        network_virtualization_enabled = @{ type = 'bool'; default = $false }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$description = $module.Params.description
$networkVirtualizationEnabled = $module.Params.network_virtualization_enabled

try {
    $vmmServer = Connect-SCVMM -Module $module

    $logicalNetwork = Get-SCLogicalNetwork -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($logicalNetwork) {
        @{
            name = $logicalNetwork.Name
            description = $logicalNetwork.Description
            network_virtualization_enabled = $logicalNetwork.IsNetworkVirtualizationEnabled
        }
    }
    else {
        @{}
    }

    if ($state -eq "present") {
        if (-not $logicalNetwork) {
            $params = @{
                VMMServer = $vmmServer
                Name = $name
                EnableNetworkVirtualization = $networkVirtualizationEnabled
            }

            if ($description) {
                $params.Description = $description
            }

            if (-not $module.CheckMode) {
                $logicalNetwork = New-SCLogicalNetwork @params -ErrorAction Stop
            }
            $module.Result.changed = $true
        }
        else {
            $changed = $false
            $params = @{
                LogicalNetwork = $logicalNetwork
            }

            if ($description -and $logicalNetwork.Description -ne $description) {
                $changed = $true
                $params.Description = $description
            }

            if ($logicalNetwork.IsNetworkVirtualizationEnabled -ne $networkVirtualizationEnabled) {
                $changed = $true
                $params.EnableNetworkVirtualization = $networkVirtualizationEnabled
            }

            if ($changed -and -not $module.CheckMode) {
                $logicalNetwork = Set-SCLogicalNetwork @params -ErrorAction Stop
            }

            $module.Result.changed = $changed
        }

        $module.Diff.after = @{
            name = $name
            description = $description
            network_virtualization_enabled = $networkVirtualizationEnabled
        }

        if ($logicalNetwork) {
            $props = @('Name', 'Description', 'IsNetworkVirtualizationEnabled', 'ID')
            $module.Result.logical_network = ConvertTo-SCVMMDict -InputObject $logicalNetwork -Properties $props
        }
    }
    else {
        if ($logicalNetwork) {
            if (-not $module.CheckMode) {
                Remove-SCLogicalNetwork -LogicalNetwork $logicalNetwork -ErrorAction Stop
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = @{}
    }

}

catch {
    $module.FailJson("Failed to manage logical network: $($_.Exception.Message)", $_)
}

$module.ExitJson()
