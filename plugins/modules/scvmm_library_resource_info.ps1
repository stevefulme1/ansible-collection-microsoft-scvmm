#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        library_share = @{ type = 'str' }
        name = @{ type = 'str' }
        resource_type = @{ type = 'str'; default = 'All'; choices = @('ISO', 'VHD', 'VHDX', 'Script', 'CustomResource', 'All') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$name = $module.Params.name
$libraryShare = $module.Params.library_share
$resourceType = $module.Params.resource_type

try {
    $vmmServer = Connect-SCVMM -Module $module

    $resources = @()

    # Gather resources by type
    if ($resourceType -eq 'All' -or $resourceType -eq 'ISO') {
        $isos = @(Get-SCISO -VMMServer $vmmServer -ErrorAction SilentlyContinue)
        $resources += $isos
    }
    if ($resourceType -eq 'All' -or $resourceType -eq 'VHD' -or $resourceType -eq 'VHDX') {
        $vhds = @(Get-SCVirtualHardDisk -VMMServer $vmmServer -ErrorAction SilentlyContinue)
        $resources += $vhds
    }
    if ($resourceType -eq 'All' -or $resourceType -eq 'Script') {
        $scripts = @(Get-SCScript -VMMServer $vmmServer -ErrorAction SilentlyContinue)
        $resources += $scripts
    }
    if ($resourceType -eq 'All' -or $resourceType -eq 'CustomResource') {
        $customs = @(Get-SCCustomResource -VMMServer $vmmServer -ErrorAction SilentlyContinue)
        $resources += $customs
    }

    if ($name) {
        $resources = @($resources | Where-Object { $_.Name -eq $name })
    }

    if ($libraryShare) {
        $resources = @($resources | Where-Object { $_.LibrarySharePath -like "*$libraryShare*" -or $_.SharePath -like "*$libraryShare*" })
    }

    $module.Result.resources = @($resources | ForEach-Object {
            ConvertTo-SCVMMDict -InputObject $_ -Properties @('Name', 'SharePath', 'Description', 'Size', 'ID')
        })

}

catch {
    $module.FailJson("Failed to retrieve library resources: $($_.Exception.Message)", $_)
}

$module.ExitJson()
