.. _client configuration:

Client Configuration and Backup 
===============================

.. contents::
   :local:

1. Overview
-----------

The :silver:`sysadmin` controls the configuration of the system to-be-backed-up, which is termed generically
as the *storage server*. This guide assumes that you have completed the :ref:`client installation
<sysadmin install>` and have your organization's customized :fname:`aws-settings.yaml` in the appropriate location

**Overview of Tasks**

1. "Localize" your server so that it properly can refer to AWS-defined elements 
2. Configure :fname:`jobs.yaml` to reflect your backup jobs 
3. Initial testing of your backup configuration
4. Install cron entries to regularly perform *sync* and *top-up* backups 
5. Start the initial seeding of your backup 

2. Localize the Storage Server
------------------------------

This step needs to be done *in lockstep* with the cloudadmin. The cloudadmin :ref:`on boards <server onboard>` and
transmits critical "username" and "password information".  The cloudadmin and sysadmin need to have identical 
copies of :fname:`aws-settings.yaml`.

Systems are defined by:

* owner
* system name

.. attention::
    The sysadmin and cloudadmin **must use the identical words for owner and system name**. For the examples, this guide
    will use *panteater* as the owner and *labstorage* as the system name.

To enroll your system to backup into AWS,  the sysadmin uses the :fname:`localize.py` script.

.. parsed-literal::

   **cd $RCS3_ROOT/rcs3/POC/sysadmin**
   **./localize.py panteater labstorage**
   Enter AWS Access Key:
   Enter AWS Secret Access Key: 

The cloudadmin will provide you the AWS Access Key and Secret Access Key. These are generated specifically for your
server when the cloudadmin on boards your server.

The following two files are written only if they do not already exist.  You can redo the localization by removing these
files

* :fname:`$RCS3_ROOT/rcs3/POC/config/credentials`
* :fname:`$RCS3_ROOT/rcs3/POC/config/rclone.conf`

The credentials file holds long-term username/password so that rclone can interact with your server-specific 
backup-bucket.  Both files have permissions changed so that only the owner (usually root) can access them. 

.. note::
  The cloudadmin can regenerate credentials for the specific AWS "service account" that performs the backup. If these 
  credentials are lost (or compromised), the backup can still be made accessible. 


3. Create jobs.yaml
-------------------

While *rclone* is the workhorse software that performs that backup, the program :fname:`gen-backup.py` is used to
handle some of the more arcane command-line parameters, create *rclone filters* to select and exclude files/directories
from backup, runs rclone itself, and optionally notifies the sysadmin of start/completion of sync backup jobs.

Backup jobs are defined in the file :fname:`config/jobs.yaml`, which does *NOT* exist on a first time install. The very
first step is to copy a template jobs.yaml file and then edit to reflect your specific server configuration:

.. parsed-literal::

   **cd $RCS3_ROOT/rcs3/POC**
   **cp templates/jobs.yaml config/jobs.yaml**

The file :fname:`config/jobs.yaml` (or just jobs.yaml) is excluded from git so that your local changes can never
be overwritten by a git pull (update of rcs3 itself). The following template is an example file

.. literalinclude:: files/jobs.yaml

jobs.yaml is yaml-formatted with all of the specialized-formatting requirements. There should be no tabs in the file
and indentation is very specific. 

Let's describe the major portions of the file

:bluelight:`path: /`
   The indicates the jobs defined below have included directories *relative* to this path

:bluelight:`exclude_global`: 
   A list of `rclone-compatible filter specifications <https://rclone.org/filtering/>`_ 
   that will be excluded from every backup job. In the case,
   a local decision is made to ignore the contents of all `.git` subdirectories

:bluelight:`exclude_file: common_excludes.yaml`
   This file in :fname:`config/common_excludes.yaml` is list of rclone filters to excludes common patterns that 
   should never be backed up.  This file *can* be updated by a git pull.  If you would like your own version of
   common_excludes.yaml, copy to a new file name in the config directory and then change jobs.yaml to reflect
   your customized version.

:bluelight:`jobs:`
   relative the the path above, you can create multiple backup jobs. Job names (the `name:` key) need to 
   be unique among all backup jobs for this server. There are sound reasons to define multiple backup jobs. 
   For example, the file system has many files and practicality demands  breaking-up the backup into 
   more manageable chunks.

:bluelight:`subdirectories:`
   This is a bullet list of subdirectories in include. In the sample `/volume1` is being backed up as
   job `backup1`

:bluelight:`excludes`:
   This is a bullet list of patterns (defined as rclone filters) to *not backup*.

4. Initial Testing of jobs.yaml
-------------------------------

:bluelight:`list`

It's always a good to test if :fname:`jobs.yaml` is syntactically correct and *looks reasonable*. 
The `list` command in gen-backup.py will provide the set of jobs that will be run

.. parsed-literal::

   **$RCS3_ROOT/rcs3/POC/sysadmin/gen-backup.py list**
   rcs3config /.rcs3/rcs3/POC/config
   backup1 /

This indicates *two* backup jobs:  *rcs3config* and *backup1*.  The first job is *implicit* so that the jobs.yaml file
is recorded in AWS. The second job (backup1) is the name of the job defined explicitly and indicates that the path to
be backed up is ``/``.  Note the details of what will included in backup1 are not included in this brief listing.

:bluelight:`detail`

This command gives the full detail of the rclone filter that will be applied and the rclone command that would be
executed.

