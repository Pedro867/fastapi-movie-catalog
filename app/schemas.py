from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')

class MovieBase(BaseModel):
    titulo         : str
    diretor        : str
    ano_lancamento : int
    genero         : str

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int

class MovieUpdate(MovieBase):
    pass

    model_config = ConfigDict(from_attributes=True)

class MoviePatch(BaseModel):
    titulo         : Optional[str] = None
    diretor        : Optional[str] = None
    ano_lancamento : Optional[int] = None
    genero         : Optional[str] = None

class StandardResponse(BaseModel, Generic[T]):
    status : str
    msg    : Optional[str] = None
    data   : Optional[T]   = None
    id     : Optional[int] = None
