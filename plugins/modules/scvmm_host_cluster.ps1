#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        cluster_reserve = @{ type = 'int' }
        credential = @{ type = 'str' }
        host_group = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$credential = $module.Params.credential
$hostGroup = $module.Params.host_group
$description = $module.Params.description

try {
    $vmmServer = Connect-SCVMM -Module $module

    $cluster = Get-SCVMHostCluster -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($cluster) {
        @{
            name = $cluster.Name
            description = $cluster.Description
            host_group = $cluster.HostGroup.Path
        }
    }
    else {
        @{}
    }

    if ($state -eq "present") {
        if (-not $cluster) {
            $params = @{
                VMMServer = $vmmServer
                ComputerName = $name
            }

            if ($credential) {
                $runAsAccount = Get-SCRunAsAccount -VMMServer $vmmServer -Name $credential -ErrorAction Stop
                $params.Credential = $runAsAccount
            }

            if ($hostGroup) {
                $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hostGroup -ErrorAction Stop
                $params.VMHostGroup = $vmHostGroup
            }

            if ($description) {
                $params.Description = $description
            }

            if (-not $module.CheckMode) {
                $cluster = Add-SCVMHostCluster @params -ErrorAction Stop
            }
            $module.Result.changed = $true
        }
        else {
            $changed = $false

            $params = @{
                VMHostCluster = $cluster
            }

            if ($description -and $cluster.Description -ne $description) {
                $changed = $true
                $params.Description = $description
            }

            if ($hostGroup) {
                $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hostGroup -ErrorAction Stop
                if ($cluster.HostGroup.ID -ne $vmHostGroup.ID) {
                    $changed = $true
                    $params.VMHostGroup = $vmHostGroup
                }
            }

            if ($changed -and -not $module.CheckMode) {
                $cluster = Set-SCVMHostCluster @params -ErrorAction Stop
            }

            $module.Result.changed = $changed
        }

        $module.Diff.after = @{
            name = $name
            description = $description
            host_group = $hostGroup
        }

        if ($cluster) {
            $module.Result.host_cluster = ConvertTo-SCVMMDict -InputObject $cluster -Properties @(
                'Name', 'Description', 'HostGroup', 'ClusterNodeCount', 'AvailableStorageNodes', 'ID'
            )
        }
    }
    else {
        if ($cluster) {
            if (-not $module.CheckMode) {
                Remove-SCVMHostCluster -VMHostCluster $cluster -ErrorAction Stop
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = @{}
    }

}

catch {
    $module.FailJson("Failed to manage host cluster: $($_.Exception.Message)", $_)
}

$module.ExitJson()
