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