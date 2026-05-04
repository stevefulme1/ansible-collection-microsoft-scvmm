#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        vm_host = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$vmHostName = $module.Params.vm_host

try {
    $vmmServer = Connect-SCVMM -Module $module

    if ($vmHostName) {
        $vmHost = Get-SCVMHost -VMMServer $vmmServer -ComputerName $vmHostName -ErrorAction Stop
        $adapters = @(Get-SCVMHostNetworkAdapter -VMHost $vmHost -ErrorAction SilentlyContinue)
    }
    else {
        $adapters = @(Get-SCVMHostNetworkAdapter -VMMServer $vmmServer -ErrorAction SilentlyContinue)
    }

    $module.Result.network_adapters = @($adapters | ForEach-Object {
            ConvertTo-SCVMMDict -InputObject $_ -Properties @('Name', 'ConnectionName', 'VMHost', 'LogicalNetwork', 'MaxBandwidth', 'ID')
        })

}

catch {
    $module.FailJson("Failed to retrieve host network adapters: $($_.Exception.Message)", $_)
}

$module.ExitJson()
