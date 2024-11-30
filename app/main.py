from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from . import dice
import json
from pathlib import Path

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global dictionary to store our tables and inventory
tables = {}
INVENTORY_FILE = "party_inventory.json"

def load_inventory():
    """Load inventory from JSON file, create if doesn't exist"""
    try:
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_inventory(inventory):
    """Save inventory to JSON file"""
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=2)

@app.on_event("startup")
async def startup_event():
    # Load all tables on startup
    tables['artifacts'] = pd.read_csv("test_artifacts.csv")
    tables['mishaps'] = pd.read_csv("test_mishaps.csv")
    tables['quirks'] = pd.read_csv("test_quirks.csv")
    
    # Ensure inventory file exists
    if not Path(INVENTORY_FILE).exists():
        save_inventory([])

def roll_quirk():
    """Roll for a random quirk from the quirks table"""
    return tables['quirks'].sample(1).iloc[0]['quirks']

@app.get("/")
async def read_root(request: Request):
    inventory = load_inventory()
    return templates.TemplateResponse("index.html", {"request": request, "inventory": inventory})

@app.get("/roll/{table_name}")
async def roll_on_table(table_name: str):
    if table_name not in tables:
        return {"error": f"Table {table_name} not found"}
    
    # Select random entry from the specified table
    entry = tables[table_name].sample(1).iloc[0]
    
    # Prepare the result
    result = {
        "name": entry['name'],
        "description": entry['description'],
    }
    
    # For artifacts, also roll a quirk
    if table_name == 'artifacts':
        result['quirk'] = roll_quirk()
    
    # Add rolled value if table has a dice column (either 'level' or 'severity')
    dice_column = 'level' if 'level' in entry else 'severity'
    if dice_column in entry:
        dice_formula = entry[dice_column]
        rolled_value = dice.roll(dice_formula)
        result[dice_column] = rolled_value
        result['dice_formula'] = dice_formula
    
    return result

@app.post("/inventory/add")
async def add_to_inventory(item: dict):
    inventory = load_inventory()
    inventory.append(item)
    save_inventory(inventory)
    return {"status": "success"}

@app.post("/inventory/remove/{index}")
async def remove_from_inventory(index: int):
    inventory = load_inventory()
    if 0 <= index < len(inventory):
        inventory.pop(index)
        save_inventory(inventory)
        return {"status": "success"}
    return {"status": "error", "message": "Invalid index"}

@app.get("/inventory")
async def get_inventory():
    return load_inventory()