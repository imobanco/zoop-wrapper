# Documentation sphinx
this folder is used to maintain and generate the sphinx documentation

## Steps

### Start
to initiate the sphinx project use the command 
```shell script
sphinx-quickstart
```

It will generate some files in the current dir. In `conf.py` we add some custom configurations to have
autodocs, napoleon, read the docs theme and so on. 

### Autodocs
to generate the docs file from the code docstrings we use the command from the root folder of the package
```shell script
sphinx-apidoc --force --output-dir docs/source .
```

After we make modifications to the `rst`'s files.

### Build
the last step is to build the documentation to static html. We do it so running this command from the root folder of the package
```shell script
sphinx-build docs/source/ docs/
```