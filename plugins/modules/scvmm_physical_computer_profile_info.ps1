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

try {
    $profiles = if ($module.Params.name) {
        Get-SCPhysicalComputerProfile -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        Get-SCPhysicalComputerProfile -VMMServer $vmmServer
    }

    $result = @()
    foreach ($profile in $profiles) {
        $result += ConvertTo-SCVMMDict -InputObject $profile -Properties @('Name', 'Description', 'OperatingSystem', 'ID')
    }

    $module.Result.profiles = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve physical computer profiles: $($_.Exception.Message)", $_)
}
