
Upload to Nexus, Upload files to hooks, Modify version number, Sync to GitLab type repository

Installation
============
You can download and install the latest version of this software from the Python package index (PyPI) as follows::

    pip install --upgrade artify

Usage
=====
    python -m artify --help

    python -m artify --command <command> [Options]
or
    python -m artify -c <command> [Options]


Params

    command     nexus, syncrepo, deploy, deltav

Upload to Nexus
===============

    python -m artify -c nexus -f <format> -n <artifact_name> -h <nexus_repository_base_url>

Params
    format      Nexus upload format. Types supported: raw, npm, maven

Deploy App using custom AWX host
================================

    python -m artify -c deploy -f <manifest_file.yml> -h <awx_host>

Change Package version
======================

Artify uses semantic version 2.0.

python -m artify -c deltav -t patch -a npm

-a, --archtype    npm, gradle, flutter

-t, --type        major, minor, patch