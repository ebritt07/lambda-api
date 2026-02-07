import uuid

import uvicorn
from fastapi import FastAPI, Request, APIRouter

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
@bicycle_lambda_router.get("/{id}", name="get bike by id")
async def get_bike(id: str) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="GET", query_params={"id":id})
    event = api_data.export_event()
    return bicycle_lambda.handler(event, {})

@bicycle_lambda_router.post("/new")
async def save_bike(bike_dto: BikeDTO) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="POST", body_dict=bike_dto.model_dump())
    event = api_data.export_event()
    return bicycle_lambda.handler(event, {})

user_profile_lambda_router = APIRouter(tags=["user profile lambdas "])
@user_profile_lambda_router.get("")
async def list_my_profile(request: Request):
    return {"msg", "no usr setup yet"}

admin_lambda_router = APIRouter(tags=["admin lambdas "])
@admin_lambda_router.get("/tables", description="admin operation to see all tables")
async def list_tables(request: Request):
    return admin_lambda.handler({}, {})


app = FastAPI(title= TITLE,
              description=DESCRIPTION)
app.include_router(bicycle_lambda_router, prefix="/bike")
app.include_router(user_profile_lambda_router, prefix="/usr")
app.include_router(admin_lambda_router, prefix="/admin")

if __name__ == "__main__":
    local_ddb = LocalDynamoManager()
    local_ddb.start_local_dynamo()
    uvicorn.run(app)