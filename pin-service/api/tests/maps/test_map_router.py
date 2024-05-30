from api.tests.conftest import client


# def test_get_map(test_db):
#     response = client.post(
#         "/maps/",
#         json={"name": "boston"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     id = data["id"]

#     response = client.get(f'/maps/{id}')
#     expected = {
#         "id": id,
#         "name": "boston",
#         "pins": []
#     }
#     assert response.json() == expected


# def test_get_maps(test_db):
#     response = client.post("/maps/", json={"name": "boston"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     map_id = data["id"]

#     response = client.get('/maps/')
#     data = response.json()
#     expected = [
#         {
#             "id": map_id,
#             "name": "boston",
#             "pins": []
#         }
#     ]
#     assert len(data) == 1
#     assert data == expected
