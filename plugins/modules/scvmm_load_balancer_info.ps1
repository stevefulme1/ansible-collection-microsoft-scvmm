#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$lbProps = @("Name", "Address", "Port", "Manufacturer", "Model", "ConfigurationProvider", "ID")

$vmmServer = Connect-SCVMM -Module $module

if ($name) {
    $loadBalancers = @(Get-SCLoadBalancer -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue)
}
else {
    $loadBalancers = @(Get-SCLoadBalancer -VMMServer $vmmServer -ErrorAction Stop)
}

$module.Result.load_balancers = @($loadBalancers | ForEach-Object {
        ConvertTo-SCVMMDict -InputObject $_ -Properties $lbProps
    })

$module.ExitJson()
