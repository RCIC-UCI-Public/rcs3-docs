.. _Cloud Management:

Cloud  Management 
=================

.. contents::
   :local:

Overview
--------

The :bluelight:`cloudadmin` (usually multiple people) control the AWS-side of the infrastructure. 
This guide covers some of
ongoing management.  Your AWS cloud infrastructure must have already been initialized using :ref:`cloud admin install`
and that your time-limited credentials are current as described in :ref:`Get Your AWS Credentials <aws credentials>` 

**Common Adminstrative Tasks**

    1. On board a new server 
    2. Creating System Owner Notifications
    3. Setting Quotas and Alarms
    4. Updating Dashboards that have per-bucket components
    5. Interpreting Dashboards and Storage Lens
    6. Digging into a few AWS Console capabilities  
    7. Emptying and Deleting a backup bucket

On-board a new server 
------------------------

On-boarding a new server is wrapped into a single administrative script  :fname:`create-bucket-with-inventory.sh`. 
This script requires two arguments: *id of owner*, *name of system*.   This wrapper performs a number of operations:

    1. Creates a backup bucket
    2. Creates an inventory bucket
    3. Creates a service account for the server
    4. Creates access policies 
    5. Applies access policy to both buckets
    6. Applies lifecycle and inventory policy to backup bucket
    7. Prints out access key and secret access key for service account (must securely transfer to sysadmin)


**Example** 

Suppose the owner *panteater* has the system *labstorage*, the :silver:`cloudadmin` would do the following:

.. _Cloudadmin New Server:

.. code-block:: bash

    cd $RCS3_ROOT/rcs3/POC/cloudadmin
    ./create-bucket-with-inventory.sh panteater labstorage

The output from this script is fairly terse. Here's the full output onboarding :bluelight:`panteater's labstorage` 
system in UCI's staging environment.  

.. code-block:: json

    {
        "Location": "http://panteater-labstorage-uci-s-bkup-bucket.s3.amazonaws.com/"
    }
    {
        "Location": "http://panteater-labstorage-uci-s-inventory.s3.amazonaws.com/"
    }
    {
        "Policy": {
            "PolicyName": "panteater-labstorage-uci-bkup-policy",
            "PolicyId": "ANPASNSBJDU4S4KXJOTFF",
            "Arn": "arn:aws:iam::166566894905:policy/panteater-labstorage-uci-bkup-policy",
            "Path": "/",
            "DefaultVersionId": "v1",
            "AttachmentCount": 0,
            "PermissionsBoundaryUsageCount": 0,
            "IsAttachable": true,
            "CreateDate": "2024-03-05T19:02:30+00:00",
            "UpdateDate": "2024-03-05T19:02:30+00:00"
        }
    }
    {
        "User": {
            "Path": "/",
            "UserName": "panteater-labstorage-sa",
            "UserId": "AIDASNSBJDU47DKWTVVVU",
            "Arn": "arn:aws:iam::166566894905:user/panteater-labstorage-sa",
            "CreateDate": "2024-03-05T19:02:31+00:00"
        }
    }
    {
        "AccessKey": {
            "UserName": "panteater-labstorage-sa",
            "AccessKeyId": "A******************R",
            "Status": "Active",
            "SecretAccessKey": "G***************************y",
            "CreateDate": "2024-03-05T19:02:33+00:00"
        }
    }


In the above output the sections are:

:Location:
  shows the backup and inventory buckets S3 URLs. Can be more than one.
:Policy:
  shows the attachment of the full policy document.
:User: 
  shows the name of the service account user :fname:`panteater-labstorage-sa`.
:AccessKey:
  shows the access key and secret key for the service account user.


.. note:: 
   The fields **AccessKeyID** and the **SecretAccessKey** need to be transmitted to sysadmin when they "localize" 
   the settings for their server. 

The :fname:`templates` directory holds the JSON files where policies are defined. For example, the file 
:fname:`lifecycle-all.json` hold the definitions for both tiering to Glacier ('Tiered-Storage') and retention of 90 days ('Delayed-Delete') policies.  The file :fname:`template-policy2.json` has elements replaced to reflect the current 
system and then is applied as a permissions policy (notably, removing the service account's ability to delete
non-current (snapshot) data or it's ability to change any bucket policy).

Host IP Restrictions
^^^^^^^^^^^^^^^^^^^^

When  :fname:`config/aws-settings.yaml` was localized, a set of valid IP subnetworks should have been declared to 
reflect your instituion.  The effect of this is that any host on these subnets that has a copy of the service 
account secrets can access the backup bucket.   
A tighter restriction is to limit specifically to the backup host IP address or its subnet. 

The following example uses the option :bluelight:`-n` (network) argument when creating the bucket. In this case, 
it limits to a single IPv4 address. Attempting to access the backup bucket using the service account from any other
address will be denied.

.. code-block:: bash

   create-bucket-with-inventory.sh -n 128.195.216.147/32 panteater labstorage

You can validate this restriction by logging on to your AWS web console, accessing the IAM service dashboard, and 
selecting user-defined policies. In this example, it is the policy named 
:bluelight:`panteater-labstorage-uci-bkup-policy`.  The summary view of this policy shows explict Deny and Allow 
Sections. Please take note of the *SourceIP| IP address* restriction that has been properly set to 
:bluelight:`128.195.216.147/32`. 

.. image:: /images/cloudadmin/IP-Policy-Restriction.png
   :alt: IP Host Restriction 

Creating System Owner Notifications
-----------------------------------

AWS `SNS (Simple Notification Service) <https://aws.amazon.com/sns/>`_ is used to inform system owners/administrators
of alarms for their bucket.  Every system should have its own notification channel, but it is not a strict requirement.
The script ``cloudadmin/create-sns-topic.py``  is used to create a notification list (topic). An example call looks like

