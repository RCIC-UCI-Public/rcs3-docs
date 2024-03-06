.. _cloud admin install:

Cloud Installation 
==================

.. contents::
   :local:

Overview
--------

The :bluelight:`cloudadmin` (usually multiple people) control the AWS-side of the infrastructure. 
It is beyond the scope of this
document to describe in detail the web-portal console provided by Amazon. Screenshots will simply presume you know how
to access your AWS account and are comfortable with copying time-limited access keys to a local credentials file for
command-line access.

Cloudadmins *must be comfortable at the Linux command line prompt*. All RCS3 configuration and
implementation is performed with command-line tools from within a local Linux environment.  Access to the AWS console
enables admins to look at various dashboards.

**Major Steps of Installation**

1. Ready a local system or use our Docker Image for all software prerequisites.
2. Clone the rcs3 repository and keep it in a non-volatile location.
3. Make some one-time configuration decisions and make those configuration decisions available to sysadmins.
4. Build out some basic infrastructure components in AWS.

1. Ready a local system
-----------------------

We maintain a docker image ``rcs3uci/rcs3-rocky8``  on  `DockerHub <https://hub.docker.com/r/rcs3uci/rcs3-rocky8>`_ that
can be used on both backup servers and for the :silver:`cloudadmin`. For the :silver:`cloudadmin`, this same image can be used under
`Singularity <https://docs.sylabs.io/guides/3.5/user-guide/introduction.html>`_.

The admin configuration needs to be held outside of the docker image. For brevity, we use the environment
variable :fname:`RCS3_ROOT`  (persistent store). This directory holds the cloned rcs3 git repository,
localized configuration, and ephemeral AWS credentials.   This directory should be bind-mounted so that it is reachable
from within the image. The image default is :fname:`RCS3_ROOT=/.rcs3`.

To start the Docker image using Singularity and persistently storing data in
the existing directory :fname:`/my/rcs3`, use:

.. code-block:: bash

   export SINGULARITYENV_PS1='RCS3 Singularity \w> '
   export SINGULARITY_BIND=/my/rcs3:/.rcs3
   singularity shell docker://rcs3uci/rcs3-rocky8

.. code-block:: bash

   RCS3 Singularity />   # you should see this Singularity prompt


The *PS1* line sets a slightly more meaningful prompt by adding the working
directory while reminding the :silver:`cloudadmins` that they are inside of the container

Optionally, run under Docker instead of Singularity (replace the singularity
command above with the docker command):

.. code-block:: bash

   docker run -it --volume /my/rcs3:/.rcs3 rcs3uci/rcs3-rocky8 /bin/bash

.. code-block:: bash

   RCS3 Docker />    # you should see this Docker prompt


.. note::
     Examples in this guide will assume that you are using our Docker image running under either Singularity
     or Docker and that you have mapped a persistent storage area into :fname:`/.rcs3`.

2. Clone the rcs3 repository
----------------------------

The `rcs3 repository <https://github.com/RCIC-UCI-Public/rcs3>`_ is how software is currently being distributed.
To clone the repo:

.. code-block:: bash

   cd $RCS3_ROOT
   git clone https://github.com/RCIC-UCI-Public/rcs3

The following table briefly describes the repo directory structure under :fname:`rcs3/POC`:

.. table::
   :widths: 30 70
   :class: noscroll-table

   +---------------------------+-----------------------------------------------------------------------+
   |  **Directory**            | **Description**                                                       |
   +===========================+=======================================================================+
   | :fname:`cloudadmin`       | Python and Bash Scripts to configure the AWS environment,             |
   |                           | define backup buckets, set quotas, upload dashboards                  |
   +---------------------------+-----------------------------------------------------------------------+
   | :fname:`common`           | Shared code between :silver:`sysadmin` and :silver:`cloudadmin`.      |
   +---------------------------+-----------------------------------------------------------------------+
   | :fname:`config`           | Location of localized configuration including quotas,                 |
   |                           | :fname:`jobs.yaml`, :fname:`aws-settings.yaml`.                       |
   +---------------------------+-----------------------------------------------------------------------+
   | :fname:`outputs`          | Temporary output files. Used by some scripts.                         |
   +---------------------------+-----------------------------------------------------------------------+
   | :fname:`scripts`          | Python scripts                                                        |
   +---------------------------+-----------------------------------------------------------------------+
   | :fname:`sysadmin`         | Python scripts utilized sysadmins to localize and run the backup      |
   +---------------------------+-----------------------------------------------------------------------+
   | :fname:`templates`        | Various "generic" template files (often JSON) that are localized      |
   |                           | by configuration scripts. These include backup job templates,         |
   |                           | lifecycle rules, templates for dashboards, policy templates and more. |
   +---------------------------+-----------------------------------------------------------------------+

