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

    class Config:
        from_attributes = True