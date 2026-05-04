#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec

$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$cloudProps = @("Name", "Description", "HostGroup", "CreationTime", "ModifiedTime", "ID")

$vmmServer = Connect-SCVMM -Module $module

if ($name) {
    $clouds = @(Get-SCCloud -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue)
}
else {
    $clouds = @(Get-SCCloud -VMMServer $vmmServer -ErrorAction Stop)
}

$module.Result.clouds = @($clouds | ForEach-Object {
    ConvertTo-SCVMMDict -InputObject $_ -Properties $cloudProps
})

$module.ExitJson()
