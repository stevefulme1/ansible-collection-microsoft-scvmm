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
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name

if ($name) {
    $classifications = Get-SCStorageClassification -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue
}
else {
    $classifications = Get-SCStorageClassification -VMMServer $vmmServer
}

$module.Result.storage_classifications = @()
foreach ($classification in $classifications) {
    $module.Result.storage_classifications += ConvertTo-SCVMMDict -InputObject $classification -Properties @('Name', 'Description', 'ID')
}

$module.ExitJson()
