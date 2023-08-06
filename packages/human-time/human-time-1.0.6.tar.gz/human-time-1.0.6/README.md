# HumanTime

Convert numerical times to their human readable English language equivalent.

Examples: 

`15:00` becomes `"Three o'clock"`

`15:15` becomes `"Quarter past three"`

`15:27` becomes `"Twenty seven minutes past three"`

Distributed on PyPI - https://pypi.org/project/human-time/

## System requirements

Python >= 3.6 is required. The instructions below are focused on creating a Python 3 virtual environment in order to
ringfence the dependencies. 

## Running the application

The package can be installed from source:
```bash
cd human-time
python3 -m venv venv
source venv/bin/activate

python -m pip install -r requirements.txt

python -m pip install -e . --upgrade
```

Alternatively the package can be pulled from PyPi:
```bash
python3 -m pip install human-time
```

The installed application can then be invoked in two says, either as command line tool, which simply performs a single
time conversion, or as a server, which provides a REST API with single endpoint `api/humantime` to convert the time.

`humantime-server` starts by default on port 5000, this can be changed by setting the `HUMANTIME_PORT` environment variable.
```bash
humantime -t 15:00
humantime-server
```
Both methods either return the human time corresponding to the current time, or if the `numeric_time` parameter is
provided, the human time for the given numeric time.

If using `humantime-server`, an OpenAPI user interface is available to test it's endpoint, which can be found at

## Testing

Before testing ensure that the Python virtual environment is set up, and both unit test and application dependencies 
are installed by running `python3 -m pip install -r requirements.txt -r test/requirements.txt`

To run the tests run `python3 -m pytest --cov=src --pyargs test`

## Build and Publish

The package is built, and deployed to PyPi via `twine`, as shown below.

```bash
python3 -m pip install setuptools twine
python3 -m setup sdist
twine upload dist/*
```



