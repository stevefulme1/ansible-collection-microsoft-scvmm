#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        mac_address = @{ type = 'str' }
        mac_type = @{ type = 'str'; default = 'Dynamic'; choices = @('Dynamic', 'Static') }
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        vm_name = @{ type = 'str'; required = $true }
        vm_network = @{ type = 'str' }
    }
)
    )
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $module.Params.vm_name -ErrorAction Stop

    $existing = Get-SCVirtualNetworkAdapter -VM $vm | Where-Object { $_.Name -eq $module.Params.name }

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'VMNetwork', 'MACAddress', 'MACAddressType', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCVirtualNetworkAdapter -VirtualNetworkAdapter $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    else {
        $needsChange = $false

        if (-not $existing) {
            if (-not $module.CheckMode) {
                $vmNetwork = Get-SCVMNetwork -VMMServer $vmmServer -Name $module.Params.vm_network -ErrorAction Stop

                $newParams = @{
                    VM = $vm
                    Name = $module.Params.name
                    VMNetwork = $vmNetwork
                    ErrorAction = 'Stop'
                }

                if ($module.Params.mac_address_type) {
                    $newParams.MACAddressType = $module.Params.mac_address_type
                }

                if ($module.Params.mac_address) {
                    $newParams.MACAddress = $module.Params.mac_address
                }

                $existing = New-SCVirtualNetworkAdapter @newParams
            }
            $needsChange = $true
        }
        else {
            $setParams = @{}
            if ($module.Params.vm_network -and $existing.VMNetwork.Name -ne $module.Params.vm_network) {
                $vmNetwork = Get-SCVMNetwork -VMMServer $vmmServer -Name $module.Params.vm_network -ErrorAction Stop
                $setParams.VMNetwork = $vmNetwork
                $needsChange = $true
            }
            if ($module.Params.mac_address -and $existing.MACAddress -ne $module.Params.mac_address) {
                $setParams.MACAddress = $module.Params.mac_address
                $needsChange = $true
            }
            if ($module.Params.mac_address_type -and $existing.MACAddressType -ne $module.Params.mac_address_type) {
                $setParams.MACAddressType = $module.Params.mac_address_type
                $needsChange = $true
            }

            if ($setParams.Count -gt 0 -and -not $module.CheckMode) {
                Set-SCVirtualNetworkAdapter -VirtualNetworkAdapter $existing @setParams -ErrorAction Stop
                $existing = Get-SCVirtualNetworkAdapter -VM $vm | Where-Object { $_.Name -eq $module.Params.name }
            }
        }

        $module.Result.changed = $needsChange
        $module.Result.nic = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @(
                'Name', 'VMNetwork', 'MACAddress', 'MACAddressType', 'ID'
            )
        }
        else {
            @{
                Name = $module.Params.name
                VMNetwork = $module.Params.vm_network
                MACAddress = $module.Params.mac_address
                MACAddressType = $module.Params.mac_address_type
            }
        }
        $module.Diff.after = $module.Result.nic
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage VM network adapter: $($_.Exception.Message)", $_)
}