.. code:: bash

   RCS3 Docker /.rcs3/rcs3/POC/cloudadmin> ./create-sns-topic.py panteater labstorage -e ppapadop@uci.edu
   RCS3 Docker /.rcs3/rcs3/POC/cloudadmin> 

You can supply multiple emails and/or make multiple invocations of ``create-sns-topic.py``.  The recipient of the SNS
notification must *confirm their subscription*. They will be sent an e-mail from AWS that is similar to:

.. image:: /images/cloudadmin/User-SNS-email.png
   :alt: SNS Confirmation e-mail. 

Using CLI to Verify Subscriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section is optional, but one can view the details of subscriptions without logging on to the AWS console. 
Both the  *cloudadmin* and the *sysadmin* can use the aws cli to list all available topics (permissions limit the sysadmin to only list their topic).  One can also view the details of a specific topic.
Here's example output for UCI's testing environment

.. code:: bash

    RCS3 Docker /.rcs3/rcs3/POC/cloudadmin> export AWS_PROFILE=166566894905_AWSAdministratorAccess
    RCS3 Docker /.rcs3/rcs3/POC/cloudadmin> aws sns list-topics
    {
        "Topics": [
            {
                "TopicArn": "arn:aws:sns:us-west-2:166566894905:aws-controltower-SecurityNotifications"
            },
            {
                "TopicArn": "arn:aws:sns:us-west-2:166566894905:panteater-labstorage-uci-notify"
            },
            {
                "TopicArn": "arn:aws:sns:us-west-2:166566894905:ppapadop-mass-uci-notify"
            },
            {
                "TopicArn": "arn:aws:sns:us-west-2:166566894905:rcic-team-notify"
            }
        ]
    }

The topic that was created in the previous step has the Amazon Resource Name (ARN) of
``arn:aws:sns:us-west-2:166566894905:panteater-labstorage-uci-notify``.  To see the details of the particular topic,
one uses the ``list-subscriptions-by-topic`` subcommand of ``sns``:

.. code:: bash

    RCS3 Docker /.rcs3/rcs3/POC/cloudadmin> aws sns list-subscriptions-by-topic --topic-arn=arn:aws:sns:us-west-2:166566894905:panteater-labstorage-uci-notify
    {
        "Subscriptions": [
            {
                "SubscriptionArn": "arn:aws:sns:us-west-2:166566894905:panteater-labstorage-uci-notify:7ae82878-ae6e-4721-8c38-b03fc53eb244",
                "Owner": "166566894905",
                "Protocol": "email",
                "Endpoint": "ppapadop@uci.edu",
                "TopicArn": "arn:aws:sns:us-west-2:166566894905:panteater-labstorage-uci-notify"
            }
        ]
    }


Setting Quotas and Alarms
-------------------------

Updating Dashboards that have per-bucket components
---------------------------------------------------

Interpreting Dashboards and Storage Lens
----------------------------------------

Digging into a few AWS Console capabilities
-------------------------------------------

Emptying and Deleting a backup bucket
-------------------------------------
