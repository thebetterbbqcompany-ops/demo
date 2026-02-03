import asyncio
import json
from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from src.database import get_db_connection
from src.services.physics import GrillAgent

router = APIRouter()

@router.post("")
def spawn_agent():
    """
    Spawns a new autonomous agent (Grill).
    """
    agent = GrillAgent()
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO grills (id, status, current_temp, target_temp, latest_thought) VALUES (?, ?, ?, ?, ?)",
        (agent.id, "OFF", 70, 70, json.dumps({"reasoning": "System Initialized."}))
    )
    conn.commit()
    conn.close()
    
    print(f"🖥️  [SYSTEM]   🆕 NEW AGENT DEPLOYED: {agent.id}")
    return {"id": agent.id, "status": "OFF"}

@router.get("")
def list_grills():
    conn = get_db_connection()
    grills = conn.execute("SELECT * FROM grills").fetchall()
    conn.close()
    return {"active_agents": [dict(g) for g in grills]}

# --- THE MISSING LINK: GET SINGLE GRILL ---
@router.get("/{grill_id}")
def get_grill(grill_id: str):
    conn = get_db_connection()
    grill = conn.execute("SELECT * FROM grills WHERE id = ?", (grill_id,)).fetchone()
    conn.close()
    if not grill:
        raise HTTPException(status_code=404, detail="Grill not found")
    return dict(grill)
# ------------------------------------------

@router.patch("/{grill_id}")
def control_grill(grill_id: str, payload: dict):
    conn = get_db_connection()
    
    # 1. Update Target Temp
    if "target_temp" in payload:
        conn.execute("UPDATE grills SET target_temp = ?, status = 'HEATING' WHERE id = ?", 
                     (payload["target_temp"], grill_id))
    
    conn.commit()
    conn.close()
    return {"status": "Command Accepted", "target": payload.get("target_temp")}

@router.get("/{grill_id}/stream")
async def stream_grill(request: Request, grill_id: str):
    """
    Real-time Neural Uplink (SSE).
    """
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            conn = get_db_connection()
            data = conn.execute("SELECT * FROM grills WHERE id = ?", (grill_id,)).fetchone()
            conn.close()

            if data:
                # Parse the thought JSON safely
                try:
                    thought = json.loads(data['latest_thought'])
                except:
                    thought = {"reasoning": "Processing..."}

                yield {
                    "data": json.dumps({
                        "id": data['id'],
                        "temp": data['current_temp'],
                        "target": data['target_temp'],
                        "status": data['status'],
                        "thought": thought
                    })
                }
            
            await asyncio.sleep(1) # Stream Heartbeat (1Hz)

    return EventSourceResponse(event_generator())
