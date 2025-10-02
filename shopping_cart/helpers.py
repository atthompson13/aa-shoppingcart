import re

def parse_eve_items(text):
    """Parse items from EVE copy format"""
    items = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        match = re.match(r'(.+?)\s+x([\d,]+)', line)
        if match:
            name = match.group(1).strip()
            quantity = int(match.group(2).replace(',', ''))
            items.append({"name": name, "quantity": quantity})
            continue
        
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                name = parts[0].strip()
                try:
                    quantity = int(parts[1].replace(',', ''))
                    items.append({"name": name, "quantity": quantity})
                    continue
                except ValueError:
                    pass
        
        parts = line.rsplit(' ', 1)
        if len(parts) == 2:
            name = parts[0].strip()
            try:
                quantity = int(parts[1].replace(',', ''))
                items.append({"name": name, "quantity": quantity})
            except ValueError:
                pass
    
    return items

def format_isk(amount):
    if amount is None:
        return "0 ISK"
    return f"{amount:,} ISK"
