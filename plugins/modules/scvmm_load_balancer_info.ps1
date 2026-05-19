#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        manufacturer = @{ type = 'str' }
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$manufacturer = $module.Params.manufacturer

try {
    $vmmServer = Connect-SCVMM -Module $module

    $params = @{
        VMMServer = $vmmServer
        ErrorAction = "SilentlyContinue"
    }

    $loadBalancers = @(Get-SCLoadBalancer @params)

    if ($name) {
        $loadBalancers = @($loadBalancers | Where-Object { $_.Name -eq $name })
    }

    if ($manufacturer) {
        $loadBalancers = @($loadBalancers | Where-Object { $_.Manufacturer -eq $manufacturer })
    }

    $module.Result.load_balancers = @($loadBalancers | ForEach-Object {
            ConvertTo-SCVMMDict -InputObject $_ -Properties @('Name', 'Address', 'Port', 'Manufacturer', 'Model', 'State', 'ID')
        })

}

catch {
    $module.FailJson("Failed to retrieve load balancers: $($_.Exception.Message)", $_)
}

$module.ExitJson()
