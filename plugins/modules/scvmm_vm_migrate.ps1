#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str'; required = $true }
        vm_host = @{ type = 'str'; required = $true }
        path = @{ type = 'str' }
        use_live_migration = @{ type = 'bool'; default = $false }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.name -ErrorAction Stop
    $targetHost = Get-SCVMHost -VMMServer $vmmServer -ComputerName $module.Params.vm_host -ErrorAction Stop

    $currentHost = $vm.VMHost.Name

    if ($currentHost -eq $targetHost.Name) {
        $module.Result.changed = $false
        $module.Result.vm = ConvertTo-SCVMMDict -InputObject $vm -Properties @(
            'Name', 'VMHost', 'Status', 'ID'
        )
        $module.ExitJson()
    }

    if ($module.CheckMode) {
        $module.Result.changed = $true
        $module.Result.vm = @{
            Name = $module.Params.name
            VMHost = $module.Params.vm_host
            Status = 'would_migrate'
        }
        $module.ExitJson()
    }

    $moveParams = @{
        VM = $vm
        VMHost = $targetHost
        ErrorAction = 'Stop'
    }

    if ($module.Params.path) {
        $moveParams.Path = $module.Params.path
    }

    if ($module.Params.use_live_migration) {
        $moveParams.UseLAN = $true
    }

    Move-SCVirtualMachine @moveParams | Out-Null

    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.name -ErrorAction Stop

    $module.Result.changed = $true
    $module.Result.vm = ConvertTo-SCVMMDict -InputObject $vm -Properties @(
        'Name', 'VMHost', 'Status', 'ID'
    )

    $module.ExitJson()
} catch {
    $module.FailJson("Failed to migrate VM: $($_.Exception.Message)", $_)
}
