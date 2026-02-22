import os
import uvicorn
import json
import base64
from fastapi import FastAPI, APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.api_gateway_schema.external_schema import BikeDTO
from src.main.lambdas.admin_lambda import admin_lambda
from src.main.lambdas.bicycle_lambda import bicycle_lambda
from src.main.lambdas.common.dynamo_schema import Bike
from src.test.test_util.api_gateway_event import APIGatewayTestEvent
from src.test.test_util.dynamodb import LocalDynamoManager

TITLE = "Lambda API Schema"
DESCRIPTION = "Defining API schema that is validated by AWS API Gateway"
# Note: This is used to test lambda functions locally with API Gateway-like events

bicycle_lambda_router = APIRouter(tags=["bicycle lambdas"])
security = HTTPBearer()


def _unwrap_api_response(response):
    if isinstance(response, dict) and "statusCode" in response and "body" in response:
        status_code = response.get("statusCode", 200)
        try:
            body = json.loads(response["body"])
        except Exception:
            body = response["body"]
        return JSONResponse(content=body, status_code=status_code)
    return response


def _decode_bearer_claims(credentials: HTTPAuthorizationCredentials) -> dict:
    token = credentials.credentials
    parts = token.split(".")
    if len(parts) != 3:
        raise HTTPException(status_code=401, detail="Invalid bearer token")

    payload_segment = parts[1]
    padded_payload = payload_segment + "=" * (-len(payload_segment) % 4)

    try:
        payload_bytes = base64.urlsafe_b64decode(padded_payload)
        claims = json.loads(payload_bytes.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid bearer token payload") from exc

    if not claims.get("sub"):
        raise HTTPException(status_code=401, detail="Bearer token missing sub claim")
    return claims


@bicycle_lambda_router.get("", name="get bike by id")
async def get_bike(id: str = Query(...)) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="GET", query_params={"id": id})
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.put("", name="update bike by id")
async def update_bike(
        id: str = Query(...),
        bike_dto: BikeDTO = ...,
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Bike | dict:
    claims = _decode_bearer_claims(credentials)
    api_data = APIGatewayTestEvent(
        method="PUT",
        query_params={"id": id},
        body_json_str=bike_dto.model_dump_json(),
        authorizer_claims=claims,
    )
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.delete("", name="delete bike by id")
async def delete_bike(
        id: str = Query(...),
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    claims = _decode_bearer_claims(credentials)
    api_data = APIGatewayTestEvent(
        method="DELETE",
        query_params={"id": id},
        authorizer_claims=claims,
    )
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.post("/new")
async def save_bike(
        bike_dto: BikeDTO,
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Bike | dict:
    claims = _decode_bearer_claims(credentials)
    api_data = APIGatewayTestEvent(
        method="POST",
        body_json_str=bike_dto.model_dump_json(),
        authorizer_claims=claims,
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
