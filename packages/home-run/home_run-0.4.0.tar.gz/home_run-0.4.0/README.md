# DLHub home_run

[![Build Status](https://travis-ci.org/DLHub-Argonne/home_run.svg?branch=master)](https://travis-ci.org/DLHub-Argonne/home_run)
[![Coverage Status](https://coveralls.io/repos/github/DLHub-Argonne/home_run/badge.svg?branch=master)](https://coveralls.io/github/DLHub-Argonne/home_run?branch=master)
[![PyPI version](https://badge.fury.io/py/home-run.svg)](https://badge.fury.io/py/home-run)

`home_run` is a tool used by [the Data and Learning Hub for Science](https://www.dlhub.org) internally to turn a bunch of files and a recipe into an functional Python object. 

## Installation

`home_run` is on PyPi. Install it by calling

```bash
pip install home_run
```

`home_run` is designed to be as light-weight as possible, and has only `requests` as a dependency. 

## Technical Details

The key ingredients for using `home_run` are files describing a function that will be served by DLHub.
These include a metadata file describing the servable (see 
[`dlhub_sdk`](http://github.com/dlhub-argonne/dlhub_sdk) for tools for creating these files, 
and [`dlhub_schemas`](http://github.com/dlhub-argonne/dlhub_schemas) for the schemas), and
the actual files that make up the servable (e.g., a Keras hdf5 file).

Each particular type of servable has its own recipe for going from these files to a Python object.
All recipes are a subclass of `BaseServable`, which provides the general framework for defining a servable object.
Each subclass has a matching `BaseMetadataModel` class in `dlhub_sdk`.
For example, the type of servable that can be described by the `PythonStaticMethodModel` can be run by the `PythonStaticMethodServable`.
   
## Project Support
This material is based upon work supported by Laboratory Directed Research and Development (LDRD) funding from Argonne National Laboratory, provided by the Director, Office of Science, of the U.S. Department of Energy under Contract No. DE-AC02-06CH11357.
