from fastapi import FastAPI
from pydantic import BaseModel
import uuid

# 1. THE SIMPLEST APP POSSIBLE
app = FastAPI(title="Basic BBQ API (KISS Version)")

# 2. IN-MEMORY DATABASE (No SQLite, No Persistence)
grills = {}

class Grill(BaseModel):
    target_temp: int

@app.post("/grills")
def create_grill():
    new_id = str(uuid.uuid4())[:4]
    grills[new_id] = {"status": "OFF", "temp": 70}
    return {"id": new_id, "msg": "Simple Grill Created"}

@app.get("/grills/{g_id}")
def get_grill(g_id: str):
    return grills.get(g_id, {"error": "Not Found"})

@app.patch("/grills/{g_id}")
def update_grill(g_id: str, data: Grill):
    if g_id in grills:
        grills[g_id]["target_temp"] = data.target_temp
        grills[g_id]["status"] = "HEATING"
    return grills[g_id]

# RUN: uvicorn src.simple:app --reload
