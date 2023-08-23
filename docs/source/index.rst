
.. warning::
   This project is under active development.
   The documentaion pages are currently a template


RCS3 Documentation
==================

**Rclone to S3 for large backup (:term:`RCS3`)** 
was developed at the Research Cyberinfrastructure Center (:term:`RCIC`)
at the University of California, Irvine.

This is a set of scripts and documentation for how UCI uses ``rclone`` 
to backup larger servers (over 100TB) to Amazon S3 Glacier Flexible Retrieval.

In particular, :term:`UCI` plans to use these to backup large data servers in labs.

This documentation describes our setup to effectively use :term:`AWS` and :term:`Rclone`
technologies.

.. toctree::
   :glob:
   :maxdepth: 1
   :caption: About RCS3

   about/preface
   about/architecture

.. toctree::
   :maxdepth: 1
   :caption: Installation

   installation/requirements
   installation/quickstart

.. toctree::
   :maxdepth: 1
   :caption: Admin

   admin/central
   admin/deletion

.. toctree::
   :maxdepth: 1
   :caption: Client

   client/usage

.. toctree::
   :maxdepth: 1
   :caption: Reference

   references/glossary
   references/changelog
