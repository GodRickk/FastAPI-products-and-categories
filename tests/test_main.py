import pytest
import fastapi
from fastapi.testclient import TestClient
import main


client = TestClient(main.app)


def test_create_category():
    response = client.post("/category/",
                           json={"name": "test category"})
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
    

def test_create_product():
    response = client.post("/product/",
                           json={"price": 123,
                                 "amount": 3000,
                                 "name": "Test simple product",
                                 "category_id": 0
                                 })
    if response.status_code == 400:
        print("Product with same name has already exist in database")
        assert response.json()["name"] == "Test simple product"
    else:
        assert response.status_code == 200
        assert response.json()["name"] == "Test simple product"


def test_create_product_with_category():
    category = test_read_category_by_name()
    response = client.post("/product-with-category/", 
                           json={"name": "Test product with category", 
                                 "price": 1500, 
                                 "amount": 8000, 
                                 "category_id": category.json()["id"]})
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

    response = client.patch(f"/product/{product_id}", 
                          json={"name": "New product name with category", 
                                "price": 100, 
                                "amount": 8})
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

# сделать так чтобы при запуске тестов командой pytest все тесты отрабатывли и при перезапуске этих тестов
# !хардкод нужных значений а не вызов тестирующий функций!
# сделать такие тесты чтобы они создавали сущности в базе, получали их, модифицировали и потом их же удаляли
# это обеспечит возможность перезапуска тестов и их успешное выполенение
# (не будет ошибок что сущность с таким имененм уже создана)
def test_update_category():
    category = test_read_category_by_id()
    category_id = category.json()["id"]

    response = client.patch(f"/category/{category_id}",
                            json={"name": "new test category name"})
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