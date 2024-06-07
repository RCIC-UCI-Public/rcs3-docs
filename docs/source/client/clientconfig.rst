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

1. *Localize* your server so that it properly can refer to AWS-defined elements 
2. Configure :fname:`jobs.yaml` to reflect your backup jobs 
3. Initial testing of your backup configuration
4. Install cron entries to regularly perform *sync* and *top-up* backups 
5. Start the initial seeding of your backup 

.. _localize: 

2. Localize the Storage Server
------------------------------

This step needs to be done *in lockstep* with the :silver:`cloudadmin`. The :silver:`cloudadmin` :ref:`on boards <server onboard>` and
transmits critical *username* and *password information*.  The :silver:`cloudadmin` and :silver:`sysadmin` need to have identical 
copies of :fname:`aws-settings.yaml`.

Systems are defined by:
    |  owner
    |  system name

.. attention::
   The :silver:`sysadmin` and :silver:`cloudadmin` **must use the identical words for owner and system name**. For the examples, this guide
   will use *panteater* as the owner and *labstorage* as the system name.

To enroll your system to backup into AWS, the :silver:`sysadmin` uses the :fname:`localize.py` script.

.. parsed-literal::

   **cd $RCS3_ROOT/rcs3/POC/sysadmin**
   **./localize.py panteater labstorage**
   Enter AWS Access Key:
   Enter AWS Secret Access Key: 

The :silver:`cloudadmin` will provide you the AWS Access Key and Secret Access Key. These are generated specifically for your
server when the :silver:`cloudadmin` on boards your server.

The following four files are written only if they do not already exist.  You can redo the localization by removing any
subset of these files for which you need to re-localize:

    | :fname:`$RCS3_ROOT/rcs3/POC/config/credentials`
    | :fname:`$RCS3_ROOT/rcs3/POC/config/rclone.conf`
    | :fname:`$RCS3_ROOT/rcs3/POC/config/weekly-backup`
    | :fname:`$RCS3_ROOT/rcs3/POC/config/daily-backup`


The credentials file holds long-term username/password so that rclone can interact with your server-specific 
backup-bucket.  Both :fname:`credentials` and :fname:`rclone.conf` have permissions changed so that only the
owner (usually root) can access them. 

.. note::

   The :silver:`cloudadmin` can regenerate credentials for the specific *AWS service account* that performs the backup. If these 
   credentials are lost (or compromised), the backup can still be made accessible. 


.. note::
   Credentials are rotated automatically after the completion of every backup job. In this sense *long-term* 
   credentials are valid from the *conclusion* of the previous backup job through the completion of the current 
   backup job.  These structure prevents credentials from expiring *during* an active backup session.  


.. _define jobs:

3. Create jobs.yaml
-------------------

While *rclone* is the workhorse software that performs that backup, the program :fname:`gen-backup.py` is used to
handle some of the more arcane command-line parameters, create *rclone filters* to select and exclude files/directories
from backup, runs ``rclone`` itself, and optionally notifies the :silver:`sysadmin` of start/completion of sync backup jobs.

Backup jobs are defined in the file :fname:`config/jobs.yaml`, which *does NOT exist* on a first time install. The very
first step is to copy a template :fname:`jobs.yaml` file and then edit to reflect your specific server configuration:

.. parsed-literal::

   **cd $RCS3_ROOT/rcs3/POC**
   **cp templates/jobs.yaml config/jobs.yaml**

The file :fname:`config/jobs.yaml` (or just :fname:`jobs.yaml`) is excluded from git so that your local changes can never
be overwritten by a git pull (update of rcs3 itself). The following template is an example file:

.. literalinclude:: /admin/files/jobs.yaml

:fname:`jobs.yaml` is yaml-formatted with all of the specialized-formatting requirements. There should be no tabs in the file
and indentation is very specific. 

Let's describe the major portions of the file

:bluelight:`path: /`
   The indicates the jobs defined below have included directories *relative* to this path.

:bluelight:`exclude_global`: 
   A list of `rclone-compatible filter specifications <https://rclone.org/filtering/>`_ 
   that will be excluded from every backup job. In the case,
   a local decision is made to ignore the contents of all :fname:`.git` subdirectories.

:bluelight:`exclude_file: common_excludes.yaml`
   This file in :fname:`config/common_excludes.yaml` is list of rclone filters to excludes common patterns that 
   should never be backed up.  This file *can* be updated by a git pull.  If you would like your own version of
   :fname:`common_excludes.yaml`, copy to a new file name in the :fname:`config/` directory and then change :fname:`jobs.yaml` to reflect
   your customized version.

