#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        computer_name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$computerName = $module.Params.computer_name

if ($computerName) {
    $servers = Get-SCLibraryServer -VMMServer $vmmServer -ComputerName $computerName -ErrorAction SilentlyContinue
} else {
    $servers = Get-SCLibraryServer -VMMServer $vmmServer
}

$module.Result.library_servers = @()
foreach ($server in $servers) {
    $module.Result.library_servers += ConvertTo-SCVMMDict -InputObject $server -Properties @('Name', 'ComputerName', 'Description', 'ID')
}

$module.ExitJson()
