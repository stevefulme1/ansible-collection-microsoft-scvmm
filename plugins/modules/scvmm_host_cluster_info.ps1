#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name

try {
    $vmmServer = Connect-SCVMM -Module $module

    if ($name) {
        $clusters = @(Get-SCVMHostCluster -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue)
    }
    else {
        $clusters = @(Get-SCVMHostCluster -VMMServer $vmmServer -ErrorAction SilentlyContinue)
    }

    $module.Result.host_clusters = @($clusters | ForEach-Object {
            ConvertTo-SCVMMDict -InputObject $_ -Properties @('Name', 'Description', 'HostGroup', 'ClusterNodeCount', 'AvailableStorageNodes', 'ID')
        })

}

catch {
    $module.FailJson("Failed to retrieve host clusters: $($_.Exception.Message)", $_)
}

$module.ExitJson()
