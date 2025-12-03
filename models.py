from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(300), nullable=False)
    created_at = Column(Date)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    founded_date = Column(Date, nullable=True)
    active = Column(Boolean, default=True)  # Soft delete flag

    members = relationship("CharacterTeam", back_populates="team")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    alias = Column(String(100), nullable=True)
    alignment = Column(String(50))
    first_appearance = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    active = Column(Boolean, default=True)  # Soft delete flag

    teams = relationship("CharacterTeam", back_populates="character")
    secret_identity = relationship("SecretIdentity", back_populates="character", uselist=False)


class SecretIdentity(Base):
    __tablename__ = "secret_identities"

    id = Column(Integer, primary_key=True, index=True)
    real_name = Column(String(100))
    birth_date = Column(Date, nullable=True)
    place_of_birth = Column(String(100), nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"))

    character = relationship("Character", back_populates="secret_identity")


class CharacterTeam(Base):
    __tablename__ = "character_team"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))

    character = relationship("Character", back_populates="teams")

    team = relationship("Team", back_populates="members")
