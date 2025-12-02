# routers/characters.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/characters", tags=["Characters"])

@router.post("/", response_model=schemas.Character)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_character(db, character)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Character])
def read_characters(db: Session = Depends(get_db)):
    return crud.get_characters(db)


@router.get("/{character_id}", response_model=schemas.Character)
def read_character(character_id: int, db: Session = Depends(get_db)):
    c = crud.get_character(db, character_id)
    if not c:
        raise HTTPException(status_code=404, detail="Character not found")
    return c


@router.put("/{character_id}", response_model=schemas.Character)
def update_character(character_id: int, character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    updated = crud.update_character(db, character_id, character)
    if not updated:
        raise HTTPException(status_code=404, detail="Character not found")
    return updated


@router.delete("/{character_id}")
def soft_delete_character(character_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_character(db, character_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"message": "Character soft-deleted"}


@router.put("/{character_id}/restore")
def restore_character(character_id: int, db: Session = Depends(get_db)):
    restored = crud.restore_character(db, character_id)
    if not restored:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"message": "Character restored"}
