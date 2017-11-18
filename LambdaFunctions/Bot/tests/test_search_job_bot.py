from bot import utilities

def test_job_level_types_enum():
    types = utilities.load_enumeration_values("job_level_types.json")

    assert types == tuple(("professional", "young_talent"))


def test_location_types_enum():
    types = utilities.load_enumeration_values("job_location_types.json")

    assert types == tuple(("Freiburg", "Timisoara"))


def test_position_types_enum():
    types = utilities.load_enumeration_values("job_position_types.json")

    assert types == tuple(("manager", "tester", "developer", "java developer", "qa"))
