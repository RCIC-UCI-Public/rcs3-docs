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

- generic IAM roles and policies
	- lambda-generic-createAthenaQueries-policy
	- lambda-generic-createS3BatchInput-policy
	- lambda-generic-pollCreateJobStatus-policy
	- lambda-generic-createAthenaQueries-role
		- requires policy: lambda-generic-createAthenaQueries-policy
	- lambda-generic-createS3BatchInput-role
		- requires policy: lambda-generic-createS3BatchInput-policy
	- lambda-generic-pollCreateJobStatus-role
		- requires policy: lambda-generic-pollCreateJobStatus-policy
		
- generic lambdas
	- createAthenaQueries
		- requires role: lambda-generic-createAthenaQueries-role
		- requires trust: createAthenaQueries-trust.json
	- createS3BatchInput
		- requires role: lambda-generic-createS3BatchInput-role
		- requires trust: createS3BatchInput-trust.json
	- pollCreateJobStatus
		- requires role: lambda-generic-pollCreateJobStatus-role
		- requires trust: pollCreateJobStatus-trust.json
				
- generic CloudWatch log groups
	- /aws/lambda/createAthenaQueries
	- /aws/lambda/S3BatchInput
	- /aws/lambda/pollCreateJobStatus

User Specific Settings
----------------------

		- Athena workgroup
		- IAM roles and policies
			- restore-s3batch-perms-policy
			- restore-stepfunc-perms-policy
			- restore-s3batch-perms-role
				- requires policy: restore-s3batch-perms-policy
				- requires trust
			- restore-stepfunc-perms-role
				- requires policy: restore-stepfunc-perms-policy
				- requires trust:
		- step function
			- sfn-full-monty
				- requires role: restore-stepfunc-perms-role
				- passes restore-s3batch-perms-role to S3 Batch job

User self-restore
-----------------

	- invoke step-function

