# Copyright: (c) 2026, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Nox sessions for the microsoft.scvmm Ansible collection."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import nox

PYTHON = "3.12"


@nox.session(python=PYTHON)
def lint(session):
    """Run ansible-lint with production profile."""
    session.install("ansible-core>=2.16", "ansible-lint>=24.12.2")
    session.run("ansible-lint", "--profile=production", "--skip-list", "sanity")


@nox.session(python=PYTHON)
def unit(session):
    """Run unit tests (argument spec validation only)."""
    session.install("-r", "test-requirements.txt")
    session.run(
        "pytest",
        "tests/unit/",
        "-v",
        "--tb=short",
        "--co" if session.posargs and "collect" in session.posargs else "",
        *[a for a in session.posargs if a != "collect"],
    )


@nox.session(python=PYTHON)
def sanity(session):
    """Run ansible-test sanity checks."""
    session.install("ansible-core>=2.16")
    session.run(
        "ansible-test",
        "sanity",
        "--docker",
        "--python",
        PYTHON,
        "--skip-test",
        "import",  # PowerShell modules cannot be import-tested on Linux
    )
