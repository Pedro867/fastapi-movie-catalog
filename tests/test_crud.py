import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.database import Base
from app import crud, schemas

# Configuração do Banco de Dados de Teste (Em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_db_crud.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_insert_movie(db_session):
    movie_in = schemas.MovieCreate(
        titulo         = "Test Movie",
        diretor        = "Test Director",
        ano_lancamento = 2024,
        genero         = "Action"
    )
    result = crud.insert_movie(db_session, movie_in)
    assert result["status"] == "ok"
    assert "id" in result
    assert result["msg"] == "Filme inserido com sucesso."


def test_insert_movie_error(db_session, monkeypatch):
    movie_in = schemas.MovieCreate(
        titulo         = "Test Movie",
        diretor        = "Test Director",
        ano_lancamento = 2024,
        genero         = "Action"
    )

    def mock_commit():
        raise SQLAlchemyError("Mock error")

    monkeypatch.setattr(db_session, "commit", mock_commit)

    result = crud.insert_movie(db_session, movie_in)
    assert result["status"] == "erro"
    assert result["msg"]    == "Erro ao inserir filme."


def test_select_one_movie(db_session):
    movie_in = schemas.MovieCreate(titulo="Test", diretor="Dir", ano_lancamento=2000, genero="Gen")
    inserted = crud.insert_movie(db_session, movie_in)

    result = crud.select_one_movie(db_session, inserted["id"])
    assert result["status"]      == "ok"
    assert result["data"].titulo == "Test"


def test_select_one_movie_empty(db_session):
    result = crud.select_one_movie(db_session, 999)
    assert result["status"] == "empty"
    assert result["msg"]    == "Filme não encontrado"


def test_select_all_movies(db_session):
    movie1 = schemas.MovieCreate(titulo="T1", diretor="D1", ano_lancamento=2001, genero="G1")
    movie2 = schemas.MovieCreate(titulo="T2", diretor="D2", ano_lancamento=2002, genero="G2")
    crud.insert_movie(db_session, movie1)
    crud.insert_movie(db_session, movie2)

    result = crud.select_all_movies(db_session)
    assert result["status"] == "ok"
    assert len(result["data"]) >= 2


def test_select_all_movies_empty(db_session):
    result = crud.select_all_movies(db_session)
    assert result["status"] == "empty"
    assert result["msg"]    == "Nenhum filme encontrado"


def test_update_movie(db_session):
    movie_in = schemas.MovieCreate(titulo="Old", diretor="D", ano_lancamento=2000, genero="G")
    inserted = crud.insert_movie(db_session, movie_in)

    movie_up = schemas.MovieUpdate(titulo="New", diretor="D", ano_lancamento=2000, genero="G")
    result   = crud.update_movie(db_session, inserted["id"], movie_up)
    assert result["status"] == "ok"

    updated = crud.select_one_movie(db_session, inserted["id"])
    assert updated["data"].titulo == "New"


def test_update_movie_empty(db_session):
    movie_up = schemas.MovieUpdate(titulo="New", diretor="D", ano_lancamento=2000, genero="G")
    result   = crud.update_movie(db_session, 999, movie_up)
    assert result["status"] == "empty"


def test_update_movie_error(db_session, monkeypatch):
    movie_in = schemas.MovieCreate(titulo="Old", diretor="D", ano_lancamento=2000, genero="G")
    inserted = crud.insert_movie(db_session, movie_in)

    movie_up = schemas.MovieUpdate(titulo="New", diretor="D", ano_lancamento=2000, genero="G")

    def mock_commit():
        raise SQLAlchemyError("Mock error")
    monkeypatch.setattr(db_session, "commit", mock_commit)

    result = crud.update_movie(db_session, inserted["id"], movie_up)
    assert result["status"] == "erro"


def test_patch_movie(db_session):
    movie_in = schemas.MovieCreate(titulo="Old", diretor="D", ano_lancamento=2000, genero="G")
    inserted = crud.insert_movie(db_session, movie_in)

    movie_patch = schemas.MoviePatch(titulo="Patched")
    result      = crud.patch_movie(db_session, inserted["id"], movie_patch)
    assert result["status"] == "ok"

    patched = crud.select_one_movie(db_session, inserted["id"])
    assert patched["data"].titulo  == "Patched"
    assert patched["data"].diretor == "D"


def test_patch_movie_empty(db_session):
    movie_patch = schemas.MoviePatch(titulo="Patched")
    result = crud.patch_movie(db_session, 999, movie_patch)
    assert result["status"] == "empty"


def test_patch_movie_error(db_session, monkeypatch):
    movie_in = schemas.MovieCreate(titulo="Old", diretor="D", ano_lancamento=2000, genero="G")
    inserted = crud.insert_movie(db_session, movie_in)

    movie_patch = schemas.MoviePatch(titulo="Patched")

    def mock_commit():
        raise SQLAlchemyError("Mock error")
    monkeypatch.setattr(db_session, "commit", mock_commit)

    result = crud.patch_movie(db_session, inserted["id"], movie_patch)
    assert result["status"] == "erro"


def test_delete_movie(db_session):
    movie_in = schemas.MovieCreate(titulo="Del", diretor="D", ano_lancamento=2000, genero="G")
    inserted = crud.insert_movie(db_session, movie_in)

    result = crud.delete_movie(db_session, inserted["id"])
    assert result["status"] == "ok"

    check = crud.select_one_movie(db_session, inserted["id"])
    assert check["status"] == "empty"


def test_delete_movie_empty(db_session):
    result = crud.delete_movie(db_session, 999)
    assert result["status"] == "empty"


def test_delete_movie_error(db_session, monkeypatch):
    movie_in = schemas.MovieCreate(titulo="Del", diretor="D", ano_lancamento=2000, genero="G")
    inserted = crud.insert_movie(db_session, movie_in)

    def mock_commit():
        raise SQLAlchemyError("Mock error")
    monkeypatch.setattr(db_session, "commit", mock_commit)

    result = crud.delete_movie(db_session, inserted["id"])
    assert result["status"] == "erro"