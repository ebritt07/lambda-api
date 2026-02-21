import pytest
from pydantic import ValidationError

from src.api_gateway_schema.external_schema import BikeDTO


def test_bike_dto_accepts_valid_style_enum_value():
    dto = BikeDTO(make="Orbea", model="Terra", style="ROAD", notes="fast gravel")

    assert dto.style.value == "ROAD"


def test_bike_dto_rejects_invalid_style_value():
    with pytest.raises(ValidationError):
        BikeDTO(make="Orbea", model="Terra", style="INVALID", notes="nope")


def test_bike_dto_notes_is_optional():
    dto = BikeDTO(make="Orbea", model="Terra", style="ROAD")

    assert dto.notes is None
