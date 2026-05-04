#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        baseline = @{ type = 'str' }
        host_cluster = @{ type = 'str' }
        vm_host = @{ type = 'str' }
    }
    required_one_of = @(
        @('vm_host', 'host_cluster')
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    if ($module.CheckMode) {
        $module.Result.changed = $true
        $module.Result.scan = @{ status = 'would_start_scan' }
        $module.ExitJson()
    }

    $scanParams = @{
        VMMServer = $vmmServer
        ErrorAction = 'Stop'
    }

    if ($module.Params.vm_host) {
        $vmHostName = Get-SCVMHost -VMMServer $vmmServer -ComputerName $module.Params.vm_host -ErrorAction Stop
        $scanParams.VMHost = $vmHostName
    }

    if ($module.Params.host_cluster) {
        $cluster = Get-SCVMHostCluster -VMMServer $vmmServer -Name $module.Params.host_cluster -ErrorAction Stop
        $scanParams.VMHostCluster = $cluster
    }

    if ($module.Params.baseline) {
        $baselineObj = Get-SCBaseline -VMMServer $vmmServer -Name $module.Params.baseline -ErrorAction Stop
        $scanParams.Baseline = $baselineObj
    }

    $job = Start-SCComplianceScan @scanParams

    $module.Result.changed = $true
    $module.Result.scan = ConvertTo-SCVMMDict -InputObject $job -Properties @(
        'Name', 'ID', 'Status', 'Progress', 'StartTime'
    )

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to start compliance scan: $($_.Exception.Message)", $_)
}
