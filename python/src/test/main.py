import os
import uvicorn
import json
from fastapi import FastAPI, APIRouter, Query
from fastapi.responses import JSONResponse

from src.api_gateway_schema.external_schema import BikeDTO
from src.main.lambdas.admin_lambda import admin_lambda
from src.main.lambdas.bicycle_lambda import bicycle_lambda
from src.main.lambdas.common.dynamo_schema import Bike
from src.test.test_util.api_gateway_event import APIGatewayTestEvent
from src.test.test_util.dynamodb import LocalDynamoManager

TITLE = "Lambda API Schema"
DESCRIPTION = "Defining API schema that is validated by AWS API Gateway"
## Note: This is used to test lambda functions locally with API Gateway-like events

bicycle_lambda_router = APIRouter(tags=["bicycle lambdas"])


def _unwrap_api_response(response):
    if isinstance(response, dict) and "statusCode" in response and "body" in response:
        status_code = response.get("statusCode", 200)
        try:
            body = json.loads(response["body"])
        except Exception:
            body = response["body"]
        return JSONResponse(content=body, status_code=status_code)
    return response


@bicycle_lambda_router.get("", name="get bike by id")
async def get_bike(id: str = Query(...)) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="GET", query_params={"id": id})
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.put("", name="update bike by id")
async def update_bike(id: str = Query(...), bike_dto: BikeDTO = ...) -> Bike | dict:
    api_data = APIGatewayTestEvent(
        method="PUT",
        query_params={"id": id},
        body_json_str=bike_dto.model_dump_json(),
    )
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.delete("", name="delete bike by id")
async def delete_bike(id: str = Query(...)) -> dict:
    api_data = APIGatewayTestEvent(method="DELETE", query_params={"id": id})
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.post("/new")
async def save_bike(bike_dto: BikeDTO) -> Bike | dict:
    api_data = APIGatewayTestEvent(
        method="POST",
        body_json_str=bike_dto.model_dump_json(),
    )
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


admin_lambda_router = APIRouter(tags=["admin lambdas "])


@admin_lambda_router.get("/tables", description="admin operation to see all tables")
async def list_tables():
    return _unwrap_api_response(admin_lambda.handler({}, {}))


app = FastAPI(title=TITLE,
              description=DESCRIPTION)
app.include_router(bicycle_lambda_router, prefix="/bike")
app.include_router(admin_lambda_router, prefix="/admin")

if __name__ == "__main__":
    os.environ["ENV"] = "LOCAL"
    local_ddb = LocalDynamoManager()
    local_ddb.start_local_dynamo()
    uvicorn.run(app)
