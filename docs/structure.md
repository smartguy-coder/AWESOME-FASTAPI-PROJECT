# Files in root:

* `models.py` - for setting up slq tables
* `dao.py` - for executing queries to database
* `database.py` - for connection to database
* `Makefile` - for making easy to set up the project
* `mkdocs.yml` - for setting up docs and docs files
* `poetry.lock` - for storing encoded data about installed packages
* `poetry.toml` - for settings of poetry
* `pyproject.toml` - for storing list of packages installed

# Files in app:

## In auth:

<h5>Overall this file is for passwords and authorisation</h5>

* `auth_lib.py` - for encoding/decoding tokens, user verification
* `dependencies.py` - for checking user authentication, getting user id and token
* `otp.py` - for encoding uuid, creating qr and verification of otp password
* `schemas.py` - for storing structure of user (and other) details related to database

## In templates:

<h5>Overall this file is for storing web pages</h5>

## Files in docs:

<h5>Overall this file is for documentation that you are reading right now</h5>

* `img` - for storing images needed for docs
* Files with `.md` extension - for docs
