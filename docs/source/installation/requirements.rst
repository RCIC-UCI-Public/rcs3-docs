.. _requirements:

Requirements
=============

RCS3 requires some very common support software to work properly.  On Windows, we provide a Powershell script 
that downloads local versions of all requirements so that RCS3 is fully self-contained. For Synology, we provide a 
docker image with appropriate software pre-installed.  For generic Linux, the system versions of **Python3** and **Git** are
almost-always sufficient for our needs. Because rclone is a standalone executable, we recommend that a local install
of RCS3 reference a specific version and location for rclone and not rely on system-supplied packages.

1. **Python** version 3.8 or newer

   The main backup driver script :fname:`gen-backup.py` is Python3 only. It has a reasonably light requirement set in
   terms of Python modules (e.g., installed via ``pip3`` ) that go beyond core libraries provided by the most common
   OS-specific Python packages.  This set includes:

   :pyyaml:
       https://pypi.org/project/pyyaml features a complete YAML 1.1 parser, Unicode support, pickle support 
       capable extension API, and sensible error messages. Backup jobs are described in a simple,
       yaml-formatted file.

   :boto3:
       https://pypi.org/project/boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which 
       allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2.

   :psutil:
       https://pypi.org/project/psutil/ is a cross-platform library for process and system monitoring.

   :distro:
       https://pypi.org/project/distro/ is an OS platform information API.

   .. note::
      Python 3.8 or higher is required  because
      boto3 no longer supports older versions of Python.
      We use Python 3.11.x and 3.12.x with no observed issues.

#. **Rclone** version 1.67 or newer

   Rclone https://rclone.org/ does the heavy lifting for RCS3.
   Even with this version, there are some known bugs that are likely to be addressed in future rclone releases.
   We highly recommend that RCS3 use its own copy of rclone so that it can be updated. Pre-compiled versions of rclone
   are standalone executable files.


#. **Git**
   
   The particular version of git https://git-scm.com/ is relatively unimportant because RCS3 utilizes no real
   advanced features of git.  Until RCS3 is "close to final", updates to our small code base, templates,
   helper scripts, and other items will be via git.  


#. **AWS CLI** version 2.11.21 or newer

   Required for the :silver:`cloudadmin`. Recommended for the :silver:`sysadmin`.

   The AWS Command Line Interface (:term:`AWS CLI`) is a unified tool to manage your AWS services. 
   With just one tool to download and configure, you can control multiple AWS services from the command line and 
   automate them through scripts.

.. _install overview:

Install Overview
================

There are two *halves* of RCS3: 

The :silver:`cloudadmin`:
  Initially, the :silver:`cloudadmin` requires more steps to setup because:

  a) RCS3 needs to be lightly customized using :fname:`config/aws-settings.yaml` to reflect a new institution 
  b) Some one-time setup in AWS itself is needed to create a **StorageLens** instance and a basic 
     **CloudWatch** dashboard for monitoring.  

The :silver:`sysdamin`:
  a) The :silver:`sysadmin` is only "complex" because backup jobs need to be specified in an outline (cron) invocation of 
     the driving python-based wrapper :fname:`gen-backup.py` that invokes ``rclone``.
  b) The :silver:`sysadmin` side must be adaptable
     to different targets.  We've successfully run on:

     - RHEL Linux and its derivatives
     - Ubuntu Linux and Debian-derived
     - Synology NAS appliances (via Docker on x86-based hardware only)
     - TrueNAS CORE (FreeBSD-based) and TrueNAS SCALE (Debian-based)
     - Microsoft Windows 11

Basic Config High-level Overview 
--------------------------------

RCS3 is designed around *two* different administrators: the :silver:`sysadmin` and the
:silver:`cloudadmin`.  In rare instances, this may be the same person.

.. important:: In all setups, it is critical to have **completely independent root-level credentials for
               system administrators and cloud administrators**. 
               This *administrative separation prevents a single credential compromise* 
               from being able to destroy both (1) backups in S3 and (2) primary data on in-lab storage servers.

To make RCS3 work, some initial configuration and setup in S3 needs to be
completed by the :silver:`cloudadmin`.  Once that
initial configuration is completed, new systems can be on-boarded. All configuration steps are accomplished from
a command-line prompt (Linux for the :silver:`cloudadmin`, Linux flavors and Microsoft Windows Powershell for a :silver:`sysadmin`)

Roughly speaking, both :silver:`sysadmin` and :silver:`cloudadmin` follow a similar path:

1. Install pre-requisite software
   
   - **Python3** and Python packages PyYAML, boto3, psutls, distro
   - **Git**
   - **Rclone**
   - **AWS CLI** (only for :silver:`cloudadmin`)

#. Clone the git repository

   .. parsed-literal::

      :bluelight:`git clone https://github.com/RCIC-UCI-Public/rcs3.git`

#. Configure a system for backup. 

   There is a :silver:`cloudadmin`-specific setup and a :silver:`sysadmin`-specific setup.

#. Run the backup the first time.
#. Schedule the backup for daily and weekly updates.
#. Optional for :silver:`cloudadmin` - set quotas and update dashboards to reflect the new system.

The :silver:`cloudadmin` runs a single command for each new system that is on-boarded. This command creates backup and
inventory buckets for the new system, creates a service account for the new system, and applies appropriate policy.
The AWS access key and secret key created by the :silver:`cloudadmin` need to be transmitted to the :silver:`sysadmin` securely.

.. note::
   The file :fname:`config/aws-settings.yaml` MUST be the same for all clients and the :silver:`cloudadmin`. 
   This file is listed in :fname:`config/.gitignore` so that local changes are not overwritten.  
   One way to handle this at your site is to define a web location for your site's version 
   of :fname:`config/aws-settings` and have your users copy that *once* as part of their installation.

   These settings should not change over the course of time.  Further ``git pull`` updates from the UCI master 
   branch will leave these settings alone.
