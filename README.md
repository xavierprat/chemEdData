# chemEdData
# An open initiative for data-oriented learning activities in Chemistry.

How to use this tool
====================

Installation
============

Unpack the whole ZIP file (or use git) in your server directory.

Set the root directory
----------------------

Allow python and php in your server
-----------------------------------
Add 
~~~
<Directory /var/www/yourWebdirectory/api >
	Options FollowSymLinks
	Options -Indexes
	AllowOverride None
	Require all granted
	Options +ExecCGI
	AddHandler cgi-script .py
</Directory>
~~~
and restart your apache server.


Update libraries
================


Add/remove/modify substances in collections
===========================================

No database: JSON file
----------------------

Browsing: Tables.php
--------------------
The tables.php

   python makeTables.py

Make a property searchable: API
===============================

Modify the index.py

