# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

Function Get-SCVMMConnectionSpec {
    <#
    .SYNOPSIS
    Returns the common argument spec entries for SCVMM connection parameters.
    #>
    [OutputType([hashtable])]
    param ()

    @{
        scvmm_server = @{
            required = $true
            type = "str"
        }
        scvmm_port = @{
            type = "int"
            default = 8100
        }
    }
}

Function Connect-SCVMM {
    <#
    .SYNOPSIS
    Imports the VirtualMachineManager module and connects to the SCVMM server.
    Returns the VMMServer object for use by module cmdlets.
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory)]
        [object]
        $Module
    )

    $server = $Module.Params.scvmm_server
    $port = $Module.Params.scvmm_port

    try {
        Import-Module VirtualMachineManager -ErrorAction Stop
    }
    catch {
        $Module.FailJson("Failed to import VirtualMachineManager PowerShell module: $($_.Exception.Message)", $_)
    }

    try {
        $vmmServer = Get-SCVMMServer -ComputerName $server -TCPPort $port -ErrorAction Stop
    }
    catch {
        $Module.FailJson("Failed to connect to SCVMM server '$server' on port $port`: $($_.Exception.Message)", $_)
    }

    $vmmServer
}

Function ConvertTo-SCVMMDict {
    <#
    .SYNOPSIS
    Converts an SCVMM object to a clean hashtable suitable for module output.
    Handles enum-to-string conversion, datetime formatting, and null values.
    #>
    [OutputType([hashtable])]
    param (
        [Parameter(Mandatory)]
        [object]
        $InputObject,

        [Parameter(Mandatory)]
        [string[]]
        $Properties
    )

    $result = @{}
    foreach ($prop in $Properties) {
        $value = $InputObject.$prop
        if ($null -eq $value) {
            $result[$prop] = $null
        }
        elseif ($value -is [enum]) {
            $result[$prop] = $value.ToString()
        }
        elseif ($value -is [datetime]) {
            $result[$prop] = $value.ToString("o")
        }
        elseif ($value -is [System.Collections.IEnumerable] -and $value -isnot [string]) {
            $result[$prop] = @($value | ForEach-Object {
                    if ($_ -is [enum]) {
                        $_.ToString()
                    }
                    elseif ($_ -is [datetime]) {
                        $_.ToString("o")
                    }
                    else {
                        $_
                    }
                })
        }
        else {
            $result[$prop] = $value
        }
    }

    $result
}

Export-ModuleMember -Function Get-SCVMMConnectionSpec, Connect-SCVMM, ConvertTo-SCVMMDict
