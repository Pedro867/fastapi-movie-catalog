import pytest

def test_full_movie_lifecycle(client):
    """
    Teste de integração que simula o ciclo de vida completo de um filme.
    Ele cria, lista, busca, atualiza (PUT e PATCH), e deleta um filme,
    verificando a persistência no banco de dados em cada etapa.
    """
    new_movie_payload = {
        "titulo"         : "Integration Test Movie",
        "diretor"        : "John Doe",
        "ano_lancamento" : 2025,
        "genero"         : "Testing"
    }
    response = client.post("/movies/", json=new_movie_payload)
    assert response.status_code      == 201
    assert response.json()["status"] == "ok"
    movie_id = response.json()["id"]
    assert movie_id is not None

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code  == 200
    movie_data = response.json()["data"]
    assert movie_data["titulo"]  == "Integration Test Movie"
    assert movie_data["diretor"] == "John Doe"

    response = client.get("/movies/")
    assert response.status_code == 200
    all_movies = response.json()["data"]
    assert any(m["id"] == movie_id for m in all_movies)
    assert isinstance(all_movies, list)

    response = client.put(f"/movies/{movie_id}", json={
        "titulo"         : "Integration Test Movie - Updated",
        "diretor"        : "John Doe Updated",
        "ano_lancamento" : 2026,
        "genero"         : "Testing Updated"
    })
    assert response.status_code == 200

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code         == 200
    movie_data = response.json()["data"]
    assert movie_data["titulo"]         == "Integration Test Movie - Updated"
    assert movie_data["ano_lancamento"] == 2026

    response = client.patch(f"/movies/{movie_id}", json={
        "titulo": "Integration Test Movie - Patched"
    })
    assert response.status_code == 200

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code         == 200
    movie_data = response.json()["data"]
    assert movie_data["titulo"]         == "Integration Test Movie - Patched"
    assert movie_data["diretor"]        == "John Doe Updated"
    assert movie_data["ano_lancamento"] == 2026

    response = client.delete(f"/movies/{movie_id}")
    assert response.status_code         == 200

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code         == 404

    response = client.post("/movies/", json={
        "titulo": "Filme Inválido",
        "diretor": "John Doe",
        "ano_lancamento": "dois mil e vinte cinco",
        "genero": "Testing"
    })
    assert response.status_code == 422

    response = client.get("/movies/999999")
    assert response.status_code == 404

    response = client.put("/movies/999999", json={
        "titulo": "Não Existente",
        "diretor": "Ninguém",
        "ano_lancamento": 2025,
        "genero": "Nenhum"
    })
    assert response.status_code == 404