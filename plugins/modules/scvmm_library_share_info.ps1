#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        path = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$path = $module.Params.path

if ($path) {
    $shares = Get-SCLibraryShare -VMMServer $vmmServer | Where-Object { $_.Path -eq $path }
} else {
    $shares = Get-SCLibraryShare -VMMServer $vmmServer
}

$module.Result.library_shares = @()
foreach ($share in $shares) {
    $module.Result.library_shares += ConvertTo-SCVMMDict -InputObject $share -Properties @('Name', 'Description', 'Path', 'ID')
}

$module.ExitJson()