3. One time Configuration
-------------------------

.. attention:: Before any preparation of your AWS environment can be made, the
             :silver:`cloudadmin` **MUST** change various settings in
             :fname:`config/aws-settings.yaml` to reflect the local institution.

A template settings file is in the
:fname:`templates/aws-settings.yaml` and is the working configuration file that UCI uses.


3.1. Set your Institution Name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Replace :rcicorange:`uci`  with your Institution Name in the AWS settings file.
AWS S3 requires all bucket names to have globally unique names. Our approach is to suffix every bucket with
as string that begins with :rcicorange:`uci-p` (UCI Production).

If you are deploying for an entire
institution, e.g., `UCSB <https://www.ucsb.edu>`_ then you can simply substitute all occurrences of :rcicorange:`uci` with
:rcicorange:`ucsb`.  If you are a department, for example, `Electrical and Computer Engineering (ECE) <https://www.ece.ucsb.edu/>`_
then you could substitute :rcicorange:`uci` with :rcicorange:`ucsb-ece`. Use an appropriate substitution for your circumstances.

The following code snippet is an example of using the venerable `sed <https://linux.die.net/man/1/sed>`_ command
to replace :rcicorange:`uci` with :rcicorange:`ucsb-ece` placing the results in the :fname:`config` directory:

.. code-block:: bash

   cd $RCS3_ROOT/rcs3/POC
   sed 's/uci/ucsb-ece/g' templates/aws-settings.yaml > config/aws-settings.yaml

This step will get you down the road quite a ways for your local customization.  We will assume that you have completed
the above step substituting your institutional name appropriately

The next subsections call out the specific areas of the :fname:`aws-settings.yaml` file that you need to address.

.. _aws credentials:

3.2. Get your AWS Credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Login into your AWS Console for Credentials
It is beyond the scope of this guide to explain how to access your AWS web-based console. You should be
able to see a screen image similar to:

.. image:: /images/cloudadmin/CommandLineAccess.png
   :alt: Access Command Line Credentials

Option to access the web console or command-line access.  Click on :guilabel:`Command Line Access` and then paste the contents
of option 2 into the credentials files :fname:`$RCS3_ROOT/.aws/credentials`:

.. image:: /images/cloudadmin/Short-Term-Credentials.png
   :alt: Paste Short Term Credentials

Your :fname:`$RCS3_ROOT/.aws/credentials` file should look similar to the following (keys and tokens below are invalid):

.. code-block:: text

   [314159307276_AWSAdministratorAccess]
   aws_access_key_id=ASIAX3D737VGKZWY2CBF
   aws_secret_access_key=1N4EX4BTU-R2&Z3Aa1o2enaNuzPtd5xrjpf/eoSf3
   aws_session_token=IQoJb3JpZ2luX2VjEIP//////////wEaCXVzLXdlc3QtMiJIMEYCIQCG/lvaXGYZuzSZcYooOlmeOfXe9saVApHJKy+ ...

You also need to add a :rcicorange:`region=xxx` to this block, where *xxx* is a valid AWS region identifier. 
In this example, :rcicorange:`us-west-2` is the region and this file then looks like:

.. code-block:: text

   [314159307276_AWSAdministratorAccess]
   region=us-west-2
   aws_access_key_id=ASIAX3D737VGKZWY2CBF
   aws_secret_access_key=1N4EX4BTU-R2&Z3Aa1o2enaNuzPtd5xrjpf/eoSf3
   aws_session_token=IQoJb3JpZ2luX2VjEIP//////////wEaCXVzLXdlc3QtMiJIMEYCIQCG/lvaXGYZuzSZcYooOlmeOfXe9saVApHJKy+ ...

You can find valid regions using the AWS command line itself by first setting a few environment variables:
:fname:`AWS_SHARED_CREDENTIALS_FILE` (set up by default in the Docker/Singularity Container) and :rcicorange:`AWS_PROFILE`.
For the :fname:`AWS_PROFILE`, need to select the string between the first :rcicorange:`[...string...]`  brackets pair of the credentials file.
The full sequence using the account above is:

.. code-block:: text

   export AWS_PROFILE=314159307276_AWSAdministratorAccess
   export AWS_SHARED_CREDENTIALS_FILE=$RCS3_ROOT/.aws/credentials
   aws account list-regions

