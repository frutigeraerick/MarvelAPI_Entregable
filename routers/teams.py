# routers/teams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_team(db, team)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    return crud.get_teams(db)


@router.get("/{team_id}", response_model=schemas.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    t = crud.get_team(db, team_id)
    if not t:
        raise HTTPException(status_code=404, detail="Team not found")
    return t


@router.put("/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    updated = crud.update_team(db, team_id, team)
    if not updated:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated


@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_team(db, team_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team soft-deleted"}

@router.put("/{team_id}/restore")
def restore_team(team_id: int, db: Session = Depends(get_db)):
    restored = crud.restore_team(db, team_id)
    if not restored:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team restored"}