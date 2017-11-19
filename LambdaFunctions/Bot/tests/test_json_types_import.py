from Bot import utilities


def test_job_level_types_import():
    json = utilities.get_json("job_level_types.json")

    assert json["name"] == "JobLevel"
    assert json["enumerationValues"][0]["value"] == "professional"


def test_job_location_types_import():
    json = utilities.get_json("job_location_types.json")

    assert json["name"] == "JobLocation"
    assert json["enumerationValues"][0]["value"] == "Freiburg"


def test_job_position_types_import():
    json = utilities.get_json("job_position_types.json")

    assert json["name"] == "JobPosition"
    assert json["enumerationValues"][0]["value"] == "manager"
