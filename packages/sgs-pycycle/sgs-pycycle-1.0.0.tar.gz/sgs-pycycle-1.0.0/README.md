# sgs-pycycle

sgs-pycycle is a pure Python 3 client and object-mapper for Oslo Bysykkel.

It requires no additional libraries.


## General

The main reason for writing this library was a simple academic task.

Since the name `pycycle` was already taken, I decided to namespace it.

I hope that somebody will find it useful.


## Requirements

- Python >=3.6 with corresponding `setuptools`


## Installation

If one wants to install the package in a convenient way as an unprivileged
user the easiest way is to use `virtualenv` that is part of Python 3.

   ```bash
   python -m venv venvSGSPycycle
   source venvSGSPycycle/bin/activate
   ```

or if using MS Windows

   ```bash
   C:\Users\'Username'\path\to\venvSGSPycycle\Scripts\activate.bat
   ```

That will install and load the virtual environment
Now one can choose one of the methods described bellow.


### pip (pypi)

The easiest way is to install the package directly from pypi.org

   ```bash
   pip install sgs-pycycle
   ```


### Manual

   ```bash
   git clone https://github.com/sgs-test/sgs-pycycle.git
   ```

One can simply install in a virtual-environment or as a privileged user by:

   ```bash
   cd sgs-pycycle
   python setup.py install
   ```

or one can add a symlink or copy `sgs-pycycle/sgs_pycycle` into any directory
that is included in the PYTHONPATH environmental variable or create own
directory.

   ```bash
   mkdir mypythonpathdir
   export PYTHONPATH=/full/path/to/mypythonpathdir
   cp -R sgs-pycycle/sgs_pycycle /full/path/to/mypythonpathdir/
   ```

This latest method also eliminates the need for `setuptools`, but will not add
the dedicated executable `sgs_pycycle`. Still the CLI interface can be accessed
as shown bellow.

Check if everything works by typing:

   ```bash
   python -m sgs_pycycle -h
   ```


## Overview and technical design

The main goals when considering the technical design were:

### Portability

Although there are several Python libraries that simplify the HTTP request as well
as handling the responses like `requests` and `pydantic` for object mapping,
I decided to use only the standard Python modules to make installation and
usage as simple as possible.


### Simplicity

There are many possible improvements (some of them listed bellow), but I made a
conscious decision to only stick with the provided task.


### Object-oriented design and extensibility

Making HTTP requests and processing data is a relatively simple task.
I wanted to provide a small set of objects (Station and StationCollection) in
order to make the use of this client library easier to extend.
Instead of using the provided CLI interface, it is now quite easy to use the
client library in f.i. web application or GUI application.
In addition using a simple object mapper is more elegant and intuitive than
simply manipulating JSON structures.


## Examples

### CLI

The CLI interface can be accessed in two ways.

   ```bash
   python -m sgs_pycycle -h
   ```

or if sgs-pycycle was installed using `setuptools`, there will also be a
binary called `sgs_pycycle`. Hence

   ```bash
   sgs_pycycle -h
   ```

will yield the same result and display a summery of all available CLI options.

   ```bash
   python -m sgs_pycycle -l
   sgs_pycycle -l
   ```

will display all stations with id, name, number of docks available, number
of bikes available.

   ```bash
   python -m sgs_pycycle -l -k name
   sgs_pycycle -l -k name
   ```

will produce the same content, only order the stations by name.

All station attributes can be used for sorting, given that string attributes
will be sorted as strings (f.i. '98' > '1654').

   ```bash
   python -m sgs_pycycle -l -c user-testapp
   sgs_pycycle -l -c user-testapp
   ```

will call the API using 'user-testapp' as Client-Identifier.


### Using the library directly

Using the library directly provides more possibilities and makes it possible
to embed the client into a web-application or even a GUI application.

   ```python
   import sgs_pycycle

   # Auto discovery URL and identity
   A_D_URL = 'https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json'
   CLIENT_IDENTITY = 'user-testapp'

   # create a Client object
   client = sgs_pycycle.Client(A_D_URL, CLIENT_IDENTITY)

   # fetch the entire collection
   try:
       collection = client.get_station_collection()
   except sgs_pycycle.ClientConnectionError as e:
       # ... unable to connect routines and messages
       pass
   len(collection)  # amount of stations

   # print the last_reported value for each station
   for station in collection:
       print(f'{station.name} - {station.last_reported}')

   # sort the stations by name
   collection.sort_by_key('name')
   for station in collection:
       # prints id, name, number of docks available, number of bikes available
       print(station)
   ```


## Todo

Incomplete list of possible future improvements:

- unit tests

- caching by using the `last_updated` and `last_reported` attributes for better performance

- extended StationCollection API, fetching a single Station, advanced sorting..

- translation / locale support

- API documentation with Sphinx

- Better error reporting and sanity checking

- Formatting output for CLI (header, even spacing, etc...)

- More CLI parameters (socket timeout, SSL context, etc...)


## Author

Simeon Simeonov - sgs @ Freenode


## [License](https://github.com/sgs-test/sgs-pycycle/blob/master/LICENSE)

Copyright (c) 2020, Simeon Simeonov
All rights reserved.

[Licensed](https://github.com/sgs-test/sgs-pycycle/blob/master/LICENSE) under the BSD 2-clause.
SPDX-License-Identifier: BSD-2-Clause-FreeBSD
