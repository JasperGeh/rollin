from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import random
from . import dice
from . import database as db

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/roll/artifact")
async def roll_artifact():
    # Example artifact roll
    artifacts = [
        {"name": "Blade of Dawn", "description": "A shimmering sword that glows at sunrise", "level_die": "1d10", "level_mod": 2},
        {"name": "Frost Rune", "description": "Ancient rune crackling with winter's power", "level_die": "1d6", "level_mod": 1},
        # Add more artifacts...
    ]
    
    artifact = random.choice(artifacts)
    rolled_level = dice.roll(artifact["level_die"]) + artifact["level_mod"]
    
    return {
        "name": artifact["name"],
        "description": artifact["description"],
        "level": rolled_level
    }