#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = "str" }
        host_group = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$hostGroup = $module.Params.host_group

try {
    $vmmServer = Connect-SCVMM -Module $module

    $params = @{
        VMMServer = $vmmServer
        ErrorAction = "SilentlyContinue"
    }

    if ($name) {
        $params.ComputerName = $name
    }

    if ($hostGroup) {
        $vmHostGroup = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hostGroup -ErrorAction Stop
        $params.VMHostGroup = $vmHostGroup
    }

    $hosts = @(Get-SCVMHost @params)

    $module.Result.hosts = @($hosts | ForEach-Object {
        ConvertTo-SCVMMDict -InputObject $_ -Properties @(
            'Name', 'ComputerName', 'OperatingSystem', 'VMHostGroup', 'OverallState', 'CommunicationState', 'ID'
        )
    })

} catch {
    $module.FailJson("Failed to retrieve VM hosts: $($_.Exception.Message)", $_)
}

$module.ExitJson()
