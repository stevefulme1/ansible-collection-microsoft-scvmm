# Microsoft SCVMM Collection Release Notes

**Topics**

- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#v020-release-summary">Release Summary</a>
    - <a href="#v020-minor-changes">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#v010-release-summary">Release Summary</a>
    - <a href="#v010-major-changes">Major Changes</a>
    - <a href="#v010-minor-changes">Minor Changes</a>

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="v020-release-summary"></a>
### Release Summary

Added community and governance files\, requirements files\,
CODEOWNERS\, and codecov configuration\.

<a id="v020-minor-changes"></a>
### Minor Changes

* Added CODE\_OF\_CONDUCT\.md\, CONTRIBUTING\.md\, SECURITY\.md\, MAINTAINERS\, and REVIEW\_CHECKLIST\.md\.
* Added CHANGELOG\.rst and CHANGELOG\.md rendered release notes\.
* Added requirements\.txt\, test\-requirements\.txt\, and bindep\.txt\.
* Added CODEOWNERS file\.
* Added codecov\.yml for coverage path mapping\.
* Fixed CI workflow \— pinned ansible\-test\-gh\-action to SHA \(v1\.17\.0\) and bumped ansible\-lint to 25\.2\.0 for ansible\-core 2\.20 compatibility\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary"></a>
### Release Summary

Initial release of the Microsoft SCVMM collection for Ansible\.
Provides 26 modules for managing SCVMM infrastructure via
PowerShell over WinRM or SSH\.

<a id="major-changes"></a>
### Major Changes

* Initial collection scaffold with GPL\-3\.0\-or\-later license\.
* Requires ansible\-core \>\= 2\.16\.0 and Python \>\= 3\.12\.
* Supports both WinRM and SSH connection methods\.
* Zero collection dependencies \— only requires pywinrm or pypsrp on the controller and the VirtualMachineManager PowerShell module on the target host\.

<a id="minor-changes"></a>
### Minor Changes

* scvmm\_vm \— Create\, modify\, and remove virtual machines\.
* scvmm\_vm\_info \— Gather information about virtual machines\.
* scvmm\_vm\_state \— Manage VM power state \(start\, stop\, suspend\, resume\)\.
* scvmm\_vm\_checkpoint \— Manage VM checkpoints \(create\, delete\, restore\)\.
* scvmm\_vm\_checkpoint\_info \— Gather information about VM checkpoints\.
* scvmm\_vm\_disk \— Attach and detach virtual hard disks to VMs\.
* scvmm\_vm\_nic \— Manage virtual network adapters on VMs\.
* scvmm\_template \— Create\, modify\, and remove VM templates\.
* scvmm\_template\_info \— Gather information about VM templates\.
* scvmm\_cloud \— Create\, modify\, and remove SCVMM clouds\.
* scvmm\_cloud\_info \— Gather information about SCVMM clouds\.
* scvmm\_host\_group \— Manage host groups\.
* scvmm\_host\_group\_info \— Gather information about host groups\.
* scvmm\_host\_info \— Gather information about Hyper\-V hosts\.
* scvmm\_logical\_network \— Create\, modify\, and remove logical networks\.
* scvmm\_logical\_network\_info \— Gather information about logical networks\.
* scvmm\_vm\_network \— Create\, modify\, and remove VM networks\.
* scvmm\_vm\_network\_info \— Gather information about VM networks\.
* scvmm\_ip\_pool \— Manage static IP address pools\.
* scvmm\_port\_classification \— Manage port classifications\.
* scvmm\_virtual\_hard\_disk \— Create and remove virtual hard disks \(VHD/VHDX\)\.
* scvmm\_virtual\_hard\_disk\_info \— Gather information about virtual hard disks\.
* scvmm\_storage\_classification \— Manage storage classifications\.
* scvmm\_library\_server\_info \— Gather information about library servers\.
* scvmm\_user\_role \— Manage user roles \(RBAC\)\.
* scvmm\_user\_role\_info \— Gather information about user roles\.
