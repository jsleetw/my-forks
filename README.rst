my-forks
========
simplly use (fab update) to sync your github forks repos with source repos

Require
-------
    * fabric : http://fabfile.org/
    * github2 : http://packages.python.org/github2/
    * easy_install :

::

    easy_install fabric github2

configuration
-------------
    * open fabfile.py edit ur code_dir
    * will asking ur user name in runtime
    * .user_name : auto save ur username in this file #do not update to git
    * .api_token : if you need update ur private repo.
                   put ur api_token in this file.
                   get ur api_token from https://github.com/account/admin

Usage
-----

::

    fab update

ChangeLog
=========

v1.0 2011-12-20
---------------
    * support private api
    * auto save username
