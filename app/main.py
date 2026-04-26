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


@app.get("/movies/", response_model=schemas.StandardResponse[list[schemas.MovieResponse]])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    retorno = crud.select_all_movies(db, skip=skip, limit=limit)

    if retorno['status'] == 'empty':
        return {'status': 'ok', 'data': []}

    return retorno


@app.get("/movies/{movie_id}", response_model=schemas.StandardResponse[schemas.MovieResponse])
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    retorno = crud.select_one_movie(db, movie_id=movie_id)

    if retorno['status'] == 'empty':
        raise HTTPException(status_code=404, detail=retorno['msg'])

    return retorno


@app.post("/movies/", status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    retorno = crud.insert_movie(db=db, movie=movie)

    if retorno['status'] == 'erro':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    return retorno


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db)):
    retorno = crud.update_movie(db, movie_id=movie_id, movie=movie)

    if retorno['status'] == 'empty':
        raise HTTPException(status_code=404, detail=retorno['msg'])

    if retorno['status'] == 'erro':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    return retorno


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    retorno = crud.delete_movie(db, movie_id=movie_id)

    if retorno['status'] == 'empty':
        raise HTTPException(status_code=404, detail=retorno['msg'])

    if retorno['status'] == 'erro':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    return retorno