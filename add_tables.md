# Adding Tables to Rollin

## CSV File Structure

Each table needs its own CSV file with at least these basic columns:
- `name` - The name of the item
- `description` - The item's description (can include `\n` for linebreaks)

Optional columns:
- `level` - For artifacts (dice formula like "1d6+2")
- `severity` - For mishaps (dice formula like "1d10")
- Any other columns specific to your item type

## Adding New Tables

### 1. Create your CSV file
Create your CSV file in the project root directory (e.g., `test_monsters.csv`).

Example format:
```csv
name,description,challenge_rating
Dragon,"A massive red dragon.\nBreathes fire.",1d20+5
Goblin,"A sneaky little goblin.\nLoves shiny things.",1d6-1
```

### 2. Update main.py
In `app/main.py`, add your new table to the `startup_event`:
```python
@app.on_event("startup")
async def startup_event():
    tables['artifacts'] = pd.read_csv("test_artifacts.csv")
    tables['mishaps'] = pd.read_csv("test_mishaps.csv")
    tables['quirks'] = pd.read_csv("test_quirks.csv")
    tables['monsters'] = pd.read_csv("test_monsters.csv")  # Add your new table
```

### 3. Update the HTML
In `templates/index.html`, add a new button for your table:
```html
<div class="buttons">
    <button onclick="rollOnTable('artifacts')">Roll Random Artifact</button>
    <button onclick="rollOnTable('mishaps')">Roll Mishap</button>
    <button onclick="rollOnTable('monsters')">Roll Monster</button>  <!-- New button -->
</div>
```

### 4. Handle Special Properties
If your table needs special handling (like how artifacts get quirks), update the roll_on_table endpoint in `main.py`:

```python
@app.get("/roll/{table_name}")
async def roll_on_table(table_name: str):
    # ... existing code ...
    
    # For artifacts, also roll a quirk
    if table_name == 'artifacts':
        result['quirk'] = roll_quirk()
    elif table_name == 'monsters':  # Add special handling for your table
        result['special_trait'] = roll_special_trait()
    
    # Add rolled value if table has a dice column
    dice_column = 'level' if 'level' in entry else 'severity'
    if table_name == 'monsters':  # Handle custom dice columns
        dice_column = 'challenge_rating'
```

### 5. Update Inventory Display
If your new items have special properties to display, update the inventory item template in `index.html`:

```javascript
`<div class="inventory-item">
    <div class="flex">
        <h3>${item.name}</h3>
        <button onclick="removeFromInventory(${index})" class="small remove">Remove</button>
    </div>
    <p class="description">${item.description}</p>
    ${item.quirk ? `<p class="quirk">Quirk: ${item.quirk}</p>` : ''}
    ${item.level ? `<p class="value">Level: ${item.level}</p>` : ''}
    ${item.severity ? `<p class="value">Severity: ${item.severity}</p>` : ''}
    ${item.challenge_rating ? `<p class="value">CR: ${item.challenge_rating}</p>` : ''}
    ${item.special_trait ? `<p class="special">Special: ${item.special_trait}</p>` : ''}
</div>`
```

## Linked Tables

For tables that need to roll on other tables (like how artifacts roll on the quirks table):

1. Create your linked table CSV (like `test_special_traits.csv`)
2. Add it to `startup_event` in `main.py`
3. Create a roll function:
```python
def roll_special_trait():
    """Roll for a random special trait"""
    return tables['special_traits'].sample(1).iloc[0]['trait']
```
4. Use it in your roll_on_table function where needed
