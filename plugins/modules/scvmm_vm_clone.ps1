#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        cloud = @{ type = 'str' }
        description = @{ type = 'str' }
        host_group = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        source_vm = @{ type = 'str'; required = $true }
        vm_host = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $existingClone = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue

    if ($existingClone) {
        $module.Result.changed = $false
        $module.Result.vm = ConvertTo-SCVMMDict -InputObject $existingClone -Properties @('Name', 'Status', 'VMHost', 'ID')
        $module.ExitJson()
    }

    if ($module.CheckMode) {
        $module.Result.changed = $true
        $module.Result.vm = @{
            Name = $module.Params.name
            VMHost = $module.Params.vm_host
            Status = if ($module.Params.start_vm) { 'would_be_running' } else { 'would_be_stopped' }
        }
        $module.ExitJson()
    }

    $sourceVM = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.source_vm -ErrorAction Stop
    $targetHost = Get-SCVMHost -VMMServer $vmmServer -ComputerName $module.Params.vm_host -ErrorAction Stop

    $cloneParams = @{
        VM = $sourceVM
        Name = $module.Params.name
        VMHost = $targetHost
        ErrorAction = 'Stop'
    }

    if ($module.Params.path) {
        $cloneParams.Path = $module.Params.path
    }

    $clonedVM = New-SCVirtualMachine @cloneParams

    if ($module.Params.start_vm) {
        Start-SCVirtualMachine -VM $clonedVM -ErrorAction Stop | Out-Null
        $clonedVM = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.name -ErrorAction Stop
    }

    $module.Result.changed = $true
    $module.Result.vm = ConvertTo-SCVMMDict -InputObject $clonedVM -Properties @('Name', 'Status', 'VMHost', 'ID')

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to clone VM: $($_.Exception.Message)", $_)
}
