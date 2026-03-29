from sqlalchemy import Column, Integer, String
from database import Base

class Link(Base):
    __tablename__="links"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    url = Column(String)
    usuario_id = Column(Integer)

class Usuario(Base):
    __tablename__= "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    bio = Column(String)
    foto_url = Column(String)
    fundo_url = Column(String)
