import asyncio
import random
import json
import uuid
from datetime import datetime
from src.database import get_db_connection
# We assume src.config exists since you were running this before. 
# If not, we will handle that in the next turn.
from src.config import log_ai, log_system

class GrillAgent:
    """
    FIX: This class was missing, causing the ImportError in routes/grills.py.
    It generates the ID for new agents.
    """
    def __init__(self):
        self.id = f"g-{str(uuid.uuid4())[:4]}"

async def pid_physics_loop():
    """
    THE NEURAL PITMASTER
    Simulates an Autonomous Agent managing Thermodynamics.
    """
    log_system("🔥 PHYSICS ENGINE: RESTORED & IGNITED")
    # Wait for DB Bootstrap
    await asyncio.sleep(1)
    
    while True:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM grills")
            rows = cursor.fetchall()
        except Exception:
            await asyncio.sleep(1)
            continue
        
        for row in rows:
            g_id = row['id']
            status = row['status']
            curr = row['current_temp']
            target = row['target_temp']
            fan = row['fan_speed']
            auger = row['auger_rate']
            
            # 1. PERCEPTION
            thought_data = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "observation": f"Temp {curr}F | Target {target}F",
                "reasoning": "System Stable",
                "action": {"fan": fan, "auger": auger}
            }

            # 2. COGNITION (State Machine)
            if status == "OFF":
                if curr > 70: curr -= 1
                thought_data["reasoning"] = "System Idle. Ambient cooling active."

            elif status == "IGNITING":
                # Logic: Igniter forces temp to 160 before handing off
                target = 180
                fan = 50
                auger = 4
                
                if curr < 100: 
                    curr += random.randint(1, 3)
                    thought_data["reasoning"] = "Ignition Cycle: Rod heating. Awaiting combustion."
                else: 
                    curr += random.randint(5, 15)
                    thought_data["reasoning"] = "Ignition Cycle: FLAME DETECTED. Accelerating."
                
                if curr >= 160:
                    status = "SMOKING"
                    thought_data["reasoning"] = "Transition: Ignition Complete. Entering Smoke Mode."

            elif status in ["SMOKING", "SEARING", "HEATING"]:
                error = target - curr
                # PID Logic
                if error > 20:
                    auger = 8; fan = 80; curr += random.randint(3, 7)
                    thought_data["reasoning"] = f"Delta High ({error}F). MAX FUEL COMMANDED."
                elif error > 0:
                    auger = 2; fan = 40; curr += random.randint(0, 3)
                    thought_data["reasoning"] = "Delta Low. Maintenance burn."
                elif error < 0:
                    auger = 0; fan = 100; curr -= random.randint(1, 4)
                    thought_data["reasoning"] = "Overshoot Detected. Cutting Auger. Flushing Firepot."
                
                if random.random() > 0.85: 
                    curr -= 3
                    thought_data["reasoning"] += " [ALERT: External Thermal Loss Detected]"

            elif status == "SHUTDOWN":
                target = 0; auger = 0; fan = 100
                curr -= random.randint(2, 5)
                thought_data["reasoning"] = "Shutdown Mode. Auger Disabled. Fan purging ash."
                if curr < 150:
                    status = "OFF"
                    thought_data["reasoning"] = "Safe Temp Reached. System Halting."

            # 3. ACTION (Commit to DB)
            thought_json = json.dumps(thought_data)
            cursor.execute('''
                UPDATE grills SET 
                status=?, current_temp=?, fan_speed=?, auger_rate=?, latest_thought=?
                WHERE id=?
            ''', (status, curr, fan, auger, thought_json, g_id))
            
            # Log significant events
            if status != "OFF":
                # Only log occasionally to prevent spam, or handled by config
                pass 

        conn.commit()
        conn.close()
        await asyncio.sleep(1.0) # Real-time Hz
