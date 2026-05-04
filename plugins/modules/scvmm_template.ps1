#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        cpu_count = @{ type = 'int' }
        description = @{ type = 'str' }
        library_server = @{ type = 'str' }
        memory_mb = @{ type = 'int' }
        name = @{ type = 'str'; required = $true }
        os_type = @{ type = 'str' }
        source_vm = @{ type = 'str' }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        vhd = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$tmplProps = @("Name", "Description", "CPUCount", "Memory", "OperatingSystem", "ID")

$vmmServer = Connect-SCVMM -Module $module

$tmpl = Get-SCVMTemplate -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue |
    Select-Object -First 1

$before = @{}
if ($tmpl) { $before = ConvertTo-SCVMMDict -InputObject $tmpl -Properties $tmplProps }

if ($state -eq "present") {
    if (-not $tmpl) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{ Name = $name; ErrorAction = "Stop" }

            if ($module.Params.source_vm) {
                $sourceVm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.source_vm -ErrorAction SilentlyContinue
                if (-not $sourceVm) { $module.FailJson("Source VM '$($module.Params.source_vm)' not found.") }
                $params.VM = $sourceVm

                if ($module.Params.library_server) {
                    $libServer = Get-SCLibraryServer -VMMServer $vmmServer -ComputerName $module.Params.library_server -ErrorAction SilentlyContinue
                    if (-not $libServer) { $module.FailJson("Library server '$($module.Params.library_server)' not found.") }
                    $params.LibraryServer = $libServer
                }
            }
            elseif ($module.Params.vhd) {
                $vhdObj = Get-SCVirtualHardDisk -VMMServer $vmmServer -Name $module.Params.vhd -ErrorAction SilentlyContinue
                if (-not $vhdObj) { $module.FailJson("VHD '$($module.Params.vhd)' not found.") }
                $hwProfile = New-SCHardwareProfile -VMMServer $vmmServer -Name "$name-hw" -ErrorAction Stop
                $params.HardwareProfile = $hwProfile
                $params.VirtualHardDisk = $vhdObj
            }
            else {
                $module.FailJson("Either source_vm or vhd is required when creating a template.")
            }

            if ($module.Params.cpu_count) { $params.CPUCount = $module.Params.cpu_count }
            if ($module.Params.memory_mb) { $params.MemoryMB = $module.Params.memory_mb }
            if ($module.Params.description) { $params.Description = $module.Params.description }
            if ($module.Params.os_type) {
                $os = Get-SCOperatingSystem -VMMServer $vmmServer | Where-Object { $_.Name -eq $module.Params.os_type } | Select-Object -First 1
                if ($os) { $params.OperatingSystem = $os }
            }

            try { $tmpl = New-SCVMTemplate @params }
            catch { $module.FailJson("Failed to create template '$name': $($_.Exception.Message)", $_) }
        }
    }
    else {
        $changed = $false
        $setParams = @{ VMTemplate = $tmpl; ErrorAction = "Stop" }
        if ($module.Params.description -and $tmpl.Description -ne $module.Params.description) {
            $setParams.Description = $module.Params.description; $changed = $true
        }
        if ($module.Params.cpu_count -and $tmpl.CPUCount -ne $module.Params.cpu_count) {
            $setParams.CPUCount = $module.Params.cpu_count; $changed = $true
        }
        if ($module.Params.memory_mb -and $tmpl.Memory -ne $module.Params.memory_mb) {
            $setParams.MemoryMB = $module.Params.memory_mb; $changed = $true
        }
        if ($changed) {
            $module.Result.changed = $true
            if (-not $module.CheckMode) {
                try { $tmpl = Set-SCVMTemplate @setParams }
                catch { $module.FailJson("Failed to update template '$name': $($_.Exception.Message)", $_) }
            }
        }
    }
    $after = @{}
    if ($tmpl) { $after = ConvertTo-SCVMMDict -InputObject $tmpl -Properties $tmplProps }
    $module.Result.template = $after
}
else {
    if ($tmpl) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try { Remove-SCVMTemplate -VMTemplate $tmpl -Force -ErrorAction Stop }
            catch { $module.FailJson("Failed to remove template '$name': $($_.Exception.Message)", $_) }
        }
    }
    $after = @{}
}

if ($module.DiffMode) { $module.Diff.before = $before; $module.Diff.after = $after }
$module.ExitJson()
