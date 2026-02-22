import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional


class BikeStyle(StrEnum):
    OTHER = "OTHER"
    ROAD = "ROAD"
    MOUNTAIN = "MOUNTAIN"
    CRUISER = "CRUISER"
    FIXIE = "FIXIE"


@dataclass
class Bike:
    make: str
    model: str
    style: str
    owner_id: str
    notes: Optional[str]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
