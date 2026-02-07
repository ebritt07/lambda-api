import uuid
from typing import Optional

from pydantic import BaseModel, Field

from src.main.lambdas.common.dynamo_schema import Bike, BikeStyle


class BikeDTO(BaseModel, Bike):
    make: str = Field(..., example='Orbea')
    model: str
    style: BikeStyle
    notes: Optional[str] = None
