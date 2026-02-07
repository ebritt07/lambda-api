from typing import Optional

from pydantic import BaseModel

from src.main.lambdas.common.dynamo_schema import BikeStyle


class BikeDTO(BaseModel):
    make: str
    model: str
    style: BikeStyle
    notes: Optional[str] = None
