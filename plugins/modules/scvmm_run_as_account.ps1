#!powershell
# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
#AnsibleRequires -PowerShell ..module_utils.SCVMMConnection

$connectionSpec = Get-SCVMMConnectionSpec
$spec = @{
    options = $connectionSpec + @{
        credential_type = @{ type = 'str'; choices = @('WindowsCredential', 'CertificateCredential', 'SSHKeyCredential') }
        description = @{ type = 'str' }
        name = @{ type = 'str'; required = $true }
        password = @{ type = 'str'; no_log = $true }
        state = @{ type = 'str'; default = 'present'; choices = @('present', 'absent') }
        username = @{ type = 'str' }
    }
    supports_check_mode = $true
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)
$vmmServer = Connect-SCVMM -Module $module

try {
    $existing = Get-SCRunAsAccount -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue

    $module.Diff.before = if ($existing) {
        ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'CredentialType', 'UserName', 'ID')
    }
    else { @{} }

    if ($module.Params.state -eq 'absent') {
        if ($existing) {
            if (-not $module.CheckMode) {
                Remove-SCRunAsAccount -RunAsAccount $existing -ErrorAction Stop
            }
            $module.Result.changed = $true
            $module.Diff.after = @{}
        }
    }
    else {
        $needsChange = $false

        if (-not $existing) {
            if (-not $module.CheckMode) {
                $securePassword = ConvertTo-SecureString -String $module.Params.password -AsPlainText -Force
                $credential = New-Object System.Management.Automation.PSCredential($module.Params.username, $securePassword)

                $newParams = @{
                    VMMServer = $vmmServer
                    Name = $module.Params.name
                    Credential = $credential
                    ErrorAction = 'Stop'
                }
                if ($module.Params.description) {
                    $newParams.Description = $module.Params.description
                }
                $existing = New-SCRunAsAccount @newParams
            }
            $needsChange = $true
        }
        else {
            $setParams = @{}
            if ($module.Params.description -and $existing.Description -ne $module.Params.description) {
                $setParams.Description = $module.Params.description
                $needsChange = $true
            }
            if ($setParams.Count -gt 0 -and -not $module.CheckMode) {
                Set-SCRunAsAccount -RunAsAccount $existing @setParams -ErrorAction Stop
                $existing = Get-SCRunAsAccount -VMMServer $vmmServer -Name $module.Params.name -ErrorAction SilentlyContinue
            }
        }

        $module.Result.changed = $needsChange
        $module.Diff.after = if ($existing) {
            ConvertTo-SCVMMDict -InputObject $existing -Properties @('Name', 'Description', 'CredentialType', 'UserName', 'ID')
        }
        else {
            @{
                Name = $module.Params.name
                Description = $module.Params.description
                CredentialType = $module.Params.credential_type
                UserName = $module.Params.username
            }
        }
    }

    $module.ExitJson()
}
catch {
    $module.FailJson("Failed to manage Run As account: $($_.Exception.Message)", $_)
}
