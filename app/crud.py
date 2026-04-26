from sqlalchemy.orm import Session
import models, schemas


def select_one_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def select_all_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def insert_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(
        titulo=movie.titulo,
        diretor=movie.diretor,
        ano_lancamento=movie.ano_lancamento,
        genero=movie.genero
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(db: Session, movie_id: int, movie: schemas.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        db_movie.titulo = movie.titulo
        db_movie.diretor = movie.diretor
        db_movie.ano_lancamento = movie.ano_lancamento
        db_movie.genero = movie.genero
        db.commit()
        return True
    return False


def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        db.delete(db_movie)
        db.commit()
        return True
    return False