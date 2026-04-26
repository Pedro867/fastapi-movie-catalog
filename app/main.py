from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/movies/", status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    retorno = crud.insert_movie(db=db, movie=movie)

    if retorno['status'] != 'ok':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    return retorno


@app.get("/movies/", response_model=list[schemas.MovieResponse])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = crud.select_all_movies(db, skip=skip, limit=limit)
    return movies


@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.select_one_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return db_movie


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db)):
    print(movie_id)
    success = crud.update_movie(db, movie_id=movie_id, movie=movie)
    if not success:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return {"message": "Filme atualizado com sucesso"}


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    success = crud.delete_movie(db, movie_id=movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Filme não encontrado para deletar")
    return {"message": "Filme removido com sucesso"}