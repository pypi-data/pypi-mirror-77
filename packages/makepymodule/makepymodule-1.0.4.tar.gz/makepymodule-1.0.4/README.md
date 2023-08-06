# makepymodule
Generates the project structure for a pip installable python module

## Installation
```bash
$ pip install makepymodule
```

## Usage
To create a new project, simply go to the location you would like to scaffold the project structure and run the following command
```bash
$ makepymodule project_name
```

A directory structure as follows will be generated
```
- project_name
  |- src
     |- project_name
        |- __init__.py
  |- setup.py
```
