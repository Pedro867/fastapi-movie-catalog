from pydantic import BaseModel

class MovieBase(BaseModel):
    titulo:         str
    diretor:        str
    ano_lancamento: int
    genero:         str

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int

class MovieUpdate(MovieBase):
    pass

    class Config:
        from_attributes = True
