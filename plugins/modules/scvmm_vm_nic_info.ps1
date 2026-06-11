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

$vmName = $module.Params.vm_name
$nicName = $module.Params.name

$vmmServer = Connect-SCVMM -Module $module

$vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $vmName -ErrorAction SilentlyContinue
if (-not $vm) {
    $module.FailJson("VM '$vmName' not found.")
}

$nics = @(Get-SCVirtualNetworkAdapter -VM $vm -ErrorAction Stop)

if ($nicName) {
    $nics = @($nics | Where-Object { $_.Name -eq $nicName })
}

$module.Result.nics = @($nics | ForEach-Object {
        $nic = $_
        @{
            name = $nic.Name
            vm_network = if ($nic.VMNetwork) { $nic.VMNetwork.Name } else { $null }
            mac_address = $nic.MACAddress
            mac_type = $nic.MACAddressType
            enabled = $nic.Enabled
            connected = $nic.Connected
            id = $nic.ID
        }
    })

$module.ExitJson()
