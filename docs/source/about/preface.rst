.. _approach:

Approach
--------

It utilizes some of the following features/technologies

- Object Versioning in AWS S3 to provide "snapshot-like" functionality to go back in time for restores
- AWS Life Cycle Rules to transition data from S3 to Glacier Deep Archive
- AWS Life Cycle Rules to retain versions and permanently deleted files
- Rclone itself (Swiss army knife of data copy/sync)
- Convenience scripts to create: IAM Roles, S3 access Policies,service accounts
- Convenience scripts to backup data
- Convenience scripts to restore data from a point in time
- Some cost-optimization to perform daily uploads of modified data and weekly "syncs" (true-ups)
- Cost estimations for both storage capacity and ongoing API calls for backups/synchronization
- Server-side encryption of data at rest.

Logically, control of the backup storage is split into at least two for security separation

:Sysadmin:
  Can upload/download files. Can Delete Files (but not specific versions)
:Cloud Admin:
  Can Create Buckets, Service Accounts, IAM Roles, Apply Lifecycle rules
  Can Delete Buckets, Create Lifecycle Rules, Permanently Delete Data, Permanently Delete Objects (MFA Required)