This will output a JSON-formatted string that lists all available regions for your account. Select the appropriate
region for your circumstances.

.. note::
   The tokens are time-limited (often valid for 60 minutes).  It's good practice to get fresh tokens and paste
   them into :fname:`$RCS3_ROOT/.aws/credentials` file before you begin any administrative actions. 
   Always make certain that
   when you update the contents of this file, that the *region=* line remains intact.


3.3. Update your AWS Identifying Accounts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must replace your AWS account and region, the original looks similar to:

.. code-block:: text

    #@@@@ The following MUST be localized to the AWS Account @@@@
    profile: "314159307276_AWSAdministratorAccess"
    accountid: "314159307276"
    region: "us-west-2"

.. note::
    The region id here must match the one in :fname:`$RCS3_ROOT/.aws/credentials`.


3.4. Update the admin team notifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RCS3 uses AWS's  `SNS (Simple Notification Service) <https://aws.amazon.com/sns/>`_ to send email alerts.
The admin team name should reflect something meaningful to you.  Replace
:rcicorange:`rcic-team-notify` with something that reflects your organization:

.. code-block:: text

   # 4. Notification for the cloud admin team (region, account, sns-team name)
   admin_notify: "rcic-team-notify"


3.5. Update *trusted* IP addresses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are numerous locks and safeguards that can be put in place to limit access to backup buckets. The default
is that only a per-server service account and the admins can access a servers backup bucket.  We've added IP address
ranging as another obstacle to access.   For UCI, we allow access from on-campus address ranges. These are specific to
UCI and should be changed to reflect your institution:

.. code-block:: text

    # 6. Restrict service accounts to specific array of IP addresses using
    # condition statments in policy definiations. Expected format is d.d.d.d/d
    iprestrictions:
      - "128.200.0.0/16"
      - "128.195.0.0/16"
      - "192.5.19.0/24"


3.6. Make your aws-settings.yaml file available
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:red:`You must make your aws-settings.yaml file available to the systems that you want to backup`.

There are no *secrets* in the :fname:`aws-settings.yaml` file. However, it contains some basic configuration that
every client system must know.
How you make it available is up to you. Source code repositories, private cloud storage, even an email-attachment could
work.


3.7. Initialize the Cloud Backup Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have settled on the precise configuration of :fname:`aws-settings.yaml` file and made it available to your
community, the next step is to initialize the cloud backup environment.  These are one-time actions that put essential
components in place.

.. note::
   These steps assume current credentials

**Step 1: Create the default Storage Lens Configuration**

Many of the custom dashboards require `Amazon Storage Lens <https://aws.amazon.com/s3/storage-lens/>`_ to be configured
to make various metrics available:

.. code-block:: bash

       cd $RCS3_ROOT/rcs3/POC
       cloudadmin/create-storage-lens.sh


**Step 2: Create emails for administrative notifications**

Determine the email addresses of your administrators who should receive notifications for various events and alarms.
You can re-run this at any time.
Each invocation *adds* the emails to the full set of emails for the topic.  Duplicates are ignored:

.. code-block:: bash

       cd $RCS3_ROOT/rcs3/POC
       cloudadmin/create-admin-sns-topic.py -e <email1> [<email> ...]

.. note::
   There is no command-line method provided by AWS to *delete* and email.  In the online AWS web console, you can
   open the Simple Notification Service, go to your admin topic and delete an email from there.

**Step 3: Create the Custom Cost-Estimates Dashboard**

RCS3 creates a custom `Cloudwatch <https://aws.amazon.com/cloudwatch/>`_ monitoring dashboard to give
an overview of resource usage:

.. code-block:: bash

       cd $RCS3_ROOT/rcs3/POC
       cloudadmin/set-cloudwatch-dashboards.py

Once you have created the dashboard above AND you have on-boarded servers for backup, you will eventually see a
display similar to the following.  Please note that the metrics used to create this dashboard utilize AWS-supplied
measurements. Those measurements are updated *daily*, so this is not a real-time view.

The top-line graph describes total data, number of files, cost of storage and API over time, how much is Glacier, and
how much data is in "snapshots" (either deleted or overwritten data). The two line graphs show API cost over time and
storage costs over time.  The time frame is settable (standard Cloudwatch), but we find that 4 week and 3 month graphs
are the most useful.

.. image:: /images/cloudadmin/Cost-Estimates-Dashboard.png
   :alt: Cost Estimates Dashboard
