from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

from storage import load_players, add_player, update_player, delete_player

app = FastAPI(title="Foot Player API")

class PlayerCreate(BaseModel):
    name: str
    position: str
    age: int
    club: str

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[str] = None
    age: Optional[int] = None
    club: Optional[str] = None


@app.get("/players")
def get_players():
    return load_players()


@app.post("/players")
def create_player(player: PlayerCreate):
    new_player = {
        "id": str(uuid.uuid4()),
        "name": player.name,
        "position": player.position,
        "age": player.age,
        "club": player.club,
    }
    add_player(new_player)
    return new_player


@app.put("/players/{player_id}")
def edit_player(player_id: str, player: PlayerUpdate):
    updates = {k: v for k, v in player.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="Aucune donnée à modifier")
    update_player(player_id, updates)
    return {"status": "updated"}


@app.delete("/players/{player_id}")
def remove_player(player_id: str):
    delete_player(player_id)
    return {"status": "deleted"}