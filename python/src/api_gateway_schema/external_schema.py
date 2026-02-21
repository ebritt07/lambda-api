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
