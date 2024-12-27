# Rollin 🎲

A lightweight web application for tabletop RPG game masters to roll on custom tables and manage party inventory. Built with FastAPI and vanilla JavaScript for simplicity and speed.

## Overview

Rollin helps Game Masters quickly generate random items, effects, and events from customizable tables. Perfect for systems like Numenera, D&D, or any tabletop RPG that uses random tables.

### Key Features

- **Table Rolling**: Roll on multiple custom tables (artifacts, cyphers, oddities, etc.)
- **Dice Support**: Full support for complex dice formulas (e.g., "2d6+3", "1d20-1")
- **Linked Tables**: Tables can trigger rolls on other tables (e.g., artifacts rolling for quirks)
- **Inventory Management**: Track party items with persistent storage
- **Customizable**: Easy to add new tables and modify existing ones
- **No Database Required**: Uses simple CSV files for tables and JSON for inventory

## Quick Start

1. **Clone and Setup**
```bash
git clone <your-repo-url>
cd rollin
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run the Application**
```bash
uvicorn app.main:app --reload
```

3. **Access the Interface**
- Open your browser to `http://127.0.0.1:8000`
- Start rolling on tables and managing inventory!

## Project Structure

```
rollin/
├── app/
│   ├── main.py          # FastAPI application & routes
│   └── dice.py          # Dice rolling utilities
├── static/
│   └── js/
│       └── main.js      # Frontend JavaScript
├── templates/
│   └── index.html       # Main interface template
├── tables/              # CSV table files
│   ├── artifacts.csv
│   ├── cyphers.csv
│   └── oddities.csv
└── party_inventory.json # Persistent storage
```

## Creating Custom Tables

1. **Create a CSV File**
- Required columns: `name`, `description`
- Optional columns: `level`, `severity`, `effect`, etc.
- Place in the `tables/` directory

Example table format:
```csv
name,description,level
Gravity Nullifier,A device that negates gravity in a 10' radius.,1d6+2
Phase Shifter,Allows passage through solid matter.,1d6+4
```

2. **Register the Table**
```python
@app.on_event("startup")
async def startup_event():
    tables['your_table'] = pd.read_csv("tables/your_table.csv")
```

3. **Add UI Button**
```html
<button onclick="rollOnTable('your_table')">Roll on Your Table</button>
```

For detailed instructions on creating custom tables, see [add_tables.md](add_tables.md).

## Development

### Requirements
- Python 3.7+
- FastAPI
- Pandas
- Uvicorn
- Jinja2

### Future Plans
- Table filtering and sorting
- Item categories and tags
- Multiple party support
- Import/export functionality
- Custom dice roll history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Choose an appropriate license]

---

For detailed documentation on adding custom tables and features, see [add_tables.md](add_tables.md).