.. parsed-literal::

   **$RCS3_ROOT/rcs3/POC/sysadmin/gen-backup.py detail**
    rcs3config /.rcs3/rcs3/POC/config
    == filter contents (output to: /tmp/rcs3config.filter) ==
    + jobs.yaml
    - **
    == command ==
    rclone --config /.rcs3/rcs3/POC/config/rclone.conf \\
    --s3-shared-credentials-file /.rcs3/rcs3/POC/config/credentials \\
    --metadata --links --transfers 2 --checkers 32 --log-level INFO \\
    --log-file /tmp/rcs3config.log --filter-from /tmp/rcs3config.filter sync \\
    /.rcs3/rcs3/POC/config s3-backup:rcs3config/.rcs3/rcs3/POC/config
    =============
    backup1 /
    == filter contents (output to: /tmp/backup1.filter) ==
    - .git/**
    - .zfs/**
    - .snapshot/**
    - .vscode/**
    - .DS_Store/**
    - #snapshot/**
    - #recycle/**
    - @eaDir/**
    - .plist/**
    - .strings
    - .cprestoretmp.*
    - .part
    - .tmp
    - .cache/**
    - .Trash*/**
    - Google/Chrome/.*cache.*
    - Google/Chrome/Safe Browsing.*
    - iPhoto Library/iPod Photo Cache/**
    - Mozilla/Firefox/.*cache.*
    - Music/Subscription/.*
    + volume1/**
    - **
    == command ==
    rclone --config /.rcs3/rcs3/POC/config/rclone.conf \\
    --s3-shared-credentials-file /.rcs3/rcs3/POC/config/credentials \\
    --metadata --links --transfers 2 --checkers 32 --log-level INFO \\
    --log-file /tmp/backup1.log --filter-from /tmp/backup1.filter \\
    sync / s3-backup:backup1/
    =============

There are some key items to take note:

* The rclone filter file is generated (.e.g. :fname:`/tmp/backup1.filter`) and its contents are displayed
* `volume1` is the path include under `/` with the entry `+ volume1/**`.
* All other top-level files and directories under `/` are excluded with the entry `- **`
* Other exclusions (.e.g `- .tmp`) apply to any level in the selected folders

The final `== command ==` stanza shows the full rclone command that would be executed when the backup actually runs.
For the *backup1* job:

* `sync` is the command given to rclone. 
* The source path is `/` and the destination is `s3-backup:backup1/`.  
* `s3-backup` is an rclone remote and was defined when :fname:`localize.py` was executed.

.. note::
   rclone's log of when it runs is shown with the `--log-file` (e.g. :fname:`/tmp/backup1.log`) argument. 


5. Install Cron Entries 
-----------------------

The :fname:`templates/crond.sample` is starting point that should be customized to your desires a sample
below with lines broken up for readability:

.. parsed-literal::

    # Run a full sync Sunday (Day 0) and 1am 
    0 1 * * 0 (/.rcs3/rcs3/POC/sysadmin/gen-backup.py --threads=2 --checkers=32 \\
    --owner=panteater --system=labstorage run >> /var/log/gen-backup.log 2>&1) &
    
    # run top syncs M-Sa (Days 1-6)at 1am
    0 1 * * 1-6 (/.rcs3/rcs3/POC/sysadmin/gen-backup.py --top-up=24h run >> /var/log/gen-backup.log 2>&1) &
   
This is the first exposure to **sync** vs **top-up** backups and the difference is critical to containing cost 
and improving performance.

   :bluelight:`sync`
       This compares the contents of the server and the backup. Updated/New files are uploaded. Deleted files are
       removed from the backup. This translates to AWS api call (head) for every single file in the backup. 

   :bluelight:`top-up`
       This scans the local file system only for any new/changed files in the top-up window (*24 hours* in the example)
       Deleted files are *NOT* removed from the backup. This is very inexpensive as only new data is uploaded. 

The two sample cron entries have comments as to day and time-of-day that *sync* (once per week) and *top-up* (6 days/week) will run. A simple lock file is written to ensure that two versions of :fname:`gen-backup.py` do not run at the same time.

Note that the following two items in the sync entry *should* be changed:

* `--owner=panteater`.  Change *panteater* to the owner of the system being backed up
* `--system=labstorage`.  Change *labstorage* to the name of the system being backed up

5.1 Install the Crontab
^^^^^^^^^^^^^^^^^^^^^^^

Execute the command 

    crontab -e

and paste the contents of the sample crontab setup. Edit to reflect both
the owner and system name.  You can change time and days of the week that your backups run. Please see 
`the crontab man page <https://linux.die.net/man/5/crontab>`_ for more details on the format and meaning
of cron entries.



6. Run the Initial Backup 
-------------------------

You could stop at step 5.1 above and simply wait until cron performed its first sync, but that is not recommended.
Instead, run the **sync** version of the backup, exactly as it is written in your crontab.


.. parsed-literal::
   (/.rcs3/rcs3/POC/sysadmin/gen-backup.py --threads=2 --checkers=32 \\
    --owner=panteater --system=labstorage run >> /var/log/gen-backup.log 2>&1) &

You can follow the progress of the backup by tailing rclone's log file. E.g.,

.. parsed-literal::
   tail -f /tmp/backup1.log


.. attention::

   It can take *days* to *weeks* to seed the first backup. The length of time depends on file system
   performance, network connectivity to AWS, total volume of data, and total number of files to backup.  The 
   rclone log file shows transfer performance every minute.  You can use this to estimate expected duration.
   
