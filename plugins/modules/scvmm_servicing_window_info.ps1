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
    $windows = if ($module.Params.name) {
        Get-SCServicingWindow -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        Get-SCServicingWindow -VMMServer $vmmServer
    }

    $result = @()
    foreach ($window in $windows) {
        $result += ConvertTo-SCVMMDict -InputObject $window -Properties @(
            'Name', 'Description', 'StartDate', 'EndDate', 'TimeZone', 'Category', 'ID'
        )
    }

    $module.Result.servicing_windows = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve servicing windows: $($_.Exception.Message)", $_)
}
