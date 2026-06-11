#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        vm_name = @{ type = 'str'; required = $true }
        vhd_name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$vmName = $module.Params.vm_name
$vhdName = $module.Params.vhd_name
$diskProps = @("Name", "BusType", "Bus", "LUN", "MaximumIOPS", "Size", "Location", "ID")

$vmmServer = Connect-SCVMM -Module $module

$vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $vmName -ErrorAction SilentlyContinue
if (-not $vm) {
    $module.FailJson("VM '$vmName' not found.")
}

$disks = @(Get-SCVirtualDiskDrive -VM $vm -ErrorAction Stop)

if ($vhdName) {
    $disks = @($disks | Where-Object { $_.VirtualHardDisk.Name -eq $vhdName })
}

$module.Result.disks = @($disks | ForEach-Object {
        $disk = $_
        $vhd = $disk.VirtualHardDisk
        @{
            vm_name = $vmName
            vhd_name = if ($vhd) { $vhd.Name } else { $null }
            bus_type = $disk.BusType
            bus = $disk.Bus
            lun = $disk.LUN
            size_gb = if ($vhd) { [math]::Round($vhd.Size / 1GB, 2) } else { 0 }
            path = if ($vhd) { $vhd.Location } else { $null }
            id = $disk.ID
        }
    })

$module.ExitJson()
