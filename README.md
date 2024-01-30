# attackflow_09

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)

## Setup

### Dependencies (Prerequisites)

-   Python 3

#### VSCode

A configuration is provided in the repository. Make sure to also set the correct Python interpret using the shortcut `Ctrl+Shift+P`, finding the `Python: Select Interpreter` option, and choosing the `venv` option. An extension is also available for [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode).

### Installation

_Make sure to run the following commands in the project root directory._

#### Create virtual environment & install packages

To create a new virtual environment in a directory called "venv", run:

```
python -m venv venv
```

A virtual environment acts as a self-contained Python installation, which will ensure our dependencies are kept separate to the rest of your system.

To activate this virtual environment:

```
source venv/bin/activate
```

**_You will need to run this command every time you open a new shell and want to work on the project!_**

Install required packages:

```
pip install -r requirements.txt
pre-commit install
```

#### Pre-commit checks

To improve code quality, pre-commit checks should run when `git commit` is executed. If this doesn't occur, you may need to run `pre-commit install`.
If there are issues with your changes, you will be notified about them when attempting to commit. If you are unsure whether you committed your changes,
use `git status` to see if there are unstaged changes from running the checks.
**_You will not be able to successfully commit until the issues are fixed!_**

To manually trigger a check, use `pre-commit run --all-files`.

### Usage

1. Enter virtual environment:

```
source venv/bin/activate
```

2. Start Django server:

```
python manage.py migrate
python manage.py runserver
```

### Tips

#### Creating an administrator account

To access the admin panel, you'll need to create a 'superuser' account to log in with. Use these commands in the terminal (in the folder where `manage.py` is) and follow the prompts, then start the Django server and navigate to [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to login.

```
python manage.py migrate
python manage.py createsuperuser
```

#### Inspecting database content

When SQLite is being used, downloading the [sqlitebrowser](https://sqlitebrowser.org/) tool remains the easiest way to inspect the contents of the database.

Database contents can also be viewed using the Django Shell. To view the Document database and the path of the files, run:

```
python manage.py shell
from reports.models import Report
all_documents = Report.objects.all()
for document in all_documents:
    print(document)
```

#### Making changes to models

If you are making changes to models (e.g., adding new models or changing fields) run commands in terminal:

```
python manage.py makemigrations
python manage.py migrate
```

Migrations are responsible for setting up the database structures (tables, columns, rows etc).
