# Testing Guide — microsoft.scvmm

This collection uses a dual-language architecture: Python files provide
argument specifications and documentation, while PowerShell (.ps1) files
contain all CRUD logic using `Ansible.Basic` and `SCVMMConnection.psm1`.

This architecture drives the testing strategy described below.

## Unit Tests

Unit tests validate **Python-side argument specifications only**. They parse
each module's `DOCUMENTATION` YAML string and verify:

- Required parameters are correctly marked
- Parameter types (`str`, `int`, `bool`) are accurate
- Choices/defaults for `state` and other enum options
- Mutual exclusivity is documented (e.g., `cloud` vs `vm_host`)
- The `scvmm_connection` doc fragment is extended

Unit tests do **not** test CRUD logic — that lives in PowerShell and requires
a live SCVMM environment.

### Running unit tests

```bash
# With pytest directly
pip install -r test-requirements.txt
pytest tests/unit/ -v --tb=short

# With nox
pip install nox
nox -s unit

# With coverage
pytest tests/unit/ -v --cov=plugins --cov-report=term-missing
```

### Test files

| File | Module tested |
|------|---------------|
| `tests/unit/plugins/modules/test_scvmm_vm.py` | `scvmm_vm` |
| `tests/unit/plugins/modules/test_scvmm_cloud.py` | `scvmm_cloud` |
| `tests/unit/plugins/modules/test_scvmm_template.py` | `scvmm_template` |
| `tests/unit/plugins/modules/test_scvmm_logical_network.py` | `scvmm_logical_network` |
| `tests/unit/plugins/modules/test_scvmm_host.py` | `scvmm_host` |

## Integration Tests

Integration tests exercise full module functionality against a live SCVMM
server. They require:

- A Windows host running SCVMM 2019 or later
- The `VirtualMachineManager` PowerShell module installed
- WinRM enabled and reachable from the Ansible controller
- A valid Run As account with SCVMM administrative privileges

### Required environment variables

| Variable | Description |
|----------|-------------|
| `SCVMM_SERVER` | Hostname or IP of the SCVMM management server |
| `SCVMM_USER` | Domain\username for WinRM authentication |
| `SCVMM_PASSWORD` | Password for the SCVMM user |
| `SCVMM_TEST_TEMPLATE` | Name of a VM template for create tests (default: `Windows2022-Standard`) |
| `SCVMM_TEST_CLOUD` | Name of a cloud for VM placement tests (default: `Test`) |
| `SCVMM_TEST_HOST_GROUP` | Host group path for cloud tests (default: `All Hosts`) |

### Running integration tests

```bash
# Run all integration targets
ansible-test integration --local --python 3.12 \
  scvmm_template scvmm_host_info scvmm_cloud scvmm_logical_network scvmm_vm

# Run a single target (safe, read-only)
ansible-test integration --local --python 3.12 scvmm_host_info
```

### Integration targets

| Target | Operations | Safety |
|--------|-----------|--------|
| `scvmm_vm` | Create, update, delete VM | **Mutating** — creates/deletes VMs |
| `scvmm_cloud` | Create, delete cloud | **Mutating** — creates/deletes clouds |
| `scvmm_logical_network` | Create, delete network | **Mutating** — creates/deletes networks |
| `scvmm_template` | List, get template info | **Read-only** — safe |
| `scvmm_host_info` | List, get host info | **Read-only** — safe |

### Recommended execution order

Run read-only targets first, then mutating ones:

1. `scvmm_host_info` (read-only)
2. `scvmm_template` (read-only)
3. `scvmm_cloud` (creates/deletes a test cloud)
4. `scvmm_logical_network` (creates/deletes a test network)
5. `scvmm_vm` (creates/deletes a test VM)

## SCVMM Server Configuration

### Minimum requirements

- Windows Server 2019 or later
- System Center Virtual Machine Manager 2019 or later
- VirtualMachineManager PowerShell module
- WinRM configured for remote management

### WinRM setup

```powershell
# Enable WinRM with NTLM authentication
Enable-PSRemoting -Force
winrm set winrm/config/service/auth '@{Basic="true";Negotiate="true";Kerberos="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'

# For HTTPS (recommended in production)
$cert = New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My
winrm create winrm/config/Listener?Address=*+Transport=HTTPS "@{Hostname=`"$env:COMPUTERNAME`";CertificateThumbprint=`"$($cert.Thumbprint)`"}"
```

### Test template preparation

The integration tests expect a VM template named `Windows2022-Standard`
(configurable via `SCVMM_TEST_TEMPLATE`). Create one from a sysprepped
Windows Server 2022 VM or import a VHD into the SCVMM library.

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

- **lint** — ansible-lint with production profile (every push/PR)
- **sanity** — ansible-test sanity checks (every push/PR)
- **unit** — pytest argument spec validation (every push/PR)
- **integration-manual** — full SCVMM integration tests (workflow_dispatch only, requires self-hosted Windows runner)

Integration tests are manual-only because they require a live SCVMM
server that cannot be provisioned in standard CI runners.

## Molecule

A Molecule scenario is provided at `extensions/molecule/default/` for
local integration testing with a delegated driver:

```bash
export SCVMM_SERVER=scvmm01.example.com
export SCVMM_USER='DOMAIN\admin'
export SCVMM_PASSWORD='...'

molecule test
```

The delegated driver expects the SCVMM server to already exist — Molecule
does not provision or tear down the Windows host.
