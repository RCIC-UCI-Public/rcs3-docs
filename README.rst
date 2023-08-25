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

This file is specified in ``..readthedocs.yaml``. RTD server build fails if the
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

Minimal changes may be needed :

- Project information info may need to be updated (version, revision).
- name, logo file,  html theme
- 'html_static_path' currently specifies 2 empty directories that can be used
  to hold specific files (css, pdf).

  When anything is added to these directories:

  - docs/source/_static/
  - docs/source/pdfs/

  file ``keepme`` in respective directory can be removed. Currently, keep me
  is a place holder.
