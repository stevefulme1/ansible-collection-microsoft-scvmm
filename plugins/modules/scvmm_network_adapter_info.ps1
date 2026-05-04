#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        vm_id = @{ type = 'str' }
        vm_name = @{ type = 'str' }
    }
    supports_check_mode = $true
}
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$props = @("Name", "MACAddress", "MACAddressType", "VMNetwork", "IPv4Addresses", "ID")
$vmmServer = Connect-SCVMM -Module $module

if ($module.Params.vm_name) {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.vm_name -ErrorAction SilentlyContinue
    if (-not $vm) { $module.FailJson("VM '$($module.Params.vm_name)' not found.") }
    $adapters = @(Get-SCVirtualNetworkAdapter -VM $vm -ErrorAction Stop)
}
else {
    $adapters = @(Get-SCVirtualNetworkAdapter -VMMServer $vmmServer -ErrorAction Stop)
}

$module.Result.network_adapters = @($adapters | ForEach-Object { ConvertTo-SCVMMDict -InputObject $_ -Properties $props })
        $module.ExitJson()
