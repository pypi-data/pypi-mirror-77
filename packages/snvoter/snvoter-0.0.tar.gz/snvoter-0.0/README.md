SNVoter
=======

A top up tool to enhance SNV calling from Nanopore sequencing data.

## Installation

Using pypi repository

```
pip install snvoter
```

Using conda

```
TBD
```

From source

```
git clone https://github.com/vahidAK/SNVoter.git
cd SNVoter
./snvoter.py
```

## Creation of a dedicated conda environment

SNVoter uses several fixed versions of its dependencies. Users are encouraged
to use a conda or similar environment to isolate the packages from their
default python instance. An environment file is available in the GitHub
repository.

```
git clone https://github.com/vahidAK/SNVoter.git
conda env create -f SNVoter/env/environment.yaml
conda activate snvoter
```
