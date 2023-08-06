# CRISPRbuilder_TB
------------------

>This **README.md** gives you the gist of the CRISPRbuilder_TB package. Please refer to **crisprbuilder_tb.ipynb** included in the package and readable on [GitHub](https://github.com/stephane-robin/crisprbuilder_tb/tree/master/crisprbuilder_tb/doc) for more detailed explanation.    


## Purpose of this package
--------------------------

>Collect and annotate Mycobacterium tuberculosis whole genome sequencing data for CRISPR investigation.    


## Requirements
---------------

>CRISPRbuilder_TB needs the following dependencies to work:

* python >= "3.6"
* xlrd >= "1.2.0"
* xmltodict >= "0.12.0"
* biopython >= "1.77"
* parallel-fastq-dump >= "0.6.5"
* blast >= "2.10.1"
* blastn >= "2.7.1"

>These different versions are automatically downloaded when installing the CRISPRbuilder_TB package.    


## Installation
---------------

>Make sure you're using a version of Python higher or equal to 3.6.
>Install the package by writing in the command prompt: `pip install crisprbuilder_tb`.    


## How to use this package
--------------------------

>The most often common instruction for this package is: `python -m crisprbuilder_tb --collect {SRA_reference}`.

See the documentation **criprbuilder-tb.ipynb** for a comprehensive explanation.    


## History
----------

First version of this package, which is 1.0.0 was published on August 2020.
