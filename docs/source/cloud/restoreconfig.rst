.. _Configure Self-Service Restore:

Configure Self-Service Restore
==============================

.. contents::
    :local:

Generic Settings
----------------

.. note::
    these could be user specific if needed to address security or operational concerns;
    these are generic to reduce the overall number and complexity of the policies and 
    the roles we need to manage.

**Athena Access**
  |  *lambda-generic-createAthenaQueries-policy*
  |  *lambda-generic-createAthenaQueries-role*
  |  *createAthenaQueries lambda function*
  |  */aws/lambda/createAthenaQueries log group*

  .. parsed-literal::
     :bluelight:`create-service-account-restore-policy.py lambda generic createAthenaQueries`
     :bluelight:`create-service-account-restore-role.py lambda generic createAthenaQueries`
     :bluelight:`create-service-account-restore-lambda.py lambda generic createAthenaQueries`

  The first command reads the file in :fname:`templates/self-service/createAthenaQueries-policy.json` and gives
  permissions for using the Athena and Glue services.

  The second command combines the newly created lambda-generic-createAthenaQueries-policy with the file in
  :fname:`templates/self-service/createAthenaQueries-trust.json` which allows a lambda function to
  use Athena and Glue services.

  The third command loads the python code in scripts/lambda-createAthenaQueries.py, applies the newly
  created lambda-generic-createAthenaQueries-role, and configures the CloudWatch log group
  /aws/lambda/createAthenaQueries for debugging output.

**S3 Batch Job Submission**
  |  *lambda-generic-createS3BatchInput-policy*
  |  *lambda-generic-createS3BatchInput-role*
  |  *createS3BatchInput lambda function*
  |  */aws/lambda/S3BatchInput log group*

  .. parsed-literal::
     :bluelight:`create-service-account-restore-policy.py lambda generic createS3BatchInput`
     :bluelight:`create-service-account-restore-role.py lambda generic createS3BatchInput`
     :bluelight:`create-service-account-restore-lambda.py lambda generic createS3BatchInput`

  The first command reads the file in :fname:`templates/self-service/createS3BatchInput-policy.json` and gives
  permissions for using the S3 Batch services.

  The second command combines the newly created lambda-generic-createS3BatchInput-policy with the file in
  :fname:`templates/self-service/createS3BatchInput-trust.json` which allows a lambda function to
  use S3 Batch services.

  The third command loads the python code in scripts/lambda-createS3BatchInput.py, applies the newly
  created lambda-generic-createS3BatchInput-role, and configures the CloudWatch log group
  /aws/lambda/createS3BatchInput for debugging output.

**S3 Batch Job Status**
  |  *lambda-generic-pollCreateJobStatus-policy*
  |  *lambda-generic-pollCreateJobStatus-role*
  |  *pollCreateJobStatus lambda function*
  |  */aws/lambda/pollCreateJobStatus log group*

  .. parsed-literal::
     :bluelight:`create-service-account-restore-policy.py lambda generic pollCreateJobStatus`
     :bluelight:`create-service-account-restore-role.py lambda generic pollCreateJobStatus`
     :bluelight:`create-service-account-restore-lambda.py lambda generic pollCreateJobStatus`

  The first command reads the file in :fname:`templates/self-service/pollCreateJobStatus-policy.json` and gives
  permissions for poll S3 Batch job status and output.

  The second command combines the newly created lambda-generic-pollCreateJobStatus-policy with the file in
  :fname:`templates/self-service/pollCreateJobStatus-trust.json` which allows a lambda function to
  use poll S3 Batch job status and output.

  The third command loads the python code in scripts/lambda-pollCreateJobStatus.py, applies the newly
  created lambda-generic-pollCreateJobStatus-role, and configures the CloudWatch log group
  /aws/lambda/pollCreateJobStatus for debugging output.

User Specific Settings
----------------------

.. note::
  In the following examples, panteater should be replaced by the service account; and
  labstorage should be replaced by the hostname.

**Athena workgroup**
  | *panteater Athena workgroup*
  | *reports-bucket/panteater S3 save location*

  .. parsed-literal::
     :bluelight:`create-athena-workgroup.py panteater labstorage`

  Creates an Athena workgroup for the service-account and sets a default location for saving
  output from Athena queries.  Allows metrics to be published to CloudWatch.

**S3 Batch access**
  |  *panteater-labstorage-s3batch-perms-policy*
  |  *panteater-labstorage-s3batch-perms-role*

  .. parsed-literal::
     :bluelight:`create-service-account-restore-policy.py panteater labstorage s3batch-perms`
     :bluelight:`create-service-account-restore-role.py panteater labstorage s3batch-perms`

  The first command reads the file in :fname:`templates/self-service/restore-s3batch-perms-policy.json`
  and gives permission to restore an object to the backup bucket associated with the service
  account and write results to the reports bucket.

  The second command combines the newly created panteater-labstorage-s3batch-perms-policy
  with the file in :fname:`templates/self-service/restore-s3batch-perms-trust.json` which allows an
  S3 Batch job to restore files to a specific bucket and save job reports to a specific bucket.

**Step Function access**
  |  *panteater-labstorage-stepfunc-perms-policy*
  |  *panteater-labstorage-stepfunc-perms-role*

  .. parsed-literal::
     :bluelight:`create-service-account-restore-policy.py panteater labstorage stepfunc-perms`
     :bluelight:`create-service-account-restore-role.py panteater labstorage stepfunc-perms`

  The first command reads the file in :fname:`templates/self-service/restore-stepfunc-perms-policy.json`
  and gives permission to access a specific set of buckets associated with the service account,
  to invoke a specific set of lambda functions, to launch specific AWS resources (Athena, Glue,
  S3 Batch, SNS, CloudWatch), and to pass the panteater-labstorage-s3batch-perms-role to an
  S3 Batch job.

  The second command combines the newly created panteater-labstorage-stepfunc-perms-policy
  with the file in :fname:`templates/self-service/restore-stepfunc-perms-trust.json` which allows a
  step function to use all of the services needed to restore files from S3 Glacier.

**Step Function**
  | *panteater-labstorage-sfn-full-monty step function*

  .. parsed-literal::
     :bluelight:`create-service-account-restore-sfn.py panteater labstorage full-monty`

  This command reads the file :fname:`templates/self-service/sfn-full-monty.json` and creates a step
  function with access to the resources of a specific service account as defined by
  panteater-labstorage-stepfunc-perms-role.  If the command is run again, it will update an
  existing step function, i.e. if changes are made to templates/self-service/sfn-full-monty.json.

User self-restore
-----------------

.. parsed-literal::
   :bluelight:`start-stepfunction-restore.py panteater labstorage full-monty restorelist.txt`

The service account would use this command to begin the restore of files in Glacier to the
Standard tier before recovering the files to local storage.  The :fname:`restorelist.txt` is a text
file with search strings, one per line, of files to restore.

