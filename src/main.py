import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db
from src.services.physics import pid_physics_loop
from src.services.cortex import cortex_loop
from src.routes import auth, grills

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "="*60)
    print("   🥩 BETTER BBQ API v2 // NEURAL PITMASTER EDITION")
    print("   🤖 VOICE: LOCAL LLAMA 3.2 // CORTEX: ONLINE")
    print("="*60 + "\n")
    
    # 1. Initialize Database
    init_db()
    
    # 2. Ignite Physics Engine (The Body)
    asyncio.create_task(pid_physics_loop())

    # 3. Ignite Cortex Engine (The Mind)
    asyncio.create_task(cortex_loop())
    
    yield
    print("⚠️  SYSTEM SHUTDOWN INITIATED")

app = FastAPI(lifespan=lifespan, title="Better BBQ Neural Controller")

# --- CORS: ALLOW POSTMAN VISUALIZER ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THE SWAGGER LOBBY ---
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Route Registration
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(grills.router, prefix="/grills", tags=["Grills"])

if __name__ == "__main__":
    import uvicorn
    # HOST 0.0.0.0 is MANDATORY for Distrobox
    uvicorn.run(app, host="0.0.0.0", port=8000)
