Bush
====

Bush is wrapper AWS cli, eash to use.

Available Services
==================

1. ec2

Usage
=====

EC2
---
Listing all EC2 instances:

.. code-block:: sh

  $ bush ec2 ls

You can choose columns:

.. code-block:: sh

  # default columns are
  # * instance_id
  # * instance_type
  # * tag_Name
  # * public_ip_address
  # * private_ip_address
  # * state
  # optional columns are
  # * availability_zone
  # * image_id
  # * key_name
  # * launch_time
  # * private_dns_name
  # * public_dns_name
  # * security_groups
  $ bush ec2 ls -c tag_Name,availability_zone,launch_time

Filtering instances by Name tags. You can use wild card:

.. code-block:: sh

  $ bush ec2 ls --name="your-product*,your-service*"

Filtering instances by instance ids:

.. code-block:: sh

  $ bush ec2 ls --id=i-xxxx,i-yyyy,i-zzzz

Filtering instances by a specific filter name:

.. code-block:: sh

  $ bush ec2 ls --filter_name=instance-state-name --filter_values=stopped,pending

Listing all EC2 images:

.. code-block:: sh

  $ bush ec2 images
