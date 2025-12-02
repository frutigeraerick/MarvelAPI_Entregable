from fastapi import FastAPI
import models
from database import engine
from routers import characters, teams, identities, character_team, report

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marvel API with Routers")

app.include_router(characters.router)
app.include_router(teams.router)
app.include_router(identities.router)
app.include_router(character_team.router)
app.include_router(report.router)