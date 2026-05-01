from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import SessionLocal, engine

app = FastAPI()

def get_db(): # pragma: no cover
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/movies/", status_code=status.HTTP_200_OK, response_model=schemas.StandardResponse[list[schemas.MovieResponse]])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    retorno = crud.select_all_movies(db, skip=skip, limit=limit)

    if retorno['status'] == 'empty':
        return {
            'status' : 'ok',
            'data'   : []
        }

    return retorno


@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.StandardResponse[schemas.MovieResponse])
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    retorno = crud.select_one_movie(db, movie_id=movie_id)

    if retorno['status'] == 'empty':
        raise HTTPException(status_code=404, detail=retorno['msg'])

    return retorno


@app.post("/movies/", status_code=status.HTTP_201_CREATED, response_model=schemas.StandardResponse)
def create_movie(movie: schemas.MovieCreate, response: Response, db: Session = Depends(get_db)):
    retorno = crud.insert_movie(db=db, movie=movie)

    if retorno['status'] == 'erro':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    response.headers["Location"] = f"/movies/{retorno['id']}"
    return retorno


@app.put("/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.StandardResponse)
def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db)):
    retorno = crud.update_movie(db, movie_id=movie_id, movie=movie)

    if retorno['status'] == 'empty':
        raise HTTPException(status_code=404, detail=retorno['msg'])

    if retorno['status'] == 'erro':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    return retorno


@app.patch("/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.StandardResponse)
def patch_movie(movie_id: int, movie: schemas.MoviePatch, db: Session = Depends(get_db)):
    retorno = crud.patch_movie(db, movie_id=movie_id, movie=movie)

    if retorno['status'] == 'empty':
        raise HTTPException(status_code=404, detail=retorno['msg'])

    if retorno['status'] == 'erro':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    return retorno


@app.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.StandardResponse)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    retorno = crud.delete_movie(db, movie_id=movie_id)

    if retorno['status'] == 'empty':
        raise HTTPException(status_code=404, detail=retorno['msg'])

    if retorno['status'] == 'erro':
        raise HTTPException(status_code=500, detail=retorno['msg'])

    return retorno