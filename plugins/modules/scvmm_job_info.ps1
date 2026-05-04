#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        job_id = @{ type = 'str' }
        recent = @{ type = 'int' }
        status = @{ type = 'str'; choices = @('Running', 'Completed', 'Failed', 'Canceled') }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $jobs = if ($module.Params.id) {
        Get-SCJob -VMMServer $vmmServer -ID $module.Params.id -ErrorAction SilentlyContinue
    }
    else {
        $jobParams = @{
            VMMServer = $vmmServer
        }
        if ($module.Params.status) {
            $jobParams.Status = $module.Params.status
        }
        Get-SCJob @jobParams | Select-Object -First $module.Params.most_recent
    }

    $result = @()
    foreach ($job in $jobs) {
        $result += ConvertTo-SCVMMDict -InputObject $job -Properties @(
            'Name', 'ID', 'Status', 'StartTime', 'EndTime', 'Progress', 'ResultName'
        )
    }

    $module.Result.jobs = $result
    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to retrieve jobs: $($_.Exception.Message)", $_)
}
