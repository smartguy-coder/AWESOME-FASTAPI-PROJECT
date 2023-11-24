# Structure of auth files:
In global file:
* `models.py` - for setting up slq tables
* `dao.py` - for executing queries to database
In auth:
* `auth_lib.py` - encoding/decoding tokens, user verification
* `dependencies.py - `