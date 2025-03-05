RCS3 documentation
==================

This repo provides RCS3 documentation that is created with Read The Docs (RTD).

The resulting website served on RTD server as

- https://rcs3.readthedocs.io
- https://rcs3.rtfd.io (shorthand notation)

Building HTML locally for testing
---------------------------------

1. Install prerequisites

   .. code-block:: console

      pip3 install sphinx
      pip3 install sphinx_rtd_theme

2. Check out repo and build

   .. code-block:: console

      git clone git@github.com:RCIC-UCI-Public/rcs3-docs.git
      cd rcs3-docs/docs
      make html

3. Point your local browser to `build/html/index.html`.

Initial Setup Notes
-------------------

This is a summary of steps to use github repo and RTD continuous build
integration.

1. The github repo was imported into the RTD per the tutorial:
   https://docs.readthedocs.io/en/stable/tutorial/

2. Added manual integration of the github repo with Read the Docs (RTD) project
   https://docs.readthedocs.io/en/stable/guides/git-integrations.html

   Note, manual integration involves

   * creating integration in **Console -> Admin -> Integrations**  on RTD console
   * and then adding this info to the github repo in **Settings -> Webhooks**

     Edit:

     - Payload URL (http url from RTD)
     - content type (application/json)
     - choose enable ssl verification

     - choose **let me select individual events** and choose

       - branch or tag creation
       - branch or tag deletion
       - pull requests
       - pushes
       - Active

     Save. After this is set any changes to the github repo files per above
     events will trigger a build automatically.

Useful info links
-----------------

- Useful RTD project links

  Only maintainer/admin can access  these:

  - console https://readthedocs.org/projects/rcs3/
  - build info https://readthedocs.org/projects/rcs3/builds/

  Email about failed builds is sent to the admin/maintainer.

- read the docs build process explanation https://github.com/readthedocs/readthedocs.org/blob/main/docs/user/builds.rst
- continuous documentation deployment https://docs.readthedocs.io/en/latest/integrations.html
- how to create reproducible builds https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html

  It includes some explanation about ``.readthedocs.yaml``, ``conf.py``  and
  ``requirements.txt``.

- getting started with sphinx https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html

File .readthedocs.yaml
----------------------

This file affects how the website docs are built on the RTD server.
It is not  used for local builds.

This file is required as of September 2023 upcoming updates.
Use a template for this file provided in https://blog.readthedocs.com/migrate-configuration-v2/

This file does not need to be modified unless RTD changes its version or
requirements or schema.

File docs/requirements.txt
--------------------------

This file affects how the website docs are built on the RTD server.
It is not  used for local builds.

This file is specified in ``.readthedocs.yaml``. RTD server build fails if the
dependencies are not implicitly specified.

This file does not need to be modified  unless RTD server builds fail and the build logs
outline what is missing. In this case missing dependencies need to be added.

Only the admin/maintainer of the project on RTD can see the log files and get
email about failed builds.

Currently this file contains minimum dependencies for python in order to
build the website on the RTD server.

File docs/source/conf.py
------------------------

Configuration file for sphinx docs builder, used locally and on RTD server.
This file is specified in ``.readthedocs.yaml``.

Minimal changes may be needed :

- Project information info may need to be updated (version, revision).
- name, logo file,  html theme
- 'html_static_path' currently specifies 2 empty directories that can be used
  to hold specific files (css, pdf).

  When anything is added to these directories:

  - docs/source/_static/
  - docs/source/pdfs/

  file ``keepme`` in respective directory can be removed. Currently, ``keepme``
  is a place holder.


Updates
-------

**2023-11-21**

Received email from RTD about a need to update webhook integration:

Previously, manually configured webhooks from integrations did not have a secret attached to them.
In order to improve security, we have deployed an update so that all new integrations will be created
with a secret, and we are deprecating old integrations without a secret. You must migrate your
integration by January 31, 2024, when they will stop working without a secret.

We are contacting you because you have at least one integration that does not have a secret set. These integrations are:

- https://readthedocs.org/dashboard/yaml2rpm/integrations/238314/
- https://readthedocs.org/dashboard/rcs3/integrations/248158/

If you aren't using an integration, you can delete it. Otherwise, we recommend clicking on "Resync webhook"
to generate a new secret, and then update the secret in your provider's settings as well. You can check our
documentation for more information on how to do this.  You can read more information about this in our
blog post: https://blog.readthedocs.com/security-update-on-incoming-webhooks/.


1. Login to RTD console https://readthedocs.org/projects/rcs3/

   In **Admin->Integrations**  click on the existing "GitHub incoming webhook":

   .. image:: images/webhook-1.png
      :width: 450
      :alt: Original webhook

2. The new popup window shows the original  webhook https://readthedocs.org/api/v2/webhook/rcs3/248158/
   errors at the top of the window and the last successful syncs that
   were triggered by the builds:

   .. image:: images/webhook-2.png
      :width: 450
      :alt: Original webhook last activity

   Not shown on the image at the bottom of the window there is "Delete
   webhook" button, click to delete this webhook.

3. Go back to **Admin->Integrations** and click on "Add integration" button

   .. image:: images/webhook-3.png
      :width: 450
      :alt: Add new webhook

4. In a new popup window there is a new webhook URL and now available secret.
   Copy both as they are needed to be added to the git repo:

   .. image:: images/webhook-4.png
      :width: 450
      :alt: New webhook URL and secret

   New webhook https://readthedocs.org/api/v2/webhook/rcs3/255799/

5. Go to the github repo  and in **Settings->Webhooks**, click on the existing webhook
   link. When opened  in the "Settings" tab  change only the Payload URL and Secret to the ones from previous step. 
   The rest of the already configure webhook settings are valid. Click "Update
   webhook" button at the bottom of the page (not shown here)

   .. image:: images/webhook-5.png
      :width: 450
      :alt: Update github webhook URL and secret

   In the "Recent deliveries" tab there will be nothing.
   The first confirmed push delivery of the webhook will be triggered by the
   RTD build process. 

6. Go back to RTD console and trigger a build in **Admin->Builds** 
   via a click on "Build version" button. This should  trigger a build
   and the **Admin->INtegrations** will show a recent activity:

   .. image:: images/webhook-6.png
      :width: 450
      :alt: Integration confirmation

**2023-11-27**

Build are randomly failing without any changes to either git repo or RTD
settings. All failed builds have the signature ( in RTD console builds info):

.. code-block:: console

   git clone --depth 1 https://github.com/RCIC-UCI-Public/rcs3-docs .
   git fetch origin --force --prune --prune-tags --depth 50 refs/heads/master:refs/remotes/origin/master
   fatal: couldn't find remote ref refs/heads/master
   Command time: 0s Return: 128

All successful builds have no **refs/heads/master:refs/remotes/origin/master**
in the git fetch command.

To fix, in Admin->Advanced settings  change the *Default branch*  from
"--------" to "main", and save. The next build is successful

