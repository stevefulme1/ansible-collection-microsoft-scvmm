#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        host = @{ type = 'str' }
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name

if ($name) {
    $pools = Get-SCStoragePool -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue
}
else {
    $pools = Get-SCStoragePool -VMMServer $vmmServer
}

$module.Result.storage_pools = @()
foreach ($pool in $pools) {
    $module.Result.storage_pools += ConvertTo-SCVMMDict -InputObject $pool -Properties @('Name', 'TotalManagedSpace', 'RemainingManagedSpace', 'State', 'ID')
}

$module.ExitJson()
