
.. warning::
   This project is under active development.
   The documentaion pages are currently a template


RCS3 Documentation
==================

**Rclone to S3 for large backup** (:term:`RCS3`) 
is developed by the `Research Cyberinfrastructure Center <https:/rcic.uci.edu>`_ (:term:`RCIC`)
at the University of California, Irvine. 

This is a set of programs, scripts, templates, policies, and documentation for UCI's use of ``rclone``  
to backup multi-Terabyte to Petabyte-scale storage servers to Amazon S3 Glacier Flexible Retrieval.  

Our primary target is  the in-faculty-lab storage server that is often run by a graduate student 
or other part-time administrator (sysadmin).
In the UCI environment, central IT does not have system-level privileges on the lab servers.
Central IT (cloud admin) provisions per-server backup buckets, applies appropriate permissions and policies, 
and provides initial guidance on setting up daily backups.   
The lab sysadmin configures their system for backup using buckets and credentials created by the cloud 
admins. Lab sysadmins can initiate restores to that backup bucket, but do not have the authority to permanently 
delete backups. Intentional adminstrative isolation means that complete data loss requires two 
different sets of elevated privilege credentials - 
one to delete primary data on the server, and a different set to permanently delete data on the backup. 
Object versioning in S3 
with specific retention policies provide a delay (e.g., 90 days) from delete/overwrite to permanent deletion. This
essentially provides "snapshots" so that restores can be accomplished from any recorded state during the 
retention period.

RCS3 is command-line driven and demands a small number of common software prerequisites: Rclone, Python3, selected Python3 packages (e.g., boto3 tools, PyYaml, multiprocessing) installed on the to-be-backed-up server. We've successfully used
these scripts and policies on Linux, Windows, and Intel-based Synology NAS. 

We're providing this information AS IS with no guarantees. Our hope is that others (especially other academic 
institutions) can use our model as a starting point to create cost-effective and robust backups for their research 
communities. 

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
