import pytest
import app.crud
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app, get_db

# Configuração do Banco de Dados de Teste (Em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_db.db"
engine                  = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal     = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_movie():
    response = client.post(
        "/movies/",
        json={"titulo": "Inception", "diretor": "Christopher Nolan", "ano_lancamento": 2010, "genero": "Ficção Científica"}
    )
    assert response.status_code      == 201
    assert response.json()["status"] == "ok"
    assert "id" in response.json()


def test_create_movie_internal_error():
    error_mock = {
        'status': 'erro',
        'msg'   : 'Erro interno no banco de dados'
    }

    with patch("app.crud.insert_movie", return_value=error_mock):
        response = client.post(
            "/movies/",
            json={"titulo": "Erro", "diretor": "D1", "ano_lancamento": 2024, "genero": "G1"}
        )

        assert response.status_code      == 500
        assert response.json()["detail"] == "Erro interno no banco de dados"


def test_read_one_movie():
    create_res = client.post("/movies/", json={"titulo": "The Matrix", "diretor": "Wachowskis", "ano_lancamento": 1999, "genero": "Sci-Fi"})
    movie_id   = create_res.json()["id"]

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code              == 200
    assert response.json()["data"]["titulo"] == "The Matrix"


def test_read_all_movies():
    client.post("/movies/", json={"titulo": "M1", "diretor": "D1", "ano_lancamento": 2000, "genero": "G1"})
    client.post("/movies/", json={"titulo": "M2", "diretor": "D2", "ano_lancamento": 2001, "genero": "G2"})

    response = client.get("/movies/")
    assert response.status_code         == 200
    assert len(response.json()["data"]) == 2


def test_read_all_movies_empty():
    response = client.get("/movies/")
    assert response.status_code    == 200
    assert response.json()["data"] == []


def test_read_one_movie_not_found():
    response = client.get("/movies/999")
    assert response.status_code == 404


def test_update_movie_put():
    create_res = client.post("/movies/", json={"titulo": "Old Title", "diretor": "D1", "ano_lancamento": 2000, "genero": "G1"})
    movie_id   = create_res.json()["id"]

    update_payload = {"titulo": "New Title", "diretor": "D1", "ano_lancamento": 2000, "genero": "G1"}
    response       = client.put(f"/movies/{movie_id}", json=update_payload)

    assert response.status_code == 200

    check = client.get(f"/movies/{movie_id}")
    assert check.json()["data"]["titulo"] == "New Title"


def test_update_put_non_existent_movie():
    response = client.put("/movies/9999", json={"titulo": "New Title", "diretor": "D1", "ano_lancamento": 2000, "genero": "G1"})
    assert response.status_code == 404


def test_update_put_internal_error():
    error_mock = {
        'status': 'erro',
        'msg'   : 'Erro interno no banco de dados'
    }

    with patch("app.crud.update_movie", return_value=error_mock):
        response = client.put(
            "/movies/9999",
            json={"titulo": "Erro", "diretor": "D1", "ano_lancamento": 2024, "genero": "G1"}
        )

        assert response.status_code      == 500
        assert response.json()["detail"] == "Erro interno no banco de dados"


def test_delete_movie():
    create_res = client.post("/movies/", json={"titulo": "To Delete", "diretor": "D1", "ano_lancamento": 2000, "genero": "G1"})
    movie_id   = create_res.json()["id"]

    delete_res = client.delete(f"/movies/{movie_id}")
    assert delete_res.status_code == 200

    check = client.get(f"/movies/{movie_id}")
    assert check.status_code == 404


def test_delete_non_existent_movie():
    response = client.delete("/movies/9999")
    assert response.status_code == 404


def test_delete_internal_error():
    error_mock = {
        'status': 'erro',
        'msg'   : 'Erro interno no banco de dados'
    }

    with patch("app.crud.delete_movie", return_value=error_mock):
        response = client.delete("/movies/9999")

        assert response.status_code      == 500
        assert response.json()["detail"] == "Erro interno no banco de dados"