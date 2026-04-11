# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this collection, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please report security issues by emailing the maintainers or by using
[GitHub's private vulnerability reporting](https://github.com/stevefulme1/ansible-collection-microsoft-scvmm/security/advisories/new).

We will acknowledge your report within 48 hours and work with you to understand
and address the issue before any public disclosure.

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | Yes                |

## Security Best Practices

When using this collection:

- **Credentials**: Never hard-code credentials in playbooks. Use Ansible Vault,
  environment variables, or a secrets manager.
- **WinRM transport**: Use NTLM or Kerberos authentication. Avoid Basic
  authentication over unencrypted connections.
- **SSH keys**: Prefer SSH key-based authentication over password authentication
  when using the SSH connection method.
- **Least privilege**: Configure SCVMM user roles with the minimum permissions
  required for your automation tasks.
