#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        hardware_profile = @{ type = 'str' }
        host_group = @{ type = 'str' }
        template = @{ type = 'str' }
        vm_name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$vmName = $module.Params.vm_name

try {
    $vmmServer = Connect-SCVMM -Module $module

    $vm = Get-SCVirtualMachine -VMMServer $vmmServer -Name $vmName -ErrorAction Stop

    $ratings = @(Get-SCVMHostRating -VMMServer $vmmServer -VM $vm -ErrorAction SilentlyContinue)

    $module.Result.ratings = @($ratings | ForEach-Object {
            @{
            vmhost = if ($_.VMHost) { $_.VMHost.Name } else { $null }
            rating = $_.Rating
            details = $_.RatingExplanation
            }
        })

}

catch {
    $module.FailJson("Failed to retrieve host ratings: $($_.Exception.Message)", $_)
}

$module.ExitJson()
