# routers/identities.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/identities", tags=["Secret Identities"])

@router.post("/", response_model=schemas.SecretIdentity)
def create_identity(identity: schemas.SecretIdentityCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_identity(db, identity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[schemas.SecretIdentity])
def read_identities(db: Session = Depends(get_db)):
    return crud.get_identities(db)


@router.get("/{identity_id}", response_model=schemas.SecretIdentity)
def read_identity(identity_id: int, db: Session = Depends(get_db)):
    ident = crud.get_identity(db, identity_id)
    if not ident:
        raise HTTPException(status_code=404, detail="Identity not found")
    return ident


@router.put("/{identity_id}", response_model=schemas.SecretIdentity)
def update_identity(identity_id: int, identity: schemas.SecretIdentityCreate, db: Session = Depends(get_db)):
    try:
        updated = crud.update_identity(db, identity_id, identity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not updated:
        raise HTTPException(status_code=404, detail="Identity not found")
    return updated


@router.delete("/{identity_id}")
def delete_identity(identity_id: int, db: Session = Depends(get_db)):
    ident = crud.get_identity(db, identity_id)
    if not ident:
        raise HTTPException(status_code=404, detail="Identity not found")
    crud.delete_identity(db, identity_id)
    return {"message": "Identity deleted"}
