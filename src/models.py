from pydantic import BaseModel
from typing import Optional, Dict, Any

class AgentThought(BaseModel):
    timestamp: str
    observation: str
    reasoning: str
    action: Dict[str, Any]

class Telemetry(BaseModel):
    current_temp_f: int
    target_temp_f: int
    fan_speed_pwm: int
    auger_rate: int

class Grill(BaseModel):
    id: str
    owner_id: str
    model: str
    status: str
    telemetry: Telemetry
    latest_thought: Optional[str] = None

class AuthRequest(BaseModel):
    username: str
    password: str

class GrillUpdate(BaseModel):
    target_temp_f: Optional[int] = None
    status: Optional[str] = None
