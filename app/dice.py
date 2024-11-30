import re
import random

def roll(dice_str: str) -> int:
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

if __name__ == "__main__":
    print(roll("1d6"), roll("1d6+2"), roll("2d10-1"))