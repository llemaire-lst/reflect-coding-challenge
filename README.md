## About The Project

This project is a coding challenge which goal is to build an ingestion pipeline over the Lucca REST API.
More details to found in this [file](reflect_coding_challenge.md).

The project is build over the [dlt](https://dlthub.com/) python library.

## Getting Started

You have two ways of getting the pipeline running on your setup.
- Run in local with your own python environment 
- Run in a container with docker compose

### Configure your credentials 

Credentials (the Lucca API key) should be filled under the .dlt/secrets.toml file with the exact naming below
```
[sources.rest_api_lucca_pipeline]
lucca_token = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx"
```

### Run Locally with Python

The pipeline have been developped with python 3.10.
You may install the dependency through the requirement file.
```
pip install -r requirements.txt
```

### Run in a container 

If you have docker installed you may use docker compose to get the pipeline running with the following command
```
docker compose up
```

## Usage

To launch the pipeline you can just run the [rest_api_lucca_pipeline](rest_api_lucca_pipeline.py) python script.
```
python rest_api_lucca_pipeline.py
```

The data are then extracted from the API and loaded into a duckdb database (loacated in the data folder) that you can query at your will.
More info [here](https://duckdb.org/docs/stable/clients/cli/overview.html#installation) if you want to install the duckdb CLI.

You will find 3 tables : users, department, work_contracts
