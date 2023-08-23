.. _client:

Client tasks
=============

Can upload/download files. Can Delete Files (but not specific versions)


Restore from AWS
-----------------

User requests restore of files from AWS Glacier

1. Start EC2 instance in the free tier (background process to send notification every 24 hours that instance is running)

2. Git pull to retrieve code.

3. Execute:

   .. code-block:: console

      ./scripts/bucket-halt-changes <user> <host>
      ./scripts/athena-setup.py <user> <host>
      ./scripts/athena-query-from-file.py <user> <host> <file with list of files to restore>
      ./scripts/athena-query-job-status.py <user> <host> <output from previous command>
	
   Loop here until successful or errors (manual cleanup after investigation)

   If errors, halt and send notification to rcic-admin

   .. code-block:: console

      ./scripts/athena-teardown.py <user> <host>
      ./scripts/glacier-restore-from-file.py <user> <host> <output from athena-query-job-status.py>
      ./scripts/glacier-query-job-status.py <user> <host> <output from previous command>

   loop here until successful or errors (manual cleanup after investigation)

If errors, halt and send notification to rcic-admin

Send notification to user and delete EC2 instance

Retrieve files
---------------

| User invokes rclone to retrieve files
| This occurs on user's machine.
| After user confirms that they recovered all files

.. code-block:: console

   ./scripts/bucket-resume-changes.py <user> <host>
