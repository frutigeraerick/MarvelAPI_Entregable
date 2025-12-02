from datetime import date
from pydantic import BaseModel



class TeamBase(BaseModel):
    name: str
    founded_date: date | None = None
    active: bool = True

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int

    class Config:
        from_attributes = True



class SecretIdentityBase(BaseModel):
    real_name: str
    birth_date: date | None = None
    place_of_birth: str | None = None

class SecretIdentityCreate(SecretIdentityBase):
    character_id: int

class SecretIdentity(SecretIdentityBase):
    id: int
    character_id: int

    class Config:
        from_attributes = True



class CharacterTeamBase(BaseModel):
    character_id: int
    team_id: int

class CharacterTeamCreate(CharacterTeamBase):
    pass

class CharacterTeam(CharacterTeamBase):
    id: int
    team: Team | None = None

    class Config:
        from_attributes = True



class CharacterBase(BaseModel):
    name: str
    alias: str | None = None
    alignment: str
    first_appearance: date | None = None
    description: str | None = None
    active: bool = True

class CharacterCreate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int
    secret_identity: SecretIdentity | None = None
    teams: list[CharacterTeam] = []

    class Config:
        from_attributes = True