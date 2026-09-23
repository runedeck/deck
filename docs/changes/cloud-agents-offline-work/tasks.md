# Tasks

## 1. Implementation

- [x] 1.1 Verify every pinned release asset on each installer run and replace an existing binary with the verified one
- [x] 1.2 Stop before extraction on a digest mismatch
- [x] 1.3 Install the standalone `mdschema` validator through verified release installation
- [x] 1.4 Apply the commit attribution contract to outgoing commits and explicit-bookmark pushes

## 2. Verification

- [x] 2.1 Run the installer regression suite in the quality workflow with local assets and isolated paths

## 3. In-house environment

- [ ] 3.1 A KVM-hosted agent environment installs the pinned tools and pushes under a roster identity, as the Cursor cloud one does