:bluelight:`jobs:`
   relative the path above, you can create multiple backup jobs. Job names (the `name:` key) need to 
   be unique among all backup jobs for this server. There are sound reasons to define multiple backup jobs. 
   For example, the file system has many files and practicality demands  breaking-up the backup into 
   more manageable chunks.

:bluelight:`subdirectories:`
   This is a bullet list of subdirectories in include. In the sample :fname:`/volume1` is being backed up as
   job `backup1`

:bluelight:`excludes`:
   This is a bullet list of patterns (defined as rclone filters) to *not backup*.

.. _job testing:

4. Initial Testing of jobs.yaml
-------------------------------

:bluelight:`list`

It's always a good to test if :fname:`jobs.yaml` is syntactically correct and *looks reasonable*. 
The `list` command in ``gen-backup.py`` will provide the set of jobs that will be run:

.. parsed-literal::

   **$RCS3_ROOT/rcs3/POC/sysadmin/gen-backup.py list**
   rcs3config /.rcs3/rcs3/POC/config
   backup1 /

This indicates two backup jobs:
  | *rcs3config* 
  | *backup1*

The first job is *implicit* so that the :fname:`jobs.yaml` file
is recorded in AWS. The second job (backup1) is the name of the job defined explicitly and indicates that the path to
be backed up is ``/``.  Note the details of what will included in *backup1* are not included in this brief listing.

:bluelight:`detail`

This command gives the full detail of the rclone filter that will be applied and the ``rclone`` command that would be
executed:

.. parsed-literal::

   **$RCS3_ROOT/rcs3/POC/sysadmin/gen-backup.py detail**
   :gray:`rcs3config /.rcs3/rcs3/POC/config
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
   =============`

There are some key items to take note:

* :fname:`/tmp/backup1.filter` - is the generated rclone filter file, and its * contents are displayed.
* :fname:`+ volume1/**` - is the entry that shows path :fname:`volume1` to include under :fname:`/`.
* :fname:`- **` - is the entry that specifies all other top-level files and * directories under :fname:`/` to be excluded.
* :fname:`- .tmp` - are all other exclusions to  apply to any level in the * selected folders.
* :fname:`== command ==`  - the final stanza shows the full ``rclone`` command that would be executed when the backup actually runs.

  For the *backup1* job:

  * ``sync / s3-backup:backup1/`` is the command given to ``rclone`` where

    -  :fname:`/` - is the source path 
    -  :fname:`s3-backup:backup1/` is the destination 
    -  :fname:`s3-backup` is an rclone remote defined when :fname:`localize.py` was executed.

  .. note::
     rclone's log of when it runs is shown with the `--log-file` (e.g. :fname:`/tmp/backup1.log`) argument. 

.. _cron:

5. Install Cron Entries 
-----------------------

The :fname:`templates/crond.sample` is starting point that should be customized to your desires a sample
below with lines broken up for readability:

.. code-block:: bash

   # Run a full sync Sunday (Day 0) and 1am 
   0 1 * * 0 /.rcs3/rcs3/POC/sysadmin/weekly-backup &
    
   # run top syncs M-Sa (Days 1-6)at 1am
   0 1 * * 1-6 /.rcs3/rcs3/POC/sysadmin/daily-backup &
   
This is the first exposure to **sync** vs **top-up** backups and the difference is critical to containing cost 
and improving performance.  When :fname:`localize.py` was executed the weekly and daily backup scripts were created.
The scripts can be *edited* to modify parameters to :fname:`gen-backup.py`

The :fname:`weekly-backup` contains a line very similar to:

.. parsed-literal::

    /.rcs3/rcs3/POC/sysadmin/gen-backup.py --threads=2 --checkers=32 \\ 
     --owner=panteater --system=labstorage run > /var/log/gen-backup.log 2>&1

The weekly backup is a *sync*

   :bluelight:`sync`
       This **compares the contents of the server and the backup**. Updated/New files are uploaded. Deleted files are
       removed from the backup. This translates to an AWS API call (head) for every single file in the backup. For
       time efficiency, rclone can have multiple outstanding "check requests" in flight. That number is governed
       by the `--checkers`.  For backups with tens of millions of files, setting to larger number  `--checkers=128`
       results in roughly 2000 file checks/second (about 1M checks/10 minutes)  

:fname:`daily-backup` looks very similar but one important difference

