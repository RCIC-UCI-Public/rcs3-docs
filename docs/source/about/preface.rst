.. _approach:

Approach
--------

**It utilizes some of the following features/technologies:**

  :bluelight:`Object Versioning in AWS S3`
    to provide "snapshot-like" functionality to go back in time for restores

  :bluelight:`AWS Life Cycle Rules`
    | to transition data from S3 to Glacier Deep Archive
    | to retain versions and permanently deleted files

  :bluelight:`Rclone`
    Rclone itself (Swiss army knife of data copy/sync)
  :bluelight:`Convenience scripts`
    | to create IAM Roles, S3 access Policies, service accounts
    | to backup data
    | to restore data from a point in time
  :bluelight:`Some cost-optimization`
    to perform daily uploads of modified data and weekly "syncs" (true-ups)
  :bluelight:`Cost estimations`
    | for storage capacity
    | for ongoing API calls for backups/synchronization
  :bluelight:`Server-side encryption`
    of data at rest

**Logically, control of the backup storage is split into at least two roles for security separation:**

  .. table::
     :widths: 30 70
     :class: noscroll-table

     +---------------------------+-----------------------------------------------------------------------+
     |  **Role**                 | **Can run actions**                                                   |
     +===========================+=======================================================================+
     | :fname:`Sysadmin`         | Upload/download files.                                                |
     |                           |                                                                       |
     |                           | Delete files (but not specific versions)                              |
     +---------------------------+-----------------------------------------------------------------------+
     | :fname:`Cloudadmin`       | Create buckets, service accounts, IAM roles                           |
     |                           |                                                                       |
     |                           | Apply lifecycle rules                                                 |
     +---------------------------+-----------------------------------------------------------------------+
     | :fname:`Deletion Admin`   | Delete buckets                                                        |
     |                           |                                                                       |
     |                           | Create lifecycle rules                                                |
     |                           |                                                                       |
     |                           | Permanently delete data                                               |
     |                           |                                                                       |
     |                           | Permanently delete objects (MFA Required)                             |
     +---------------------------+-----------------------------------------------------------------------+
