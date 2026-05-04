#!powershell

# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        name = @{ type = 'str'; required = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        storage_classification = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

$name = $module.Params.name
$state = $module.Params.state
$storageClassification = $module.Params.storage_classification

$current = Get-SCStoragePool -VMMServer $vmmServer -Name $name -ErrorAction SilentlyContinue

if ($state -eq 'present') {
    if ($null -eq $current) {
        $module.FailJson("Storage pools cannot be created directly via SCVMM. They are discovered from storage providers.")
    } else {
        $module.Diff.before = ConvertTo-SCVMMDict -InputObject $current -Properties @('Name', 'TotalManagedSpace', 'RemainingManagedSpace', 'State', 'ID')
        $needsUpdate = $false
        $params = @{ ErrorAction = 'Stop' }

        if ($null -ne $storageClassification) {
            $classification = Get-SCStorageClassification -VMMServer $vmmServer -Name $storageClassification -ErrorAction Stop
            if ($current.StorageClassification -ne $classification) {
                $needsUpdate = $true
                $params.StorageClassification = $classification
            }
        }

        if ($needsUpdate) {
            if (-not $module.CheckMode) {
                $result = Set-SCStoragePool -StoragePool $current @params
                $module.Diff.after = ConvertTo-SCVMMDict -InputObject $result -Properties @('Name', 'TotalManagedSpace', 'RemainingManagedSpace', 'State', 'ID')
            } else {
                $module.Diff.after = $module.Diff.before.Clone()
                $module.Diff.after.StorageClassification = $storageClassification
            }
            $module.Result.changed = $true
        } else {
            $module.Diff.after = $module.Diff.before
        }
    }
} else {
    if ($null -ne $current) {
        $module.FailJson("Storage pools cannot be removed directly. Remove them from the storage provider.")
    } else {
        $module.Diff.before = @{}
        $module.Diff.after = @{}
    }
}

$module.ExitJson()