.. parsed-literal::

    /.rcs3/rcs3/POC/sysadmin/gen-backup.py --threads=2 --checkers=32 \\
    --owner=panteater --system=labstorage :bluelight:`--top-up=24h` run >> /var/log/gen-backup.log 2>&1

Daily adds the parameter `--top-up`:
 
   :bluelight:`top-up`
       This scans the local file system only for any new/changed files in the top-up window (*24 hours* in the example)
       Deleted files are *NOT* removed from the backup. This is inexpensive becuase (1) only new data is uploaded
       (2) the head API call of *sync* is **not** made on all existing files. 


The two sample cron entries have comments as to day and time-of-day that *sync* (once per week) and *top-up* (6 days/week) will run.
A simple lock file is written to ensure that two versions of :fname:`gen-backup.py` do not run at the same time.

Note that the following two items in the sync entry *should have been* changed when  you
:ref:`localized the storage server <localize>`

* `--owner=panteater`.  Change *panteater* to the owner of the system being backed up
* `--system=labstorage`.  Change *labstorage* to the name of the system being backed up

5.1 Install the Crontab
^^^^^^^^^^^^^^^^^^^^^^^

Execute the command 

.. parsed-literal::

   **crontab -e**

and paste the contents of the sample crontab setup. 
You can change time and days of the week that your backups run. Please see 
the `crontab man page <https://linux.die.net/man/5/crontab>`_ for more details on the format and meaning
of cron entries.

.. _seed backup:

6. Run the Initial Backup 
-------------------------

You could stop at step 5.1 above and simply wait until cron performed its first sync, but that is not recommended.
Instead, run the **sync** version of the backup


.. parsed-literal::

   ** /.rcs3/rcs3/POC/config/weekly-backup & **

You can follow the progress of the backup by tailing rclone's log file, e.g:

.. parsed-literal::

   **tail -f /tmp/backup1.log**


.. attention::

   It can take *days* to *weeks* to seed the first backup. The length of time depends on file system
   performance, network connectivity to AWS, total volume of data, and total number of files to backup.  The 
   rclone log file shows transfer performance every minute.  You can use this to estimate expected duration.
  
7. Advanced Options
-------------------

In this section we describe two advanced options: *using rclone directly* and *client-side encryption*.


.. _rclone direct:

7.1 Using Rclone Directly
^^^^^^^^^^^^^^^^^^^^^^^^^

:fname:`gen-backup.py` ultimately spins off ``rclone`` via python's `subprocess` module. Calling 
:fname:`gen-backup.py` with the ``rclone`` argument will print out rclone command and all flags utilized. E.g.:


.. parsed-literal::

   **./gen-backup.py rclone**
   rclone --config /.rcs3/rcs3/POC/config/rclone.conf \\
   --s3-shared-credentials-file /.rcs3/rcs3/POC/config/credentials \\
   --metadata --links --transfers 2 --checkers 32

You could cut and paste this directly, but a more convenient method is shown in the example below 
where rclone's ``listremotes`` command is used:

.. parsed-literal::

   **$(./gen-backup.py rclone) listremotes**
   s3-backup:
   s3-crypt:
   s3-inventory:
   s3-native:

You can now use any `rclone command <https://rclone.org/commands>`_ but should only limit to commands that
**make no changes**. A particulary convenvient command is ``serve http`` so that  you could use a web
browser to view what is stored in the backup. 

It is recommended that you only serve to localhost and use an 
alternate port.  An example of serving data to localhost over port 8080 in a read-only manner:

.. parsed-literal::

   **$(./gen-backup.py rclone) serve http --read-only --addr localhost:8080 s3-backup:**

Point your browser to :fname:`http://localhost:8080` to view the contents of your backup.
If you are familiar with `ssh tunneling <https://www.ssh.com/academy/ssh/tunneling>`_, it's not
difficult to view remotely.  

:bluelight:`Windows`

The windows installation uses fully-localized versions of git, python, aws, and rclone. RCS3 provides the
wrapper Powershell script :fname:`rclone.ps1`.  The ``listremotes`` example above in Powershell looks like:

.. parsed-literal::

   **./rclone.ps1 listremotes**
   s3-backup:
   s3-crypt:
   s3-inventory:
   s3-native:

In the examples above, you can replace ``$(./gen-backup.py rclone)`` with ``./rclone.ps1``

7.2 Client Side Encryption
^^^^^^^^^^^^^^^^^^^^^^^^^^

