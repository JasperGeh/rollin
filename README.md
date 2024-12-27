# Rollin

A lightweight web app for TTRPG game masters to roll on custom tables and manage party inventory. Built with FastAPI and minimal JavaScript.

## Features

- Roll on various tables (artifacts, mishaps, etc.)
- Support for dice formulas (e.g., "1d6+2", "2d10-1")
- Linked table rolls (e.g., artifacts rolling quirks automatically)
- Simple party inventory management
- Persistent storage between sessions

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd rollin
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Open your browser to `http://127.0.0.1:8000`

## Project Structure

```
rollin/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── dice.py          # Dice rolling utilities
│
├── static/
│   └── js/
│       └── main.js      # Frontend JavaScript
│
├── templates/
│   └── index.html       # Main page template
│
├── test_artifacts.csv   # Sample artifact table
├── test_mishaps.csv     # Sample mishap table
├── test_quirks.csv      # Sample quirks table
├── party_inventory.json # Persistent inventory storage
├── requirements.txt
├── README.md
└── add_tables.md       # Guide for adding new tables
```

## Adding Custom Tables

See [add_tables.md](add_tables.md) for detailed instructions on how to add your own custom tables and item types.

## CSV File Format

Tables are stored as CSV files with at least these columns:
- `name` - Item name
- `description` - Item description (supports \n for linebreaks)

Optional columns:
- `level` - For dice rolls (e.g., "1d6+2")
- `severity` - For mishap intensity
- Other columns as needed

Example:
```csv
name,description,level
Moonweaver's Veil,A shimmering cloak.\nGrants stealth in darkness.,1d6+2
```

## Development

### Adding New Features

1. Add routes in `app/main.py`
2. Update templates in `templates/index.html`
3. Add new CSV files for additional tables

### Future Plans

- [ ] Table filtering and sorting
- [ ] Item categories/tags
- [ ] Item notes and editing
- [ ] Multiple party support
- [ ] Export/import functionality

## License

[Your chosen license]

## Contributing

[Your contribution guidelines]