.. _work-database:

Working with your application's database in web applications
====================================================================


Introduction
------------

Database service for Divio applications are provided by the cloud providers (AWS, AZ) entirely separate from the 
application. The available database services depend on the Divio region your application uses. Most applications use 
Amazon RDS PostgreSQL.


MySQL on AWS
------------

When your application is using MySQL on AWS, please also consult the available `best practices for "Scale-blocking 
operations" <https://aws.amazon.com/blogs/database/best-practices-for-working-with-amazon-aurora-serverless/>`_ for the 
service.
