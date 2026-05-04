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
    $templates = Get-SCServiceTemplate -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue
} else {
    $templates = Get-SCServiceTemplate -VMMServer $vmmServer
}

$module.Result.service_templates = @()
foreach ($template in $templates) {
    $module.Result.service_templates += ConvertTo-SCVMMDict -InputObject $template -Properties @('Name', 'Description', 'Release', 'Status', 'ID')
}

$module.ExitJson()
