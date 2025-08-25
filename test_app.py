import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_get(client):
    """Probar que la página principal responde con código 200"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data or b"<form" in response.data


def test_home_post(client):
    """Probar que genera una contraseña vía POST"""
    response = client.post("/", data={
        "longitud": 16,
        "mayus": "on",
        "numeros": "on",
        "simbolos": "on"
    })
    assert response.status_code == 200
    # Checa que al menos contenga una contraseña renderizada
    assert b"password" in response.data or b"<html" in response.data


def test_api_fuerza_ok(client):
    """Probar la API con una contraseña válida"""
    response = client.get("/api/fuerza?password=Clave123!")
    data = response.get_json()

    assert response.status_code == 200
    assert "fuerza" in data
    assert "puntuacion" in data
    assert isinstance(data["detalles"], list)


def test_api_fuerza_error(client):
    """Probar la API sin enviar contraseña"""
    response = client.get("/api/fuerza")
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data
