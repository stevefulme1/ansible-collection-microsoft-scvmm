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
$props = @("Name", "Description", "ID")
$vmmServer = Connect-SCVMM -Module $module

if ($module.Params.name) {
    $items = @(Get-SCPortClassification -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue)
}
else {
    $items = @(Get-SCPortClassification -VMMServer $vmmServer -ErrorAction Stop)
}

$module.Result.port_classifications = @($items | ForEach-Object { ConvertTo-SCVMMDict -InputObject $_ -Properties $props })
        $module.ExitJson()
