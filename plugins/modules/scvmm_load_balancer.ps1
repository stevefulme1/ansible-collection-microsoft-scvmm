#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        address = @{ type = 'str' }
        credential = @{ type = 'str' }
        manufacturer = @{ type = 'str' }
        model = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        port = @{ type = 'int' }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$state = $module.Params.state
$lbProps = @("Name", "Address", "Manufacturer", "Model", "State", "ID")

$vmmServer = Connect-SCVMM -Module $module

$lb = Get-SCLoadBalancer -VMMServer $vmmServer -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -eq $name } | Select-Object -First 1

$before = @{}
if ($lb) {
    $before = ConvertTo-SCVMMDict -InputObject $lb -Properties $lbProps
}

if ($state -eq "present") {
    if (-not $lb) {
        if (-not $module.Params.address) {
            $module.FailJson("address is required when adding a load balancer.")
        }
        if (-not $module.Params.credential) {
            $module.FailJson("credential is required when adding a load balancer.")
        }

        $runAs = Get-SCRunAsAccount -VMMServer $vmmServer -Name $module.Params.credential -ErrorAction SilentlyContinue
        if (-not $runAs) {
            $module.FailJson("RunAs account '$($module.Params.credential)' not found.")
        }

        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            $params = @{
                VMMServer = $vmmServer
                Address = $module.Params.address
                RunAsAccount = $runAs
                ErrorAction = "Stop"
            }
            if ($module.Params.manufacturer) { $params.Manufacturer = $module.Params.manufacturer }
            if ($module.Params.model) { $params.Model = $module.Params.model }
            if ($module.Params.configuration_provider) {
                $provider = Get-SCConfigurationProvider -VMMServer $vmmServer |
                    Where-Object { $_.Name -eq $module.Params.configuration_provider }
                if ($provider) { $params.ConfigurationProvider = $provider }
            }
            try {
                $lb = Add-SCLoadBalancer @params
            }
            catch {
                $module.FailJson("Failed to add load balancer: $($_.Exception.Message)", $_)
            }
        }
    }

    $after = @{}
    if ($lb) {
        $after = ConvertTo-SCVMMDict -InputObject $lb -Properties $lbProps
    }
    $module.Result.load_balancer = $after
}
else {
    if ($lb) {
        $module.Result.changed = $true
        if (-not $module.CheckMode) {
            try {
                Remove-SCLoadBalancer -LoadBalancer $lb -ErrorAction Stop
            }
            catch {
                $module.FailJson("Failed to remove load balancer: $($_.Exception.Message)", $_)
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
