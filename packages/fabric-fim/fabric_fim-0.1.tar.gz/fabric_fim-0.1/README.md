# Information Model
FABRIC Information Model library, containing class definitions and methods for operating
on different types of information model representations (sliver and slice)

## Development environment

The recommended way is to set up your development environment using virtualenv after checking
out the code:
```bash
$ git clone git@github.com:fabric-testbed/InformationModel.git
$ cd InformationModel
$ mkvirtualenv -r requirements.txt infomodel
$ workon infomodel
(infomodel) $

```

## Installation

Multiple installation options possible. For CF development the recommended method is to
install from GitHub MASTER branch:
```bash
$ pip install git+https://github.com/fabric-testbed/InformationModel.git
```

For developing and testing the FIM code itself use editable install (from top-level directory)
```bash
(infomodel) $ pip install -e .
```

For inclusion in tools, etc, use PyPi
```bash
$ pip install fim
```

## Code structure and imports

Base classes are under `fim.graph` and `fim.slivers`. 