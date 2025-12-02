from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/character_team", tags=["Character-Team Relation"])

@router.post("/", response_model=schemas.CharacterTeam)
def create_character_team(ct: schemas.CharacterTeamCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_character_team(db, ct)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[schemas.CharacterTeam])
def read_character_teams(db: Session = Depends(get_db)):
    return crud.get_character_teams(db)


@router.delete("/{ct_id}")
def delete_character_team(ct_id: int, db: Session = Depends(get_db)):
    crud.delete_character_team(db, ct_id)
    return {"message": "Character-Team relationship deleted"}