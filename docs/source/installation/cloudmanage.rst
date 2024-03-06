.. _Cloud Management:

Cloud  Management 
=================

.. contents::
   :local:

Overview
--------

The cloud admin (usually multiple people) control the AWS-side of the infrastructure. This guide covers some of
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


Creating System Owner Notifications
-----------------------------------

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
