from typing import Optional

from pydantic import BaseModel

from src.main.lambdas.common.dynamo_schema import BikeStyle

# data classes included here will be generated as part of the openapi schema
# and wired into API Gateway's model validation.


class BikeDTO(BaseModel):
    make: str
    model: str
    style: BikeStyle
    notes: Optional[str] = None


class BikeListItemDTO(BaseModel):
    id: str
    make: str
    model: str
    style: BikeStyle
    notes: Optional[str] = None


class BikeListResponseDTO(BaseModel):
    items: list[BikeListItemDTO]
    next_token: Optional[str] = None
    count: int
