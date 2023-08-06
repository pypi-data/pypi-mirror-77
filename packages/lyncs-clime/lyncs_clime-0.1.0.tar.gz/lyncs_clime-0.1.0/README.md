# A Python interface to c-lime for Lyncs

[![python](https://img.shields.io/pypi/pyversions/lyncs_clime.svg?logo=python&logoColor=white)](https://pypi.org/project/lyncs_clime/)
[![pypi](https://img.shields.io/pypi/v/lyncs_clime.svg?logo=python&logoColor=white)](https://pypi.org/project/lyncs_clime/)
[![license](https://img.shields.io/github/license/Lyncs-API/lyncs.clime?logo=github&logoColor=white)](https://github.com/Lyncs-API/lyncs.clime/blob/master/LICENSE)
[![build & test](https://img.shields.io/github/workflow/status/Lyncs-API/lyncs.clime/build%20&%20test?logo=github&logoColor=white)](https://github.com/Lyncs-API/lyncs.clime/actions)
[![codecov](https://img.shields.io/codecov/c/github/Lyncs-API/lyncs.clime?logo=codecov&logoColor=white)](https://codecov.io/gh/Lyncs-API/lyncs.clime)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=codefactor&logoColor=white)](https://github.com/ambv/black)

Lyncs.clime is a faithful Python interface to c-lime.
[c-lime] is a C-API for creating, reading, writing, and manipulating LIME files
and offers a small set of utilities for examining, packing and unpacking LIME files.

LIME (which stands for Lattice QCD Interchange Message Encapsulation or more generally,
Large Internet Message Encapsulation) is a simple packaging scheme for combining records
containing ASCII and/or binary data. Its ancestors are the Unix cpio and tar formats and
the Microsoft Corporation DIME (Direct Internet Message Encapsulation) format.

It is simpler and allows record sizes up to $2^{63}$ bytes, making chunking unnecessary
for the foreseeable future. Unlike tar and cpio, the records are not associated with Unix files.
They are identified only by a record-type (LIME type) character string, analogous to the familiar
MIME application type.

[c-lime]: https://github.com/usqcd-software/c-lime

## Installation

The package can be installed via `pip`:

```
pip install [--user] lyncs_clime
```

## Documentation

The following classes are available in lyncs_clime: Reader, ...


## Contributing

When contributing to the package, clone the source from [github](https://github.com/Lyncs-API/lyncs.clime):

```
git clone https://github.com/Lyncs-API/lyncs.clime
cd lyncs.clime
```

install the package in development mode:

```
pip install -e .[all]
```

and run the test-suite for checking the correctness of the installation:

```
pytest -v
```

If everything goes well, you should see all the tests passed and obtain a coverage report.

A main implementation requirement is an **high code-coverage**.
If you are going to implement something new, please, also add the respective
test files or functions in the `test/` directory.

Another implementation requirement is to **format the code** via [black](https://github.com/ambv/black)
and to use [pylint](https://github.com/PyCQA/pylint) for improving the code standard.

These packages can be installed via pip:

```
pip install black pylint
```

Before any commit, run black from the source directory:

```
black .
```

When you are done with the implementation, try to resolve as many comments/warnings/errors
as possible brought up by `pylint`:

```
pylint lyncs_clime
```

**NOTE:** pylint and black are incompatible in few formatting assumptions. Please, ignore
the comments C0303 and C0330 of pylint. If they show up in the files you have edited/added,
please, add the following line after the documentation string at the beginning of the respective files:

```
# pylint: disable=C0303,C0330
```

