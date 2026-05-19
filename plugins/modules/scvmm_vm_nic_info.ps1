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
    if (-not $vm) { $module.FailJson("VM '$($module.Params.vm_name)' not found.") }

    $adapters = @(Get-SCVirtualNetworkAdapter -VM $vm -ErrorAction Stop)

    if ($module.Params.name) {
        $adapters = @($adapters | Where-Object { $_.Name -eq $module.Params.name })
    }

    $props = @("Name", "MACAddress", "MACAddressType", "VMNetwork", "IPv4Addresses", "ID")
    $module.Result.nics = @($adapters | ForEach-Object { ConvertTo-SCVMMDict -InputObject $_ -Properties $props })

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve VM NICs: $($_.Exception.Message)", $_)
}
