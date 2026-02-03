import asyncio
import httpx
import json
from src.database import get_db_connection
from src.config import log_system

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

async def generate_thought(status, current_temp, target_temp):
    """
    Sends telemetry to the Local LLM and retrieves a 'Pitmaster' observation.
    """
    prompt = f"""
    You are an expert BBQ Pitmaster AI controlling a smart smoker.
    
    TELEMETRY:
    - Status: {status}
    - Current Temp: {current_temp}°F
    - Target Temp: {target_temp}°F
    
    TASK:
    Write a ONE-SENTENCE internal thought explaining what you are doing to the fire.
    Use technical but rugged language (e.g., "Airflow", "Combustion", "Thermal Mass").
    DO NOT be chatty. Be precise.
    
    THOUGHT:
    """
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 40}
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_URL, json=payload, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "Systems Nominal.").strip().replace('"', '')
    except Exception as e:
        print(f"⚠️ CORTEX FAILURE: {e}")
        return "Neural Uplink Offline. Running Fallback Logic."

async def cortex_loop():
    """
    The High-Level Cognitive Loop.
    Runs every 10 seconds to update the 'latest_thought' based on Ollama's output.
    """
    log_system("🧠 CORTEX LOOP: INITIALIZED")
    await asyncio.sleep(5) # Let Physics warm up

    while True:
        conn = get_db_connection()
        grills = conn.execute("SELECT * FROM grills").fetchall()
        
        for g in grills:
            if g['status'] == "OFF":
                continue

            # 1. GENERATE NEW THOUGHT
            thought_text = await generate_thought(g['status'], g['current_temp'], g['target_temp'])
            
            # 2. READ EXISTING THOUGHT JSON
            try:
                current_data = json.loads(g['latest_thought'])
            except:
                current_data = {"reasoning": "Initializing..."}

            # 3. UPDATE REASONING FIELD ONLY
            current_data["reasoning"] = f"[AI] {thought_text}"
            
            # 4. COMMIT TO DB
            conn.execute("UPDATE grills SET latest_thought=? WHERE id=?", 
                         (json.dumps(current_data), g['id']))
            print(f"🧠 [AGENT:{g['id'][:4]}] {thought_text}")

        conn.commit()
        conn.close()
        
        # Think every 8 seconds (Prevent GPU Overload)
        await asyncio.sleep(8)
