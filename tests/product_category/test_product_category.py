from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_create_category():
    response = client.post("/category/", json={"name": "test category"})
    assert response.status_code == 200
    assert response.json()["name"] == "test category"


def test_read_category_by_name():
    category_name = "test category"

    response = client.get(f"/category/?category_name={category_name}")
    assert response.status_code == 200
    assert response.json()["name"] == "test category"
    return response


def test_read_category_by_id():
    category = test_read_category_by_name()
    category_id = category.json()["id"]

    response = client.get(f"/category/{category_id}")
    assert response.status_code == 200
    assert response.json()["id"] == category_id
    return response


def test_update_category():
    category = test_read_category_by_id()
    category_id = category.json()["id"]

    response = client.patch(
        f"/category/{category_id}", json={"name": "new test category name"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "new test category name"


def test_delete_category():
    category_name = "new test category name"
    get_category_response = client.get(f"/category/?category_name={category_name}")

    category_id = get_category_response.json()["id"]

    delete_response = client.delete(f"/category/{category_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["name"] == category_name
    assert delete_response.json()["id"] == category_id
