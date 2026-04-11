# Microsoft SCVMM Collection Release Notes

**Topics**

- <a href="#v0-3-0">v0\.3\.0</a>
    - <a href="#v030-release-summary">Release Summary</a>
    - <a href="#v030-minor-changes">Minor Changes</a>
- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#v020-release-summary">Release Summary</a>
    - <a href="#v020-minor-changes">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#v010-release-summary">Release Summary</a>
    - <a href="#v010-major-changes">Major Changes</a>
    - <a href="#v010-minor-changes">Minor Changes</a>

<a id="v0-3-0"></a>
## v0\.3\.0

<a id="v030-release-summary"></a>
### Release Summary

Major module expansion — added 71 new modules bringing the collection
to 97 total\. Covers profiles\, services\, update \& compliance\,
bare metal provisioning\, infrastructure configuration\, and
extended networking\, storage\, library\, and RBAC management\.

<a id="v030-minor-changes"></a>
### Minor Changes

* scvmm\_vm\_migrate — VM live/storage migration\.
* scvmm\_vm\_clone — Clone existing VMs\.
* scvmm\_vm\_dvd\_drive — Manage virtual DVD drives\.
* scvmm\_vm\_scsi\_adapter — Manage SCSI controllers\.
* scvmm\_hardware\_profile — Manage hardware profiles\.
* scvmm\_hardware\_profile\_info — Gather hardware profile info\.
* scvmm\_guest\_os\_profile — Manage guest OS profiles\.
* scvmm\_guest\_os\_profile\_info — Gather guest OS profile info\.
* scvmm\_application\_profile — Manage application profiles\.
* scvmm\_application\_profile\_info — Gather application profile info\.
* scvmm\_capability\_profile — Manage capability profiles\.
* scvmm\_capability\_profile\_info — Gather capability profile info\.
* scvmm\_host — Add/configure/remove Hyper\-V hosts\.
* scvmm\_host\_cluster — Manage host clusters\.
* scvmm\_host\_cluster\_info — Gather host cluster info\.
* scvmm\_host\_network\_adapter — Configure host physical NICs\.
* scvmm\_host\_network\_adapter\_info — Gather host NIC info\.
* scvmm\_host\_rating\_info — Get placement ratings\.
* scvmm\_cloud\_capacity — Set cloud capacity limits\.
* scvmm\_cloud\_capacity\_info — Gather cloud capacity info\.
* scvmm\_logical\_network\_definition — Manage network sites\.
* scvmm\_logical\_network\_definition\_info — Gather network site info\.
* scvmm\_vm\_subnet — Manage VM subnets\.
* scvmm\_vm\_subnet\_info — Gather VM subnet info\.
* scvmm\_logical\_switch — Manage logical switches\.
* scvmm\_logical\_switch\_info — Gather logical switch info\.
* scvmm\_uplink\_port\_profile — Manage uplink port profiles\.
* scvmm\_uplink\_port\_profile\_info — Gather uplink port profile info\.
* scvmm\_port\_classification\_info — Gather port classification info\.
* scvmm\_mac\_address\_pool — Manage MAC address pools\.
* scvmm\_mac\_address\_pool\_info — Gather MAC address pool info\.
* scvmm\_ip\_pool\_info — Gather IP pool info\.
* scvmm\_network\_adapter\_info — Gather VM NIC details\.
* scvmm\_load\_balancer — Register/manage load balancers\.
* scvmm\_storage\_classification\_info — Gather storage classification info\.
* scvmm\_storage\_pool — Manage storage pools\.
* scvmm\_storage\_pool\_info — Gather storage pool info\.
* scvmm\_storage\_provider — Register storage providers\.
* scvmm\_storage\_provider\_info — Gather storage provider info\.
* scvmm\_storage\_file\_share\_info — Gather file share info\.
* scvmm\_library\_share — Add/remove library shares\.
* scvmm\_library\_share\_info — Gather library share info\.
* scvmm\_iso\_info — Gather ISO image info from library\.
* scvmm\_script\_info — Gather script resources from library\.
* scvmm\_custom\_resource\_info — Gather custom resources from library\.
* scvmm\_library\_resource — Import resources into library\.
* scvmm\_run\_as\_account — Manage RunAs accounts\.
* scvmm\_run\_as\_account\_info — Gather RunAs account info\.
* scvmm\_user\_role\_quota — Set user role quotas\.
* scvmm\_user\_role\_quota\_info — Gather quota info\.
* scvmm\_service\_template — Manage service templates\.
* scvmm\_service\_template\_info — Gather service template info\.
* scvmm\_service — Deploy/manage service instances\.
* scvmm\_service\_info — Gather service instance info\.
* scvmm\_sql\_profile — Manage SQL profiles\.
* scvmm\_sql\_profile\_info — Gather SQL profile info\.
* scvmm\_update\_server — Register/remove WSUS servers\.
* scvmm\_update\_server\_info — Gather update server info\.
* scvmm\_baseline — Manage update baselines\.
* scvmm\_baseline\_info — Gather baseline info\.
* scvmm\_compliance\_scan — Trigger compliance scans\.
* scvmm\_compliance\_info — Gather compliance status\.
* scvmm\_pxe\_server — Register PXE servers\.
* scvmm\_pxe\_server\_info — Gather PXE server info\.
* scvmm\_physical\_computer\_profile — Manage bare metal profiles\.
* scvmm\_physical\_computer\_profile\_info — Gather bare metal profile info\.
* scvmm\_custom\_property — Manage custom properties\.
* scvmm\_custom\_property\_info — Gather custom property definitions\.
* scvmm\_servicing\_window — Manage servicing windows\.
* scvmm\_servicing\_window\_info — Gather servicing window info\.
* scvmm\_job\_info — Gather VMM job history\.
* Updated extensions/audit/event\_query\.yml with all 97 module entries\.
* Updated README\.md with categorized module catalog\.

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
