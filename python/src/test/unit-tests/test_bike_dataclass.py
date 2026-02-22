import uuid

from src.main.lambdas.common.dynamo_schema import Bike


def test_bike_stores_passed_fields():
    bike = Bike(make="Orbea", model="Terra", style="ROAD", owner_id="user-1", notes="gravel setup")

    assert bike.make == "Orbea"
    assert bike.model == "Terra"
    assert bike.style == "ROAD"
    assert bike.owner_id == "user-1"
    assert bike.notes == "gravel setup"


def test_bike_generates_unique_uuid_ids_when_omitted():
    bike_one = Bike(make="BMC", model="Roadmachine", style="ROAD", owner_id="user-1", notes=None)
    bike_two = Bike(make="Trek", model="Domane", style="ROAD", owner_id="user-2", notes=None)

    assert bike_one.id
    assert bike_two.id
    assert bike_one.id != bike_two.id
    assert str(uuid.UUID(bike_one.id)) == bike_one.id
    assert str(uuid.UUID(bike_two.id)) == bike_two.id


def test_bike_preserves_explicit_id():
    bike = Bike(make="Surly", model="Steamroller", style="FIXIE", owner_id="user-1", notes=None, id="bike-123")

    assert bike.id == "bike-123"


def test_bike_allows_notes_none():
    bike = Bike(make="Soma", model="Wolverine", style="OTHER", owner_id="user-1", notes=None)

    assert bike.notes is None


def test_bike_equality_matches_dataclass_field_values():
    bike_one = Bike(make="Cannondale", model="Topstone", style="OTHER", owner_id="user-1", notes="all-road", id="same-id")
    bike_two = Bike(make="Cannondale", model="Topstone", style="OTHER", owner_id="user-1", notes="all-road", id="same-id")
    bike_three = Bike(make="Cannondale", model="Topstone", style="OTHER", owner_id="user-1", notes="all-road", id="different-id")

    assert bike_one == bike_two
    assert bike_one != bike_three


def test_bike_repr_contains_key_fields():
    bike = Bike(make="State", model="4130", style="OTHER", owner_id="user-1", notes=None, id="repr-id")

    representation = repr(bike)

    assert "Bike(" in representation
    assert "make='State'" in representation
    assert "model='4130'" in representation
    assert "owner_id='user-1'" in representation
    assert "id='repr-id'" in representation
