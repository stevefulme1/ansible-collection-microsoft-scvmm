#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        cloud = @{ type = 'str' }
        name = @{ type = 'str' }
        vm_host = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$cloud = $module.Params.cloud
$vmHost = $module.Params.vm_host

$vmProps = @("Name", "Status", "CPUCount", "MemoryAssignedMB", "Description",
    "Cloud", "VMHost", "CreationTime", "ModifiedTime", "ID",
    "StartAction", "StopAction", "OperatingSystem")

$vmmServer = Connect-SCVMM -Module $module

if ($name) {
    $vms = @(Get-SCVirtualMachine -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue)
}
elseif ($cloud) {
    $cloudObj = Get-SCCloud -VMMServer $vmmServer -Name $cloud -ErrorAction SilentlyContinue
    if (-not $cloudObj) {
        $module.FailJson("Cloud '$cloud' not found.")
    }
    $vms = @(Get-SCVirtualMachine -Cloud $cloudObj -ErrorAction Stop)
}
elseif ($vmHost) {
    $hostObj = Get-SCVMHost -VMMServer $vmmServer -ComputerName $vmHost -ErrorAction SilentlyContinue
    if (-not $hostObj) {
        $module.FailJson("VM host '$vmHost' not found.")
    }
    $vms = @(Get-SCVirtualMachine -VMHost $hostObj -ErrorAction Stop)
}
else {
    $vms = @(Get-SCVirtualMachine -VMMServer $vmmServer -ErrorAction Stop)
}

$module.Result.vms = @($vms | ForEach-Object {
    ConvertTo-SCVMMDict -InputObject $_ -Properties $vmProps
})

$module.ExitJson()
