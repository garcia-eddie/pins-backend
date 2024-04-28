from api.tests.conftest import client


def test_get_pins(test_db):
    response = client.post("/maps/", json={"name": "Somerville"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    map_id = data["id"]

    request = {
        "name": "Ogawa",
        "coordinates": [42.35695407894345, -71.05786815495368],
        "map_id": map_id
    }
    response = client.post("/pins/", json=request)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    pin_id = data["id"]

    response = client.get('/pins/')
    data = response.json()
    expected = [
        {
            "id": pin_id,
            "name": "Ogawa",
            "coordinates": [42.35695407894345, -71.05786815495368],
            "map_id": map_id
        }
    ]
    assert len(data) == 1
    assert data == expected
