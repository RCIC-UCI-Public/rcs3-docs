.. _sysadmin install:

Client Installation 
===================

.. contents::
   :local:

Overview
--------

The :silver:`sysadmin` is responsible for readying the server to be backed up, defining backup job(s) (paths
to be included and excluded), and setting up a scheduled invocations of the backup via :fname:`gen-backup.py`.

:silver:`Sysadmins` *must be willing to perform some tasks at the Linux/Windows Powershell command line*. 
All RCS3 configuration and implementation is performed with text-based tools with no native GUI.

**Major Steps of Installation**

1. Ready a local system or use our Docker Image for all software prerequisites.
2. Clone the rcs3 repository and keep it in a non-volatile location.
3. Copy your organization's :fname:`aws-settings.yaml`  to specific directory
4. Start the Docker container 

1. Ready a local system
-----------------------

We maintain a docker image ``rcs3uci/rcs3-rocky8``  on  `DockerHub <https://hub.docker.com/r/rcs3uci/rcs3-rocky8>`_ that
can be used on backup servers.  

The system configuration needs to be held outside of the docker image. For brevity, we use the environment
variable :fname:`RCS3_ROOT`  (persistent store). This directory holds the cloned rcs3 git repository,
localized configuration, and the *crontab* for the root user running inside the container. 
The image default is :fname:`RCS3_ROOT=/.rcs3`.

:ref:`More Details <cloudadmin ready>` on running under Singularity or Docker are provided in the :silver:`cloudadmin`'s setup.

1.1 Map Persistent Storage 
^^^^^^^^^^^^^^^^^^^^^^^^^^

A Docker image is both stateless and read-only. This means that when stopped and then restarted, 
it behaves as if the image has been reinstalled from scratch. This means that any configuration to define
the backup must be held in *persistent* storage. This is a folder that is mapped to a certain path in the Docker image.
There are three "volume mappings" required:

1. A folder to hold the backup configuration (for git checkout of the rcs3 repository)
2. A folder to hold the crontab for the container's root user
3. A folder of the data to be backed up (e.g., :fname:`/volume1`)

For brevity, it is assumed that before you start the container for the very first time
you will create these folders using your favorite method on your system:

1. :fname:`/backup-config` is an **existing** (empty) folder to hold the backup configuration 
2. :fname:`/backup-config/crontab` is an **existing** (empty) folder to hold the crontab 

At the command line, you can use the ``docker run`` command to map the above volumes appropriately and get an
interactive shell prompt. The command here is broken into separate lines for
readability:

.. _sysadmin docker shell:

.. parsed-literal::

   **docker run -it \\
              --volume /volume1:/volume1 \\
              --volume /backup-config:/.rcs3 \\
              --volume /backup-config/crontab:/var/spool/cron \\
              rcs3uci/rcs3-rocky8 /bin/bash**
   :bluelight:`RCS3 Docker />`   # you should see this Docker prompt

| 1 :sup:`st` ``--volume`` map makes your real data available to the container
| 2 :sup:`nd` ``--volume`` map provides the space for the git repository and configuration (maps to :fname:`/.rcs3`)
| 3 :sup:`rd` ``--volume`` map provides the space for the crontab configuration (maps to :fname:`/var/spool/cron`)

When you type ``exit`` at the :bluelight:`RCS3 Docker />` prompt, the container will stop running.

.. note::
     Examples in this guide will assume that you are using our Docker image running under either Singularity
     or Docker and that you have mapped a persistent storage areas into the path.

2. Clone the rcs3 repository
----------------------------

The `rcs3 repository <https://github.com/RCIC-UCI-Public/rcs3>`_ is how software is currently being distributed.
At the command prompt of the container, clone the rcs3 github repository:

.. parsed-literal::

   **cd $RCS3_ROOT**
   **git clone https://github.com/RCIC-UCI-Public/rcs3**

Please see :ref:`more details of folder structure<cloudadmin clone>` in the :silver:`cloudadmin` guide.

3. Copy your Organization's aws-settings.yaml
---------------------------------------------

.. attention:: Before you can backup data, the
             :silver:`cloudadmin` **MUST** provide to you a customized 
             :fname:`config/aws-settings.yaml` file to reflect the local institution configuration.

A template settings file is in the
:fname:`/.rcs3/rcs3/POC/templates/aws-settings.yaml` and is the working configuration file that UCI uses.

You need to copy your organization's customized :fname:`aws-settings.yaml` file into 
:fname:`/.rcs3/rcs3/POC/config/aws-settings.yaml`.

.. warning:: Do *NOT* use the template setttings file *as is*. Unless you are at UCI, your backup will never work.

4. Start the Docker Container 
-----------------------------

The Docker container needs to run *all the time*.  It will consume significant CPU resources only when a backup 
is processing. The default "entry point" for the container is to run :fname:`crond`, Linux's service daemon that runs
commands on a scheduled basis.  The command is very similar to :ref:`the interactive prompt example above <sysadmin docker shell>`

.. parsed-literal::

   **docker run** :red:`--name rcs3-backup` \\
              **--volume /volume1:/volume1 \\
              --volume /backup-config:/.rcs3 \\
              --volume /backup-config/crontab:/var/spool/cron \\
              rcs3uci/rcs3-rocky8** :red:`&`

The notable changes from the interactive prompt, are

1. The running container is given a specific name :red:`rcs3-backup`
2. The container is being run in the background :red:`&` 

You can see the that this container is running by executing ``docker ps`` on the physical host:

.. parsed-literal::

    **docker ps**
    :gray:`CONTAINER ID IMAGE               COMMAND                CREATED       STATUS       PORTS NAMES`
    :gray:`76ed12ab78c0 rcs3uci/rcs3-rocky8 "/bin/sh -c '/sbin/c…" 6 minutes ago Up 6 minutes       rcs3-backup`

.. _sysadmin docker shell running:

Shell Prompt in a Running Container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can obtain a shell prompt within this *runnning* docker container: 

.. parsed-literal::

    **docker exec -it rcs3-backup /bin/bash**
    :bluelight:`RCS3 Docker />`


.. attention::
   All configuration/testing of backup/running first backup will assume you are at the prompt in the running
   container
