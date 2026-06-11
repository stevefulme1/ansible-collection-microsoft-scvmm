#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        vm_name = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$vmName = $module.Params.vm_name

$vmmServer = Connect-SCVMM -Module $module

$vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $vmName -ErrorAction SilentlyContinue
if (-not $vm) {
    $module.FailJson("VM '$vmName' not found.")
}

$dvdDrives = @(Get-SCVirtualDVDDrive -VM $vm -ErrorAction Stop)

$module.Result.dvd_drives = @($dvdDrives | ForEach-Object {
        $drive = $_
        $iso = $drive.ISO
        @{
            vm_name = $vmName
            bus = $drive.Bus
            lun = $drive.LUN
            iso = if ($iso) { $iso.SharePath } else { $null }
            iso_name = if ($iso) { $iso.Name } else { $null }
            id = $drive.ID
        }
    })

$module.ExitJson()
