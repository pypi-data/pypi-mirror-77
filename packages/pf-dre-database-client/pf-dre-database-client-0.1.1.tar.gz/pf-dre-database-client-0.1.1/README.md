# Meter Management System Client
The python implementation of the pf-dre-database repo provides a client
for all Data interactions required with the Meter Management System:
- Relational tables (Read Only)
- Timescale DB (Read/Write - No insertion or deletion)
    - JSON Schema
    - Narrow Data Format Schema

This python implementation is to be built and deployed to PyPI for use
across all python subsystems of the Demand Response Engine.

## Input Data Format
When issuing calls to the MMS which require a time series based DataFrame to be
passed the format of the schema should be followed with the following general 
rules. 
- Timestamps are to be generated in string format following the ISO 8601 
standard and to follow simple conventions should be kept in UTC format.
- Any columns within the data structure which are a JSON datatype are to be 
created in serialized string format, not as a pure python dictionary.
    ```python
    # Correct Format
    json_col = json.dumps({'A': 'Dictionary', 'B': 'to', 'C': 'Send'})
    # Incorrect Format
    json_col = {'A': 'Dictionary', 'B': 'to', 'C': 'Send'}
    ```
###### **Example Data Frame for a narrow column format schema**

|      measurement_date | device_id | device_metric_type_id |   value    |
|----------------------:|----------:|----------------------:|-----------:|
|2020-01-01T12:00:00.000|    1      |          P            | 1.0        |
|2020-01-01T12:01:00.000|    1      |          P            | 2.0        |
|2020-01-01T12:00:00.000|    1      |          Q            | -1.0       |
|2020-01-01T12:01:00.000|    1      |          Q            | -2.0       |
|2020-01-01T12:00:00.000|    2      |          P            | 10.0       |
|2020-01-01T12:01:00.000|    2      |          P            | 20.0       |
|2020-01-01T12:00:00.000|    2      |          Q            | -10.0      |
|2020-01-01T12:01:00.000|    2      |          Q            | -20.0      |
| object (str)          | int64     | object (str)          | float64    |

###### **Example Data Frame for a JSON schema**

|      measurement_date | device_id | metrics                     |
|----------------------:|----------:|----------------------------:|
|2020-01-01T12:00:00.000|    1      | {"P": 1.0, "Q": -1.0}       |
|2020-01-01T12:00:00.000|    2      | {"P": 2.0, "Q": -2.0}       |
|2020-01-01T12:01:00.000|    1      | {"P": 10.0, "Q": -10.0}     |
|2020-01-01T12:01:00.000|    2      | {"P": 20.0, "Q": -20.0}     |
| object (str)          | int64     | object (str)                |

## Standardized Output DataFrame Format
When issuing calls to the MMS which return a time series DataFrame, the client, 
regardless of schema will be constructed to return in a standardized format.
This makes the reading and manipulation of data consistent.

| device_id | device_metric_type_id |      measurement_date |   value    |
|----------:|----------------------:|----------------------:|-----------:|
|    1      |          P            |2020-01-01T12:00:00.000| 1001.0     |
|           |                       |2020-01-01T12:01:00.000| 1012.0     |
|           |          Q            |2020-01-01T12:00:00.000| 12.132     |
|           |                       |2020-01-01T12:01:00.000| -2.132     |
|    2      |          P            |2020-01-01T12:00:00.000| 2001.0     |
|           |                       |2020-01-01T12:01:00.000| 2012.0     |
|           |          Q            |2020-01-01T12:00:00.000| 22.132     |
|           |                       |2020-01-01T12:01:00.000| -3.132     |
| int64     | object (str)          | object (str)          | float64    |

The client also has the option of returing the data frame results in a raw, 
un-standardised format. In this case, the dataframe will be returned in the 
format of the underlying database schema without any alteration.

### Prerequisites
- Python 3.7.0+

### Setup
The following environment variables are required in order to make use
of the client.

- `PGDATABASE`: The name of the MMS Database instance.
- `PGUSER`: MMS Database user.
- `PGPASSWORD`: MMS Database password.
- `PGHOST`: MMS Database host.
- `PGPORT`: MMS Database port (read/write permissions required).

### Development

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
