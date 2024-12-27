from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import json
import re
import random
from pathlib import Path

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global dictionary to store our tables and inventory
tables = {}
INVENTORY_FILE = "rollin_party_inventory.json"

def dice_roll(dice_str):
    # Try to convert input to integer first
    try:
        return int(dice_str)
    except (ValueError, TypeError):
        pass
    """Roll dice in standard notation (e.g., '1d6', '2d10', '1d6+2', '2d10-1')"""
    match = re.match(r'(\d+)d(\d+)([-+]\d+)?', dice_str)
    if not match:
        raise ValueError(f"Invalid dice notation: {dice_str}")
    num_dice = int(match.group(1))
    sides = int(match.group(2))
    modifier = match.group(3)
    results = [random.randint(1, sides) for _ in range(num_dice)]
    roll_total = sum(results)
    if modifier:
        # Convert the modifier string (e.g. '+2' or '-1') to an integer
        mod_value = int(modifier)
        roll_total += mod_value
    return roll_total
    #return (roll_total, results, modifier)

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
    tables['artifacts'] = pd.read_csv("tables/test_artifacts.csv")
    tables['numenera_artifact_quirks'] = pd.read_csv("tables/numenera_artifact_quirks.csv")
    tables['numenera_cypher'] = pd.read_csv("tables/numenera_cypher.csv")
    tables['numenera_oddities'] = pd.read_csv("tables/numenera_oddities.csv")
    tables['numenera_intrusions'] = pd.read_csv("tables/numenera_intrusions.csv")
    tables['numenera_weird'] = pd.read_csv("tables/numenera_weird.csv")
    # Ensure inventory file exists
    if not Path(INVENTORY_FILE).exists():
        save_inventory([])

def roll_quirk():
    """Roll for a random quirk from the quirks table"""
    return tables['numenera_artifact_quirks'].sample(1).iloc[0]['quirk']

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
    if table_name == 'numenera_cypher':
        result = {
            "no": "C-" + str(entry['no']),
            "name": entry['name'],
            "description": entry['description'],
            "effect": entry['effect'],
            "image": entry['image'],
            "source": entry['source']
        }
    elif table_name == 'numenera_artifacts':
        result = {
            "no": "A-" + str(entry['no']),
            "name": entry['name'],
            "description": entry['description'],
            "effect": entry['effect'],
            "image": entry['image'],
            "source": entry['source']
        }
    elif table_name == 'numenera_oddities':
        result = {
            "no": "O-" + str(entry['no']),
            "name": "Oddity",
            "description": entry['description'],
            "source": entry['source']
        }
    elif table_name == 'numenera_intrusions':
        result = {
            #"no": "I-" + str(entry['no']),
            "name": "Intrusion – " + entry['context'],
            "description": entry['intrusion'],
            #"context": entry['context'],
            "source": entry['source']
        }
    elif table_name == 'numenera_weird':
        result = {
            "name": "Weird – " + entry['context'],
            "description": entry['weird'],
            "source": entry['source']
        }
    else:
        result = {
            "name": entry['name'],
            "description": entry['description'],
        }
    
    # For artifacts, also roll a quirk
    if table_name == 'artifacts':
        if random.randint(1,6) == 1:
            result['quirk'] = roll_quirk()
    
    # Add rolled value if table has a dice column (either 'level' or 'severity')
    dice_column = 'level'
    if dice_column in entry:
        dice_formula = entry[dice_column]
        rolled_value = dice_roll(dice_formula)
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