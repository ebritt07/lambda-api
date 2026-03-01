import os
import uvicorn
import json
import base64
from fastapi import FastAPI, APIRouter, Query, Request
from fastapi.responses import JSONResponse

from src.api_gateway_schema.external_schema import BikeDTO, BikeListResponseDTO
from src.main.lambdas.admin_lambda import admin_lambda
from src.main.lambdas.bicycle_lambda import bicycle_lambda
from src.main.lambdas.common.dynamo_schema import Bike
from src.test.test_util.api_gateway_event import APIGatewayTestEvent
from src.test.test_util.dynamodb import LocalDynamoManager

TITLE = "Lambda API Schema"
DESCRIPTION = "Defining API schema that is validated by AWS API Gateway"
# Note: This is used to test lambda functions locally with API Gateway-like events

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


def _extract_claims_from_auth_header(request: Request) -> dict | None:
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        return None

    token = auth_header.split(" ", 1)[1]
    parts = token.split(".")
    if len(parts) != 3:
        return None

    payload_segment = parts[1]
    padded_payload = payload_segment + "=" * (-len(payload_segment) % 4)

    try:
        payload_bytes = base64.urlsafe_b64decode(padded_payload)
        claims = json.loads(payload_bytes.decode("utf-8"))
    except Exception:
        return None

    return claims if isinstance(claims, dict) else None


@bicycle_lambda_router.get("", name="get bike by id")
async def get_bike(id: str = Query(...)) -> Bike | dict:
    api_data = APIGatewayTestEvent(method="GET", raw_path="/bike", query_params={"id": id})
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.get("/list", name="list bikes")
async def list_bikes(
        limit: int = Query(25, ge=1, le=100),
        next_token: str | None = Query(None),
) -> BikeListResponseDTO | dict:
    query_params = {"limit": str(limit)}
    if next_token is not None:
        query_params["next_token"] = next_token
    api_data = APIGatewayTestEvent(method="GET", raw_path="/bike/list", query_params=query_params)
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.put("", name="update bike by id")
async def update_bike(
        request: Request,
        id: str = Query(...),
        bike_dto: BikeDTO = ...,
) -> Bike | dict:
    api_data = APIGatewayTestEvent(
        method="PUT",
        raw_path="/bike",
        query_params={"id": id},
        body_json_str=bike_dto.model_dump_json(),
        authorizer_claims=_extract_claims_from_auth_header(request),
    )
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.delete("", name="delete bike by id")
async def delete_bike(
        request: Request,
        id: str = Query(...),
) -> dict:
    api_data = APIGatewayTestEvent(
        method="DELETE",
        raw_path="/bike",
        query_params={"id": id},
        authorizer_claims=_extract_claims_from_auth_header(request),
    )
    event = api_data.export_event()
    return _unwrap_api_response(bicycle_lambda.handler(event, {}))


@bicycle_lambda_router.post("/new")
async def save_bike(
        request: Request,
        bike_dto: BikeDTO,
) -> Bike | dict:
    api_data = APIGatewayTestEvent(
        method="POST",
        raw_path="/bike/new",
        body_json_str=bike_dto.model_dump_json(),
        authorizer_claims=_extract_claims_from_auth_header(request),
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
