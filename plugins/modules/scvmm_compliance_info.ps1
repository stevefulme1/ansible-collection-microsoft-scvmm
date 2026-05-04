#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        host_cluster = @{ type = 'str' }
        vm_host = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $complianceParams = @{
        VMMServer = $vmmServer
    }

    if ($module.Params.vm_host) {
        $vmHostName = Get-SCVMHost -VMMServer $vmmServer -ComputerName $module.Params.vm_host -ErrorAction Stop
        $complianceParams.VMHost = $vmHostName
    }

    if ($module.Params.host_cluster) {
        $cluster = Get-SCVMHostCluster -VMMServer $vmmServer -Name $module.Params.host_cluster -ErrorAction Stop
        $complianceParams.VMHostCluster = $cluster
    }

    $status = Get-SCComplianceStatus @complianceParams

    $result = @()
    foreach ($item in $status) {
        $result += ConvertTo-SCVMMDict -InputObject $item -Properties @('VMHost', 'Baseline', 'Status', 'LastScanTime', 'ID')
    }

    $module.Result.compliance_status = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve compliance status: $($_.Exception.Message)", $_)
}
