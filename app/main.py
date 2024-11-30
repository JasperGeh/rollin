from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from . import dice

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global dictionary to store our tables
tables = {}

@app.on_event("startup")
async def startup_event():
    # Load all tables on startup
    tables['artifacts'] = pd.read_csv("test_artifacts.csv")
    tables['mishaps'] = pd.read_csv("test_mishaps.csv")
    tables['quirks'] = pd.read_csv("test_quirks.csv", header=0)
    print(tables['quirks'])

def roll_quirk():
    """Roll for a random quirk from the quirks table"""
    return tables['quirks'].sample(1).iloc[0]['quirk']

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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