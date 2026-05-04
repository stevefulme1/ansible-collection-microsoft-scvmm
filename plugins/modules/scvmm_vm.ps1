#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        cloud = @{ type = 'str' }
        cpu_count = @{ type = 'int' }
        description = @{ type = 'str' }
        host_group = @{ type = 'str' }
        memory_mb = @{ type = 'int' }
        name = @{ type = 'str'; required = $true }
        start_action = @{ type = 'str'; choices = @('NeverAutoTurnOnVM', 'AlwaysAutoTurnOnVM', 'TurnOnVMIfRunningWhenVSStopped') }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        stop_action = @{ type = 'str'; choices = @('SaveVM', 'TurnOffVM', 'ShutdownGuestOS') }
        template = @{ type = 'str' }
        vm_host = @{ type = 'str' }
        }
        state = @{
            type = "str"
            choices = @("present", "absent")
            default = "present"
        }
        template = @{
            type = "str"
        }
        cloud = @{
            type = "str"
        }
        host_group = @{
            type = "str"
        }
        vm_host = @{
            type = "str"
        }
        cpu_count = @{
            type = "int"
        }
        memory_mb = @{
            type = "int"
        }
        description = @{
            type = "str"
        }
        start_action = @{
            type = "str"
            choices = @("NeverAutoTurnOnVM", "AlwaysAutoTurnOnVM", "TurnOnVMIfRunningWhenVSStopped")
        }
        stop_action = @{
            type = "str"
            choices = @("SaveVM", "TurnOffVM", "ShutdownGuestOS")
        }
    }
    mutually_exclusive = @(
        , @("cloud", "vm_host")
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$template = $module.Params.template
$cloud = $module.Params.cloud
$hostGroup = $module.Params.host_group
$vmHost = $module.Params.vm_host
$cpuCount = $module.Params.cpu_count
$memoryMb = $module.Params.memory_mb
$description = $module.Params.description
$startAction = $module.Params.start_action
$stopAction = $module.Params.stop_action

$vmProps = @("Name", "Status", "CPUCount", "MemoryAssignedMB", "Description",
    "Cloud", "VMHost", "CreationTime", "ModifiedTime", "ID",
    "StartAction", "StopAction", "OperatingSystem")

$vmmServer = Connect-SCVMM -Module $module

$vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

$before = @{}
if ($vm) {
    $before = ConvertTo-SCVMMDict -InputObject $vm -Properties $vmProps
}

if ($state -eq "present") {
    if (-not $vm) {
        if (-not $template) {
            $module.FailJson("template is required when creating a new VM.")
        }

        $tmpl = Get-SCVMTemplate -VMMServer $vmmServer -Name $template -ErrorAction SilentlyContinue
        if (-not $tmpl) {
            $module.FailJson("Template '$template' not found.")
        }

        $vmConfig = New-SCVMConfiguration -VMTemplate $tmpl -Name $name -ErrorAction Stop

        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{
                Name = $name
                VMConfiguration = $vmConfig
                ErrorAction = "Stop"
            }

            if ($cloud) {
                $cloudObj = Get-SCCloud -VMMServer $vmmServer -Name $cloud -ErrorAction SilentlyContinue
                if (-not $cloudObj) {
                    $module.FailJson("Cloud '$cloud' not found.")
                }
                $params.Cloud = $cloudObj
            }
            elseif ($vmHost) {
                $hostObj = Get-SCVMHost -VMMServer $vmmServer -ComputerName $vmHost -ErrorAction SilentlyContinue
                if (-not $hostObj) {
                    $module.FailJson("VM host '$vmHost' not found.")
                }
                $params.VMHost = $hostObj
            }
            elseif ($hostGroup) {
                $hg = Get-SCVMHostGroup -VMMServer $vmmServer -Name $hostGroup -ErrorAction SilentlyContinue
                if (-not $hg) {
                    $module.FailJson("Host group '$hostGroup' not found.")
                }
                $params.HostGroup = $hg
            }

            if ($cpuCount) { $params.CPUCount = $cpuCount }
            if ($memoryMb) { $params.MemoryMB = $memoryMb }
            if ($description) { $params.Description = $description }
            if ($startAction) { $params.StartAction = $startAction }
            if ($stopAction) { $params.StopAction = $stopAction }

            try {
                $vm = New-SCVirtualMachine @params
            }
            catch {
                $module.FailJson("Failed to create VM '$name': $($_.Exception.Message)", $_)
            }
        }
    }
    else {
        $changed = $false
        $setParams = @{
            VM = $vm
            ErrorAction = "Stop"
        }

        if ($cpuCount -and $vm.CPUCount -ne $cpuCount) {
            $setParams.CPUCount = $cpuCount
            $changed = $true
        }
        if ($memoryMb -and $vm.MemoryAssignedMB -ne $memoryMb) {
            $setParams.MemoryMB = $memoryMb
            $changed = $true
        }
        if ($description -and $vm.Description -ne $description) {
            $setParams.Description = $description
            $changed = $true
        }
        if ($startAction -and $vm.StartAction.ToString() -ne $startAction) {
            $setParams.StartAction = $startAction
            $changed = $true
        }
        if ($stopAction -and $vm.StopAction.ToString() -ne $stopAction) {
            $setParams.StopAction = $stopAction
            $changed = $true
        }

        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                try {
                    $vm = Set-SCVirtualMachine @setParams
                }
                catch {
                    $module.FailJson("Failed to update VM '$name': $($_.Exception.Message)", $_)
                }
            }
        }
    }

    $after = @{}
    if ($vm) {
        $after = ConvertTo-SCVMMDict -InputObject $vm -Properties $vmProps
    }
    $module.Result.vm = $after
}
else {
    if ($vm) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try {
                Remove-SCVirtualMachine -VM $vm -Force -ErrorAction Stop
            }
            catch {
                $module.FailJson("Failed to remove VM '$name': $($_.Exception.Message)", $_)
            }
        }
    }
    $after = @{}
}

if ($module.DiffMode) {
    $module.Diff.before = $before
    $module.Diff.after = $after
}

$module.ExitJson()
