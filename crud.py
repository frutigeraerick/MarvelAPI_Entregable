from sqlalchemy.orm import Session, joinedload
import models, schemas



def get_characters(db: Session):
    return db.query(models.Character).filter(models.Character.active == True).all()


def get_character(db: Session, character_id: int):
    return db.query(models.Character).filter(models.Character.id == character_id).first()


def create_character(db: Session, character: schemas.CharacterCreate):
    db_character = models.Character(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


def update_character(db: Session, character_id: int, character: schemas.CharacterCreate):
    db_character = get_character(db, character_id)
    if db_character:
        for key, value in character.dict().items():
            setattr(db_character, key, value)
        db.commit()
        db.refresh(db_character)
    return db_character


def delete_character(db: Session, character_id: int):
    db_character = get_character(db, character_id)
    if db_character:
        db_character.active = False  
        db.commit()
        db.refresh(db_character)
    return db_character


def restore_character(db: Session, character_id: int):
    db_character = get_character(db, character_id)
    if db_character:
        db_character.active = True
        db.commit()
        db.refresh(db_character)
    return db_character



def get_teams(db: Session):
    return db.query(models.Team).filter(models.Team.active == True).all()


def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def update_team(db: Session, team_id: int, team: schemas.TeamCreate):
    db_team = get_team(db, team_id)
    if db_team:
        for key, value in team.dict().items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_id: int):
    db_team = get_team(db, team_id)
    if db_team:
        db_team.active = False  
        db.commit()
        db.refresh(db_team)
    return db_team


def restore_team(db: Session, team_id: int):
    db_team = get_team(db, team_id)
    if db_team:
        db_team.active = True
        db.commit()
        db.refresh(db_team)
    return db_team



def get_identities(db: Session):

    return db.query(models.SecretIdentity).all()


def get_identity(db: Session, identity_id: int):
    return db.query(models.SecretIdentity).filter(models.SecretIdentity.id == identity_id).first()


def create_identity(db: Session, identity: schemas.SecretIdentityCreate):

    character = db.query(models.Character).filter(models.Character.id == identity.character_id).first()
    if not character:
        raise ValueError("Character not found")

    existing = db.query(models.SecretIdentity).filter(models.SecretIdentity.character_id == identity.character_id).first()
    if existing:
        raise ValueError("Character already has a SecretIdentity")

    db_identity = models.SecretIdentity(**identity.dict())
    db.add(db_identity)
    db.commit()
    db.refresh(db_identity)
    return db_identity


def update_identity(db: Session, identity_id: int, identity: schemas.SecretIdentityCreate):
    db_identity = get_identity(db, identity_id)
    if db_identity:
        new_char_id = identity.character_id
        if new_char_id != db_identity.character_id:
            new_char = db.query(models.Character).filter(models.Character.id == new_char_id).first()
            if not new_char:
                raise ValueError("New Character id not found")
            other = db.query(models.SecretIdentity).filter(models.SecretIdentity.character_id == new_char_id).first()
            if other and other.id != identity_id:
                raise ValueError("New Character already has a SecretIdentity")

        for key, value in identity.dict().items():
            setattr(db_identity, key, value)
        db.commit()
        db.refresh(db_identity)
    return db_identity


def delete_identity(db: Session, identity_id: int):
    db_identity = get_identity(db, identity_id)
    if db_identity:
        db.delete(db_identity)
        db.commit()


def get_character_teams(db: Session):
    return db.query(models.CharacterTeam).all()


def create_character_team(db: Session, ct: schemas.CharacterTeamCreate):
    character = db.query(models.Character).filter(models.Character.id == ct.character_id).first()
    team = db.query(models.Team).filter(models.Team.id == ct.team_id).first()
    if not character or not team:
        raise ValueError("Character or Team not found")

    db_ct = models.CharacterTeam(**ct.dict())
    db.add(db_ct)
    db.commit()
    db.refresh(db_ct)
    return db_ct


def delete_character_team(db: Session, ct_id: int):
    db_ct = db.query(models.CharacterTeam).filter(models.CharacterTeam.id == ct_id).first()
    if db_ct:
        db.delete(db_ct)
        db.commit()