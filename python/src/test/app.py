import os
import uvicorn
import json
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse

from src.main.api_gateway_schema.external_schema import BikeDTO
from src.main.lambdas.admin_lambda import admin_lambda
from src.main.lambdas.bicycle_lambda import bicycle_lambda
from src.main.lambdas.common.dynamo_schema import Bike
from src.main.lambdas.common.logger import logger
from src.test.test_util.api_gateway_event import APIGatewayTestEvent
from src.test.test_util.dynamodb import LocalDynamoManager

TITLE = "[Local] Lambda API Tester"
DESCRIPTION = """

Interactive tester:
 - Test Lambda core functionality
 - Generate JSON Schema generates that API Gateway will use.
 - In summary, even though this lives in the 'test' directory, the generated json schema is actually PRODUCTION code. 

Explaining why:
 - This project aims to have very lightweight lambdas with almost instant
start up time (even when cold)!.
 - To do so, we constrict the lambdas to only do simple db operations
and business logic validations.
 - All syntax validation will be performed by API Gateway, using this json schema.
"""

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

@bicycle_lambda_router.get("/{id}", name="get bike by id")
async def get_bike(id: str) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="GET", query_params={"id":id})
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))

@bicycle_lambda_router.put("/{id}", name="update bike by id")
async def update_bike(id: str, bike_dto: BikeDTO) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="PUT", query_params={"id":id}, body_dict=bike_dto.model_dump())
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))

@bicycle_lambda_router.delete("/{id}", name="delete bike by id")
async def delete_bike(id: str) -> dict:
    api_data = APIGatewayTestEvent(method="DELETE", query_params={"id":id})
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))

@bicycle_lambda_router.post("/new")
async def save_bike(bike_dto: BikeDTO) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="POST", body_dict=bike_dto.model_dump())
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))

user_profile_lambda_router = APIRouter(tags=["user profile lambdas "])
@user_profile_lambda_router.get("")
async def list_my_profile(request: Request):
    return {"msg", "no usr setup yet"}

admin_lambda_router = APIRouter(tags=["admin lambdas "])
@admin_lambda_router.get("/tables", description="admin operation to see all tables")
async def list_tables(request: Request):
    return _unwrap_api_response(admin_lambda.handler({}, {}))


app = FastAPI(title= TITLE,
              description=DESCRIPTION)
app.include_router(bicycle_lambda_router, prefix="/bike")
app.include_router(user_profile_lambda_router, prefix="/usr")
app.include_router(admin_lambda_router, prefix="/admin")

if __name__ == "__main__":
    os.putenv("ENV", "LOCAL")
    os.putenv("AWS_ACCESS_KEY_ID", "test-id")
    os.putenv("AWS_SECRET_ACCESS_KEY", "test-key")
    local_ddb = LocalDynamoManager()
    local_ddb.start_local_dynamo()
    uvicorn.run(app)
