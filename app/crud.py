from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import models, schemas


def select_one_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if db_movie:
        return {
            'status': 'ok',
            'data'  : db_movie
        }

    return {
        'status': 'empty',
        'msg'   : 'Filme não encontrado'
    }


def select_all_movies(db: Session, skip: int = 0, limit: int = 10):
    list_movies = db.query(models.Movie).offset(skip).limit(limit).all()

    if list_movies:
        return {
            'status': 'ok',
            'data'  : list_movies
        }

    return {
        'status': 'empty',
        'msg'   : 'Nenhum filme encontrado'
    }


def insert_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(
        titulo=movie.titulo,
        diretor=movie.diretor,
        ano_lancamento=movie.ano_lancamento,
        genero=movie.genero
    )
    db.add(db_movie)
    try:
        db.commit()
        db.refresh(db_movie)
        return {
            'status': 'ok',
            'msg'   : 'Filme inserido com sucesso.',
            'id'    : db_movie.id
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            'status': 'erro',
            'msg'   : 'Erro ao inserir filme.'
        }


def update_movie(db: Session, movie_id: int, movie: schemas.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        db_movie.titulo = movie.titulo
        db_movie.diretor = movie.diretor
        db_movie.ano_lancamento = movie.ano_lancamento
        db_movie.genero = movie.genero
        try:
            db.commit()
            db.refresh(db_movie)
            return {
                'status': 'ok',
                'msg'   : 'Filme atualizado com sucesso.',
                'id'    : db_movie.id
            }
        except SQLAlchemyError as e:
            db.rollback()
            return {
                'status': 'erro',
                'msg'   : 'Erro ao atualizar filme.'
            }
    return {
        'status': 'empty',
        'msg'   : 'Filme não encontrado.'
    }


def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        try:
            db.delete(db_movie)
            db.commit()
            return {
                'status': 'ok',
                'msg'   : 'Filme removido com sucesso.',
                'id'    : movie_id
            }
        except SQLAlchemyError as e:
            db.rollback()
            return {
                'status': 'erro',
                'msg'   : 'Erro ao deletar filme.'
            }
    return {
        'status': 'empty',
        'msg'   : 'Filme não encontrado.'
    }