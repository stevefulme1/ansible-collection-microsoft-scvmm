#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        library_share = @{ type = 'str'; required = $true }
        overwrite = @{ type = 'bool'; default = $false }
        source_path = @{ type = 'str'; required = $true }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$libraryShare = $module.Params.library_share
$action = $module.Params.action

$share = Get-SCLibraryShare -VMMServer $vmmServer | Where-Object { $_.Path -eq $libraryShare }

if ($null -eq $share) {
    $module.FailJson("Library share not found: $libraryShare")
}

if ($action -eq 'refresh') {
    $module.Diff.before = @{ Action = 'none' }
    $module.Diff.after = @{ Action = 'refresh' }

    if (-not $module.CheckMode) {
        Read-SCLibraryShare -LibraryShare $share -ErrorAction Stop
    }
    $module.Result.changed = $true
}
elseif ($action -eq 'remove') {
    $module.Diff.before = ConvertTo-SCVMMDict -InputObject $share -Properties @('Name', 'Description', 'Path', 'ID')
    $module.Diff.after = @{}

    if (-not $module.CheckMode) {
        Remove-SCLibraryShare -LibraryShare $share -ErrorAction Stop
    }
    $module.Result.changed = $true
}

$module.ExitJson()
