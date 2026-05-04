#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ required = $true; type = "str" }
        vm_subnet = @{ required = $true; type = "str" }
        state = @{ type = "str"; choices = @("present", "absent"); default = "present" }
        ip_range_start = @{ type = "str" }
        ip_range_end = @{ type = "str" }
        gateway = @{ type = "list"; elements = "str" }
        dns_servers = @{ type = "list"; elements = "str" }
        dns_suffix = @{ type = "str" }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$vmSubnetName = $module.Params.vm_subnet
$state = $module.Params.state
$ipRangeStart = $module.Params.ip_range_start
$ipRangeEnd = $module.Params.ip_range_end
$gateway = $module.Params.gateway
$dnsServers = $module.Params.dns_servers
$dnsSuffix = $module.Params.dns_suffix

try {
    $vmmServer = Connect-SCVMM -Module $module

    $vmSubnet = Get-SCVMSubnet -VMMServer $vmmServer -Name $vmSubnetName -ErrorAction Stop

    $ipPool = Get-SCStaticIPAddressPool -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue | Where-Object {
        $_.VMSubnet.ID -eq $vmSubnet.ID
    }

    $module.Diff.before = if ($ipPool) {
        @{
            name = $ipPool.Name
            vm_subnet = $ipPool.VMSubnet.Name
            ip_range_start = $ipPool.IPAddressRangeStart
            ip_range_end = $ipPool.IPAddressRangeEnd
            gateway = @($ipPool.DefaultGateways)
            dns_servers = @($ipPool.DNSServers)
            dns_suffix = $ipPool.DNSSuffix
        }
    } else {
        @{}
    }

    if ($state -eq "present") {
        if (-not $ipPool) {
            $params = @{
                VMMServer = $vmmServer
                Name = $name
                VMSubnet = $vmSubnet
            }

            if ($ipRangeStart) {
                $params.IPAddressRangeStart = $ipRangeStart
            }

            if ($ipRangeEnd) {
                $params.IPAddressRangeEnd = $ipRangeEnd
            }

            if ($gateway) {
                $params.DefaultGateway = $gateway
            }

            if ($dnsServers) {
                $params.DNSServer = $dnsServers
            }

            if ($dnsSuffix) {
                $params.DNSSuffix = $dnsSuffix
            }

            if (-not $module.CheckMode) {
                $ipPool = New-SCStaticIPAddressPool @params -ErrorAction Stop
            }
            $module.Result.changed = $true
        } else {
            $changed = $false
            $params = @{
                StaticIPAddressPool = $ipPool
            }

            if ($ipRangeStart -and $ipPool.IPAddressRangeStart -ne $ipRangeStart) {
                $changed = $true
                $params.IPAddressRangeStart = $ipRangeStart
            }

            if ($ipRangeEnd -and $ipPool.IPAddressRangeEnd -ne $ipRangeEnd) {
                $changed = $true
                $params.IPAddressRangeEnd = $ipRangeEnd
            }

            if ($gateway) {
                $changed = $true
                $params.DefaultGateway = $gateway
            }

            if ($dnsServers) {
                $changed = $true
                $params.DNSServer = $dnsServers
            }

            if ($dnsSuffix -and $ipPool.DNSSuffix -ne $dnsSuffix) {
                $changed = $true
                $params.DNSSuffix = $dnsSuffix
            }

            if ($changed -and -not $module.CheckMode) {
                $ipPool = Set-SCStaticIPAddressPool @params -ErrorAction Stop
            }

            $module.Result.changed = $changed
        }

        $module.Diff.after = @{
            name = $name
            vm_subnet = $vmSubnetName
            ip_range_start = $ipRangeStart
            ip_range_end = $ipRangeEnd
            gateway = $gateway
            dns_servers = $dnsServers
            dns_suffix = $dnsSuffix
        }

        if ($ipPool) {
            $module.Result.ip_pool = ConvertTo-SCVMMDict -InputObject $ipPool -Properties @(
                'Name', 'VMSubnet', 'IPAddressRangeStart', 'IPAddressRangeEnd', 'DefaultGateways', 'DNSServers', 'DNSSuffix', 'ID'
            )
        }
    } else {
        if ($ipPool) {
            if (-not $module.CheckMode) {
                Remove-SCStaticIPAddressPool -StaticIPAddressPool $ipPool -ErrorAction Stop
            }
            $module.Result.changed = $true
        }

        $module.Diff.after = @{}
    }

} catch {
    $module.FailJson("Failed to manage IP pool: $($_.Exception.Message)", $_)
}

$module.ExitJson()
