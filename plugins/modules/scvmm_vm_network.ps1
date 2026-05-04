#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ required = $true; type = "str" }
        logical_network = @{ required = $true; type = "str" }
        state = @{ type = "str"; choices = @("present", "absent"); default = "present" }
        description = @{ type = "str" }
        isolation_type = @{ type = "str"; choices = @("NoIsolation", "VLANNetwork", "WindowsNetworkVirtualization") }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$logicalNetworkName = $module.Params.logical_network
$state = $module.Params.state
$description = $module.Params.description
$isolationType = $module.Params.isolation_type

try {
    $vmmServer = Connect-SCVMM -Module $module

    $logicalNetwork = Get-SCLogicalNetwork -VMMServer $vmmServer -Name $logicalNetworkName -ErrorAction Stop

    $vmNetwork = Get-SCVMNetwork -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue | Where-Object {
        $_.LogicalNetwork.ID -eq $logicalNetwork.ID
    }

    $module.Diff.before = if ($vmNetwork) {
        @{
            name = $vmNetwork.Name
            logical_network = $vmNetwork.LogicalNetwork.Name
            description = $vmNetwork.Description
            isolation_type = $vmNetwork.IsolationType
        }
    }
    else {
        @{}
    }

    if ($state -eq "present") {
        if (-not $vmNetwork) {
            $params = @{
                VMMServer = $vmmServer
                Name = $name
                LogicalNetwork = $logicalNetwork
            }

            if ($description) {
                $params.Description = $description
            }

            if ($isolationType) {
                $params.IsolationType = $isolationType
            }

            if (-not $module.CheckMode) {
                $vmNetwork = New-SCVMNetwork @params -ErrorAction Stop
            }
            $module.Result.changed = $true
        }
        else {
            $changed = $false
            $params = @{
                VMNetwork = $vmNetwork
            }

            if ($description -and $vmNetwork.Description -ne $description) {
                $changed = $true
                $params.Description = $description
            }

            if ($changed -and -not $module.CheckMode) {
                $vmNetwork = Set-SCVMNetwork @params -ErrorAction Stop
            }

            $module.Result.changed = $changed
        }

        $module.Diff.after = @{
            name = $name
            logical_network = $logicalNetworkName
            description = $description
            isolation_type = $isolationType
        }

        if ($vmNetwork) {
            $module.Result.vm_network = ConvertTo-SCVMMDict -InputObject $vmNetwork -Properties @(
                'Name', 'Description', 'LogicalNetwork', 'IsolationType', 'VMSubnet', 'ID'
            )
        }
    }
    else {
        if ($vmNetwork) {
            if (-not $module.CheckMode) {
                Remove-SCVMNetwork -VMNetwork $vmNetwork -ErrorAction Stop
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = @{}
    }

}

catch {
    $module.FailJson("Failed to manage VM network: $($_.Exception.Message)", $_)
}

$module.ExitJson()
