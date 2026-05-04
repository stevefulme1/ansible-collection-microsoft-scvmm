#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        vm_name = @{ type = 'str'; required = $true }
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.vm_name -ErrorAction Stop

    $checkpoints = if ($module.Params.name) {
        Get-SCVMCheckpoint -VM $vm -Name $module.Params.name -ErrorAction SilentlyContinue
    }
    else {
        Get-SCVMCheckpoint -VM $vm
    }

    $result = @()
    foreach ($checkpoint in $checkpoints) {
        $result += ConvertTo-SCVMMDict -InputObject $checkpoint -Properties @(
            'Name', 'Description', 'VM', 'CreationTime', 'ID'
        )
    }

    $module.Result.checkpoints = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve VM checkpoints: $($_.Exception.Message)", $_)
}
