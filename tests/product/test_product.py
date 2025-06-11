from fastapi.testclient import TestClient
import main


client = TestClient(main.app)


def test_create_product_with_category():
    category = test_read_category_by_name()
    response = client.post(
        "/product-with-category/",
        json={
            "name": "Test product with category",
            "price": 1500,
            "amount": 8000,
            "category_id": category.json()["id"],
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test product with category"
    return response


def test_read_product_by_name():
    product_name = "Test product with category"

    get_response = client.get(f"/product/?product_name={product_name}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test product with category"
    return get_response


def test_read_product_by_id():
    product = test_read_product_by_name()
    product_id = product.json()["id"]

    get_response = client.get(f"/product/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == product_id
    return get_response


def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_product():
    product = test_read_product_by_id()
    product_id = product.json()["id"]

    response = client.patch(
        f"/product/{product_id}",
        json={"name": "New product name with category", "price": 100, "amount": 8},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New product name with category"
    assert response.json()["price"] == 100
    assert response.json()["amount"] == 8


def test_delete_product_with_category():
    get_response = client.get("/product/?product_name=New product name with category")
    product_id = get_response.json()["id"]

    delete_response = client.delete(f"/product/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == product_id
    assert delete_response.json()["name"] == "New product name with category"

    check_response = client.get(f"/products/{product_id}")
    assert check_response.status_code == 404


def test_delete_poduct():
    get_response = client.get("/product/?product_name=Test simple product")
    product_id = get_response.json()["id"]

    delete_response = client.delete(f"/product/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == product_id
    assert delete_response.json()["name"] == "Test simple product"

    check_response = client.get(f"/products/{product_id}")
    assert check_response.status_code == 404