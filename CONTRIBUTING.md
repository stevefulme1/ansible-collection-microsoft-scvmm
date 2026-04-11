# Contributing to Microsoft SCVMM Collection

Thank you for your interest in contributing to the Microsoft SCVMM Collection! This document provides guidelines for contributing to this project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your contribution
4. **Make your changes** following our guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request**

## Development Environment Setup

### Requirements
- Python 3.12 or later
- Ansible 2.16 or later
- Access to a Windows Server with SCVMM and the `VirtualMachineManager` PowerShell module
- PowerShell 5.1 or later on the SCVMM host

### Setup Steps
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ansible-collection-microsoft-scvmm.git
cd ansible-collection-microsoft-scvmm

# Install development dependencies
pip install -r requirements.txt
pip install -r test-requirements.txt
```

## Types of Contributions

### Module Development
To contribute a new module:
1. Check existing issues and the roadmap to see if the module is planned
2. Comment on the corresponding issue to claim it
3. Follow the module development guidelines below

### Bug Fixes
Found a bug? Please:
1. Check if an issue already exists
2. If not, create a new issue with detailed information
3. Submit a PR with the fix

### Documentation
Documentation improvements are always welcome:
- Module documentation (EXAMPLES, RETURN, parameter descriptions)
- Collection-level documentation (README, guides, tutorials)
- Code comments for complex logic

## Module Development Guidelines

### Module Structure
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: scvmm_example
short_description: Short description of what the module does
description:
  - Longer description of the module.
  - Can be multiple paragraphs.
extends_documentation_fragment:
  - microsoft.scvmm.scvmm_connection
options:
  name:
    description:
      - Name of the resource.
    type: str
    required: true
'''

EXAMPLES = r'''
- name: Example task
  microsoft.scvmm.scvmm_example:
    scvmm_server: scvmm01.example.com
    name: example_resource
    state: present
'''

RETURN = r'''
# Document return values
'''
```

### Module Requirements
1. **Documentation**: Complete DOCUMENTATION, EXAMPLES, and RETURN sections
2. **Error Handling**: Proper exception handling with meaningful error messages
3. **Idempotency**: Modules must be idempotent (safe to run multiple times)
4. **Check Mode**: Support for `--check` mode
5. **Changed Status**: Accurately report when changes are made
6. **Testing**: Include unit tests and integration tests

### PowerShell Integration
Most modules interact with SCVMM via PowerShell cmdlets from the `VirtualMachineManager` module:
- Use the shared `scvmm_connection` doc fragment for connection parameters
- Handle PowerShell errors appropriately
- Support both WinRM and SSH connection methods

## Testing

### Sanity Tests
```bash
ansible-test sanity --python 3.12
```

### Unit Tests
```bash
ansible-test units --python 3.12
```

### Integration Tests
```bash
# Requires an SCVMM host
ansible-test integration scvmm_vm --python 3.12
```

## Code Style

### Python
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Maximum line length: 160 characters (Ansible standard)

### Documentation
- Use proper reStructuredText formatting
- Include complete parameter descriptions with types and defaults
- Provide at least 3 examples showing common use cases
- Document all return values

## Pull Request Process

1. **Branch naming**: Use descriptive names (e.g., `feature/scvmm_vm_module`, `fix/checkpoint-restore`)
2. **Commits**: Write clear commit messages following conventional commit format
3. **Testing**: Ensure all tests pass
4. **Changelog**: Add a changelog fragment in `changelogs/fragments/`
5. **Documentation**: Update relevant documentation
6. **Review**: Address review comments promptly

### Changelog Fragments
Create a file in `changelogs/fragments/` named `<pr_number>-<description>.yml`:

```yaml
---
minor_changes:
  - scvmm_vm - Added support for Generation 2 VMs.
bugfixes:
  - scvmm_vm_state - Fixed issue with VM state detection.
```

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Ansible Forum**: Post questions with the `scvmm` tag

## Code of Conduct

This project follows the [Ansible Code of Conduct](https://docs.ansible.com/projects/ansible/devel/community/code_of_conduct.html). Please read and follow it in all interactions.

## Resources

- [Ansible module development guide](https://docs.ansible.com/projects/ansible/devel/dev_guide/developing_modules_general.html)
- [Ansible collection development guide](https://docs.ansible.com/projects/ansible/devel/dev_guide/developing_collections.html)
- [SCVMM PowerShell reference](https://learn.microsoft.com/en-us/powershell/module/virtualmachinemanager/)

## License

By contributing to this project, you agree that your contributions will be licensed under the GNU General Public License v3.0 or later.
