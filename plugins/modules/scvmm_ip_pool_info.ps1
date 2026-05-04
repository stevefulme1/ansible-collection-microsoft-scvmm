#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        logical_network_definition = @{ type = 'str' }
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$props = @("Name", "VMSubnet", "IPAddressRangeStart", "IPAddressRangeEnd",
    "DefaultGateways", "DNSServers", "DNSSuffix", "ID")

$vmmServer = Connect-SCVMM -Module $module

if ($name) {
    $pools = @(Get-SCStaticIPAddressPool -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue)
}
else {
    $pools = @(Get-SCStaticIPAddressPool -VMMServer $vmmServer -ErrorAction Stop)
}

$module.Result.ip_pools = @($pools | ForEach-Object {
    ConvertTo-SCVMMDict -InputObject $_ -Properties $props
})

$module.ExitJson()
