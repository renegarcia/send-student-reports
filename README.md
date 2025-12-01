# Student email sender

This program sends reports of student marks by email. 

You need a list of data in csv forma and a template file with the contents of the email.  Sample template and data files are provided under the `data` folder.

## Before you begin

You need an outlook email and a valid app script registered with Microsoft Entry for this program to work. 

1. Register with Microsoft Entra as documented [here](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app) (tested with option _Personal Microsoft accounts only_ other options may work as well)
2. On the side panel, under _API permissions_ add __Mail.Send__

### Optional

Once registration is done, record your Application ID and register as the environment variable `CLIENT_ID`.

```bash
export CLIENT_ID="your client id"
```

## Installation

First, create a virtual environment:

```bash
python -m venv .venv
cd .venv
source bin/activate.bash
```

Once your virtualenv is loaded, install Microsoft's authentication library `msal` from pip:

```bash
python -m pip install msal 
```

## Ussage

First, load the virtualenv previousley intalled. 

With a terminal open on the main directory, suppose your data is stored on `data/marks.csv` and the template is `data/template.html`. If you exported your application id as `CLIENT_ID` send your reports as follows:

```bash
python scripts/main.py --csv data/marks.csv --template data/template.html
```

If you stored your id elsewhere, 

```bash
CLIENT_ID="your id" python scripts/main.py --csv data/marks.csv --template data/template.html
```


## Template format

Any valid format that python's native [format language](https://docs.python.org/3/library/string.html#formatstrings) supports. 

