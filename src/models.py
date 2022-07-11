import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from eralchemy import render_er


Base = declarative_base()

association_planet_film = Table(
    "association_planet_film",
    Base.metadata,
    Column("planet_id", ForeignKey("planet.id"), primary_key=True),
    Column("film_id", ForeignKey("film.id"), primary_key=True),
)

association_character_film = Table(
    "association_character_film",
    Base.metadata,
    Column("character_id", ForeignKey("character.id"), primary_key=True),
    Column("film_id", ForeignKey("film.id"), primary_key=True),
)

association_favs_characters = Table(
    "association_favs_characters",
    Base.metadata,
    Column("character_id", ForeignKey("character.id")),
    Column("personajes_favoritos_id", ForeignKey("personajes_favoritos.id")),
)

association_favs_planets = Table(
    "association_favs_planets",
    Base.metadata,
    Column("character_id", ForeignKey("character.id")),
    Column("personajes_favoritos_id", ForeignKey("personajes_favoritos.id")),
)

class Favs_characters(Base):
    __tablename__ = 'personajes_favoritos'
    id = Column(Integer, primary_key=True)
    character = relationship("Character", secondary=association_favs_characters, back_populates="personajes_favoritos")
    # user_id = Column(Integer, ForeignKey("user.id"))
    # user = relationship("User", backref=backref("personajes_favoritos", uselist=False))

    # user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    # user = relationship("User", back_populates="personajes favoritos")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    is_loggin = Column(Boolean, default=False, nullable=False)
    personajes_favoritos_id = Column(Integer, ForeignKey('personajes_favoritos.id'))
    # favs_characters_id = Column(Integer, ForeignKey(Favs_characters), primary_key=True)
    # friend = relationship('User', foreign_keys='personajes_favoritos.favs_characters_id')
    # friend_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    # favs_characters_id = Column(Integer, ForeignKey('personajes_favoritos.id'), unique=True)
    # favs_characters = relationship("Favs_characters", backref=backref("user", uselist=False))
    # favs_planets_id = Column(Integer, ForeignKey('planetas_favoritos.id'), unique=True)
    # favs_planets = relationship("Favs_planets", backref=backref("user", uselist=False))
    # favorits_characters = relationship("Favs_characters", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # favorits_planets = relationship("Favs_planets", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    hair_color = Column(String(50))
    birth_year = Column(DateTime())
    film = relationship(
        "Film", secondary=association_character_film, back_populates="films"
    )
    url = Column(String(100), nullable=False)
    personajes_favoritos = relationship(
        "Favs_characters", secondary=association_favs_characters, back_populates="character"
    )


class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    
    name = Column(String(50), nullable=False)
    diameter = Column(Integer)
    population = Column(Integer)
    film = relationship(
        "Film", secondary=association_planet_film, back_populates="films"
    )
    resident_id = Column(Integer, ForeignKey("character.id"))
    resident = relationship("Character")
    planet = relationship(
        "Favs_planets", secondary=association_favs_planets, back_populates="planetas_favoritos"
    )

class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)
    episode_id = Column(Integer, nullable=False)
    director = Column(String(50), nullable=False)
    character = relationship(
        "Character", secondary=association_character_film, back_populates="characters"
    )
    planet = relationship(
        "Planet", secondary=association_planet_film, back_populates="planets"
    )
    
class Favs_planets(Base):
    __tablename__ = 'planetas_favoritos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref=backref("planetas_favoritos", uselist=False))
    planetas_favoritos = relationship(
        "Favs_planets", secondary=association_favs_planets, back_populates="planet"
    )
    # user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    # user = relationship("User", back_populates="planetas favoritos")


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')