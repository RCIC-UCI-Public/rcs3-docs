RCS3 documentation 
==================

This repo provides RCS3 documentation that is
created with Read The Docs.

The resulting website will be https://rcs3.readthedocs.io

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


File .readthedocs.yaml
----------------------

2023-08-23

Updated per https://blog.readthedocs.com/migrate-configuration-v2/
