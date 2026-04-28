import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app, get_db

# Configuração do Banco de Dados de Teste (Em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    assert response.status_code == 201
    assert response.json()["status"] == "ok"
    assert "id" in response.json()


def test_read_movies_empty():
    response = client.get("/movies/")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_read_one_movie_not_found():
    response = client.get("/movies/999")
    assert response.status_code == 404


def test_full_lifecycle():
    create_res = client.post("/movies/", json={
        "titulo": "The Matrix", "diretor": "Wachowskis", "ano_lancamento": 1999, "genero": "Ficção Científica"
    })
    movie_id = create_res.json()["id"]

    read_res = client.get(f"/movies/{movie_id}")
    assert read_res.status_code == 200
    assert read_res.json()["data"]["titulo"] == "The Matrix"

    update_res = client.put(f"/movies/{movie_id}", json={
        "titulo": "The Matrix Reloaded", "diretor": "Wachowskis", "ano_lancamento": 2003, "genero": "Ficção Científica"
    })
    assert update_res.status_code == 200

    del_res = client.delete(f"/movies/{movie_id}")
    assert del_res.status_code == 200

    final_res = client.get(f"/movies/{movie_id}")
    assert final_res.status_code == 404