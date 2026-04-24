from sqlalchemy import Column, Integer, String
from database import Base

class Movie(Base):
    __tablename__ = "movie"

    id             = Column(Integer, primary_key=True, index=True)
    titulo         = Column(String, index=True)
    diretor        = Column(String)
    ano_lancamento = Column(Integer)
    genero         = Column(String)