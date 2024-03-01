.. _Cloud admin Install:

Cloud Admin Installation and Configuration
==========================================

**Overview**

The cloud admin (usually multiple people) control the AWS-side of the infrastructure. It is beyond the scope of this
document to describe in detail the web-portal console provided by Amazon. Screenshots will simply presume you know how
to access your AWS account and are comfortable with copying time-limited access keys to a local credentials file for 
command-line access. Cloud admins must be comfortable at the Linux command line prompt. All RCS3 configuration and
implementation is performed with command-line tools from within a local Linux environment.  Access to the AWS console
enables admins to look at various dashboards.

**Major Steps of configuration**

1. Ready a local system or use our Docker Image for all software pre-requisites

2. Clone the rcs3 repository and keep it in a non-volatile location

3. Make some one-time configuration decisions and make those configuration decisions available to sysadmins

4. Build out some basic infrastructure components in AWS 

5. On board your first server that you want to back up



**Ready a local system**

We maintain a docker image ``rcs3uci/rcs3-rocky8``  on  `DockerHub <https://hub.docker.com/r/rcs3uci/rcs3-rocky8>`_ that
can be used on both backup servers and for the cloudadmin. For the cloudadmin, this same image can be used under 
`Singularity <https://docs.sylabs.io/guides/3.5/user-guide/introduction.html>`_.

The admin configuration needs to be held outside of the docker image. For brevity, we use the environment
variable ``RCS3_PSTORE``  (persistent store). This directory holds the cloned rcs3 git repository, 
localized configuration, and ephemeral AWS credentials.   This diretory should be bind-mounted so that it is reachable 
from within the image. The image defaults ``RCS3_PSTORE=/.rcs3``. 

To start the Docker image using Singularity and persistently storing data in the existing directory``/my/store``, use:

.. code-block:: bash

   export SINGULARITYENV_PS1='Singularity \w> '
   export SINGULARITY_BIND=$HOME/.rcs3:/.rcs3
   singularity shell docker://rcs3uci/rcs3-rocky8 
   Singularity />  

.. note:: The *PS1* line sets a slightly more meaningful prompt by adding the working directory

Examples in this guide will assume that you using our Docker image.

**Clone the rcs3 repository**

The `rcs3 repository <https://github.com/RCIC-UCI-Public/rcs3>`_ is how software is currently being distributed.
To clone the repo 

.. code-block:: bash

   cd $RCS3_PSTORE
   git clone https://github.com/RCIC-UCI-Public/rcs3 

The directories in the repo are currently under rcs3/POC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - ``sysadmin`` :
     Python scripts utilized sysadmins to localize and run the backup
  - ``cloudadmin``:
     Python and Bash Scripts to configure the AWS environment, define backup buckets, set quotas, upload dashboards
  -  ``outputs``:
     Temporary output files. Used by some scripts.
  -  ``common``: 
     Shared code between sysadmin and cloudadmin.
  -  ``templates``: 
     Various "generic" template files (often JSON) that are localized by configuration scripts. These include backup
     job templates, lifecycle rules, templates for dashboards, policy templates and more.
  -  ``config``:
     Location of localized configuration including quotas, jobs.yaml, aws-settings.yaml. 

**One time Configuration - aws-settings.yaml**

Before any preparation of your AWS environment can be made, the cloudadmin **MUST** change various settings in
the ``config/aws-settings.yaml`` to reflect the local institution. 




**Prerequisites**

1. ``Python 3``. Required python modules: ``name1``, ``name2``, ``name3``. 

2. Install AWS S3 command line tools.
   
3. Install rclone

.. _building:

Building
----------

Do the following in the top-level directory

.. code-block:: bash

   ./some-script.sh

After this step is complete the following files are generated:

- ``file1`` 
- ``file2`` 
- ``file3`` 

In order to proceed with next steps execute the following commands:

.. code-block:: bash

   command1.sh
   command2.py args1 arg2 

