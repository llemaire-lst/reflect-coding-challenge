from typing import Any, Optional

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig

from utils.custom_auth import CustomAuth
from utils.custom_paginator import CustomOffsetPaginator, PageNumberLimitPaginator


@dlt.source(name="lucca_v3", max_table_nesting=0)
def lucca_v3_source(lucca_token: Optional[str] = dlt.secrets.value) -> Any:
    # Create a REST API configuration for the Lucca API v3
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://reflect2-sandbox.ilucca-demo.net/api/v3/",
            "auth": CustomAuth(lucca_token),
            "paginator": CustomOffsetPaginator(
                param_name="paging", offset_initial_value=0, limit_value=1000
            ),
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "users",
                "write_disposition": "merge",
                "endpoint": {
                    "params": {
                        "formerEmployees": "true",
                        "modifiedAt": "since,{incremental.start_value}",
                        "fields": "firstName,lastName,login,mail,dtContractStart,legalEntityId,employeeNumber,departmentId,managerId,birthDate,cultureID,calendarId,rolePrincipalId,habilitedRoles[id],id,url,name,displayName,dtContractEnd,cspId,nationalityId,seniorityDate,insuranceNumber,userWorkCycles[id],picture[id],address,directLine,jobTitle,gender,personalEmail,personalMobile,professionalMobile,allowsElectronicPayslip,quote,personalCard,corporateCard,bankname,rib,iban,bic,frenchCarTaxHorsePower,frenchMotocyclesTaxHorsePower,unitSellPrice,modifiedAt,applicationData,extendedData",
                    },
                    "incremental": {
                        "cursor_path": "modifiedAt",
                        "initial_value": "1970-01-01T00:00:00Z",
                    },
                },

                
            },
            {
                "name": "departments",
                "endpoint": {
                    "params": {
                        "fields": "name,code,id,hierarchy,parentId,isActive,position,level,sortOrder,headId,head,users[id],currentUsers[id],currentUsersCount"
                    }
                },
            },
        ],
    }

    yield from rest_api_resources(config)


@dlt.source(name="lucca_v4", max_table_nesting=0)
def lucca_v4_source(lucca_token: Optional[str] = dlt.secrets.value) -> Any:
    # Create a REST API configuration for the Lucca API v4
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://reflect2-sandbox.ilucca-demo.net/directory/api/4.0/",
            "auth": CustomAuth(lucca_token),
            "paginator": PageNumberLimitPaginator(limit=1000, base_page=1),
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "replace",
        },
        "resources": [
            {"name": "work-contracts"},
        ],
    }

    yield from rest_api_resources(config)


def load_lucca() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_lucca",
        destination=dlt.destinations.duckdb("data/data.duckdb"),
        dataset_name="rest_api_data",
        dev_mode=False,
    )

    load_info_v3 = pipeline.run(lucca_v3_source())
    print(load_info_v3)  # noqa: T201
    load_info_v4 = pipeline.run(lucca_v4_source())
    print(load_info_v4)  # noqa: T201


if __name__ == "__main__":
    load_lucca()
