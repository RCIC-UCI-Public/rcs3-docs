.. _quickstart:

Quickstart 10K Foot View
========================

.. contents::
   :local:

Overview
--------

There are two logical adminstrative domains for backup.  Privilege separation between these two domains should be 
maintained so that complete data loss can only occur if both domains are compromised. The domains are:

* The :bluelight:`cloudadmin` (usually multiple people) controls the AWS-side of the infrastructure. 
* The :bluelight:`sysadmin` controls the server to be backed up (server)

Cloudadmins *must be comfortable at the Linux command line prompt*.  Sysadmins must be willing to perform
a small set of tasks at the command line.  RCS3 has no native graphical interface. The next section very
briefly describes the tasks and provides links other parts of the documentation for the details.

First Backup
------------

.. table::
   :widths: 20 40 40

   +--------------------------------+--------------------------------------+---------------------------------------+
   | **Task**                       |             **Sysadmin**             |           **Cloudadmin**              |
   +================================+======================================+=======================================+
   | 1. Prerequisites               | :ref:`Native OS <requirements>`      | :ref:`Native OS <requirements>`       |
   |                                |                                      |                                       |
   |                                | :ref:`Docker Image <sysadmin ready>` | :ref:`Docker Image <cloudadmin ready>`|
   |                                |                                      |                                       |
   |                                | Windows                              |                                       |
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 2. Clone RCS3 Repository       | :ref:`Clone <sysadmin clone>`        | :ref:`Clone <cloudadmin clone>`       |
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 3. One-Time Cloud Config       |                                      | :ref:`Settings <cloudadmin onetime>`  |
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 4. :fname:`aws-settings.yaml`  | :ref:`Copy <sysadmin copy>`          | :ref:`Publish <cloudadmin publish>`   |
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 5. Onboard Server              | :ref:`Run localize.py <localize>`    | :ref:`Allocate Space <server onboard>`|
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 6. Define Backup Jobs          | :ref:`jobs.yaml <define jobs>`       |                                       |
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 7. Test Backup Config          | :ref:`list/detail <job testing>`     |                                       |
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 8. Schedule Regular backup     | :ref:`crontab entry <cron>`          |                                       |
   |                                |                                      |                                       |
   |                                | Windows                              |                                       |
   +--------------------------------+--------------------------------------+---------------------------------------+
   | 9. Seed the Backup             | :ref:`First Backup <seed>`           |                                       |
   +--------------------------------+--------------------------------------+---------------------------------------+

