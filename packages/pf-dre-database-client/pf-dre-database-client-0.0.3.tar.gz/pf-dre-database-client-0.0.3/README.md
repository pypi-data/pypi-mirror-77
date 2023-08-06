# Meter Management System Client
The python implementation of the pf-dre-database repo provides a client
for all Data interactions required with the Meter Management System:
- Relational tables (Read Only)
- Timescale DB (Read/Write - No insertion or deletion)
    - JSON Schema
    - Narrow Data Format Schema

This python implementation is to be built and deployed to PyPI for use
across all python subsystems of the Demand Response Engine.


### Prerequisites
- Python 3.7.0+

### Set-up

1. Clone the repo
2. Create a python virtual environment:
    - Windows: `C:\>   python -m venv .\venv` (Python must be in PATH variable)
    - Linux: `$ python3 -m venv ./venv`
3. Activate the virtual environment:
    - Windows: `C:\>   .\venv\Scripts\activate.bat` (Python must be in PATH variable)
    - Linux: `$ ./venv/bin/activate`
4. Install development specific requirements
    `(venv) pip install --upgrade twine setuptools wheel`
5. Install requirements:
    `(venv) pip install -r requirements.txt`


### Tests

Tests should be run locally. Access must be granted to the test
database and .env.template should be renamed to .env and configured with
appropriate parameters.

To run tests:
 `(venv) python -m tests`


### Deployment

#### Test PyPI
    `python -m twine upload --repository pf-dre-database-test --config-file .pypirc dist/*`

#### PyPI
    `python -m twine upload --repository pf-dre-database --config-file .pypirc dist/*`
