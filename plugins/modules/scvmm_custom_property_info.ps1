#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        member_type = @{ type = 'str'; choices = @('VM', 'VMHost', 'Cloud', 'VMTemplate', 'ServiceTemplate', 'ServiceInstance') }
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $properties = if ($module.Params.name) {
        Get-SCCustomProperty -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        Get-SCCustomProperty -VMMServer $vmmServer
    }

    $result = @()
    foreach ($property in $properties) {
        $result += ConvertTo-SCVMMDict -InputObject $property -Properties @('Name', 'Description', 'MemberType', 'ID')
    }

    $module.Result.custom_properties = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve custom properties: $($_.Exception.Message)", $_)
}
