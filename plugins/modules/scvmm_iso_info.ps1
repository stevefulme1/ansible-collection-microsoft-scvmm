#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        library_server = @{ type = 'str' }
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name

if ($name) {
    $isos = Get-SCISO -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue
}
else {
    $isos = Get-SCISO -VMMServer $vmmServer
}

$module.Result.isos = @()
foreach ($iso in $isos) {
    $module.Result.isos += ConvertTo-SCVMMDict -InputObject $iso -Properties @('Name', 'Description', 'SharePath', 'ID')
}

$module.ExitJson()
