#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str' }
        path = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name

try {
    $vmmServer = Connect-SCVMM -Module $module

    if ($name) {
        $hostGroups = @(Get-SCVMHostGroup -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue)
    }
    else {
        $hostGroups = @(Get-SCVMHostGroup -VMMServer $vmmServer -ErrorAction SilentlyContinue)
    }

    $module.Result.host_groups = @($hostGroups | ForEach-Object {
        ConvertTo-SCVMMDict -InputObject $_ -Properties @(
            'Name', 'Description', 'Path', 'ParentHostGroup', 'CreationTime', 'ID'
        )
    })

}

catch {
    $module.FailJson("Failed to retrieve host groups: $($_.Exception.Message)", $_)
}

$module.ExitJson()