Data is stored in S3 in such a way that :silver:`cloudadmins` can view (through download) the contents of 
any file stored in S3.  At most universities, existing policy bars them from doing that *without* the 
data owners knowledge or consent. 
Some data use agreements might demand that data be encrypted on the backup so that only the 
encryption key holder could view the unencrypted contents.  

To address concerns that might arise from the above (or any other rationale for storing data in an 
encrypted form in the backup),
the :silver:`sysadmin` can secure all file content data *prior to transmission* by defining
a :bluelight:`private encryption key`.    There are some important facts when using a *private encryption key*:

* The private key is only known to the holder. If it is lost, no one can assist in recovery.  The private key is not
  known by :silver:`cloudadmins`.  Private key owners :red:`must backup their key`
* The private key *cannot be rotated* without re-uploading new versions of files.  Rclone will encrypt a file prior to
  uploading it into S3. 
* Encrypted and unencrypted files can co-exist in the same backup bucket


**Setup is a few steps:**

  In the examples below use your :ref:`system specific method <rclone direct>` for invoking rclone directly.
  The examples, when appropriate show the Linux variant. The assumption is that you are in the :fname:`sysadmin` 
  directory.

  :bluelight:`1. Define encryption key`
     Use clone natively to define an encryption key on the ``s3-crypt`` endpoint.

     .. parsed-literal::

        **$(./gen-backup.py rclone) config update s3-crypt --all**

     | Take defaults for all questions, have rclone generate the password and the salt,
     | do NOT edit advanced config. The rclone page on `crypted remotes <https://rclone.org/crypt/>`_ provides details. 
     | **Remember to record both the generated password and salt password** 

     .. warning::
        | Save the passwords that were generated in a safe place like BitWarden or 1Password.
        | If you lose this password, no one can restore your data. 

  :bluelight:`2. Recommended: Rename your backup job`.  
     Edit :fname:`jobs.yaml` and adjust the jobname  to reflect that a particular backup job is encrypted.
     Choose a name like `backup1-encrypted`. 

     The following shows the changed contents of an example  :fname:`jobs.yaml` 
     to rename the existing backup job `backup1` to `backup1-encrypted`:

     .. table::
        :class: noscroll-table

        +---------------------------------+------------------------------------+
        |  Before editing                 | After editing                      |
        +=================================+====================================+
        | .. parsed-literal::             | .. parsed-literal::                |
        |                                 |                                    |
        |   jobs:                         |    jobs:                           |
        |     - name: **backup1**         |      - name: **backup1-encrypted** |
        |       subdirectories:           |        subdirectories:             |
        |         - Users/phili/Documents |          - Users/phili/Documents   |
        +---------------------------------+------------------------------------+

  :bluelight:`3. Change the remote that gen-backup.py uses`.  
     Add the ``--endpoint=s3-crypt`` argument to your invocation of :fname:`gen-backup-py` command
     to override the default of ``s3-backup``. Don't forget 
     to update your crontab (or Windows Scheduled Task)  entries.

With the steps above, your data will be encrypted at the source with the passwords that were generated. 


Here's an example session:

.. parsed-literal::

   **$(./gen-backup.py rclone) lsd s3-backup:**        :bluelight:`(1)`
           0 1999-12-31 16:00:00        -1 backup1
           0 1999-12-31 16:00:00        -1 rcs3config
   **./gen-backup.py  --endpoint=s3-crypt run**        :bluelight:`(2)`
   === rcs3config sync started at 2024-04-18 15:43:54.933541
   === backup1-encrypted sync started at 2024-04-18 15:43:54.933541
   === rcs3config completed at 2024-04-18 15:43:56.029525
   === backup1-encrypted completed at 2024-04-18 15:44:42.001963
   All tasks completed.
   **$(./gen-backup.py rclone) lsd s3-backup:**        :bluelight:`(3)`
           0 1999-12-31 16:00:00        -1 backup1-encrypted
           0 1999-12-31 16:00:00        -1 backup
           0 1999-12-31 16:00:00        -1 rcs3config

| :bluelight:`(1)`  Listing the top-level directories of the backup *prior* to performing an encrypted backup 
| :bluelight:`(2)`  Backup data in an encrypted manner
| :bluelight:`(3)`  Listing the top-level directories of the backup *after* the performing the encrypted backup

.. note::
  
   Please notice the dates of `1999-12-31` on the directories.  This is an artifact of S3 in that 
   directories are not objects but are just `string prefixes` with no metadata. Rclone is building support
   for full metadata on directories at the expense of storing another object. 

