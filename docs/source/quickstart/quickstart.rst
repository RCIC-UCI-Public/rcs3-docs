.. _quickstart:

Quickstart 10K Foot View
========================

.. contents::
   :local:

Overview
--------

There are two logical administrative domains for backup.  Privilege separation between these two domains should be 
maintained so that complete data loss can only occur if both domains are compromised. The domains are:

:silver:`cloudadmin`:
  | controls the AWS-side of the infrastructure, Usually multiple people.
  | :silver:`Cloudadmins` *must be comfortable at the Linux command line prompt*. 

:silver:`sysadmin`:
  | controls the server to be backed up (server)
  | :silver:`Sysadmins` must be willing to perform a small set of tasks at the command line. 

RCS3 has no native graphical interface.
The next section very briefly describes the tasks and provides links to other parts of the documentation for the details.

First Backup
------------

.. table::
   :class: noscroll-table
   :widths: 5 32 27 34

   +------+---------------------------+--------------------------------------+------------------------------------------+
   | Step | **Task**                  |             **Sysadmin**             |           **Cloudadmin**                 |
   +======+===========================+======================================+==========================================+
   |  1   | Prerequisites             | :ref:`Native OS <requirements>`      | :ref:`Native OS <requirements>`          |
   |      |                           |                                      |                                          |
   |      |                           | :ref:`Docker Image <sysadmin ready>` | :ref:`Docker Image <cloudadmin ready>`   |
   |      |                           |                                      |                                          |
   |      |                           | Windows                              |                                          |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  2   | Clone RCS3 Repository     | :ref:`Clone <sysadmin clone>`        | :ref:`Clone <cloudadmin clone>`          |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  3   | One-Time Cloud Config     |                                      | :ref:`Settings <cloudadmin onetime>`     |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  4   | Customize                 | :ref:`Download <sysadmin copy>`      | :ref:`Publish <cloudadmin publish>`      |
   |      | :fname:`aws-settings.yaml`|                                      |                                          |
   |      |                           | from *your* cloudadmin               |                                          |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  5   |  Onboard Server           | :ref:`Run localize.py <localize>`    | :ref:`Allocate Space <server onboard>`   |
   |      |                           |                                      |                                          |
   |      |                           |                                      | :fname:`create-bucket-with-inventory.sh` |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  6   |  Define Backup Jobs       | :ref:`jobs.yaml <define jobs>`       |                                          |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  7   |  Test Backup Config       | :ref:`list/detail <job testing>`     |                                          |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  8   |  Schedule Regular backup  | :ref:`crontab entry <cron>`          |                                          |
   |      |                           |                                      |                                          |
   |      |                           | Windows                              |                                          |
   +------+---------------------------+--------------------------------------+------------------------------------------+
   |  9   |  Seed the Backup          | :ref:`First Backup <seed backup>`    |                                          |
   |      |                           |                                      |                                          |
   |      |                           | :fname:`gen-backup.py` `run`         |                                          |
   +------+---------------------------+--------------------------------------+------------------------------------------+

