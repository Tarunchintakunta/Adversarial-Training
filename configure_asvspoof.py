import json
import re

nb_path = '/Users/tarunchintakunta/Downloads/soukya/ASVspoof_ResNet_Reproduced.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Insert Drive Mount Cell
drive_mount_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {
        "id": "drive_mount_cell"
    },
    "outputs": [],
    "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')\n"
    ]
}

# Find index to insert - after "Setup and Imports" cell (which is likely index 2 based on previous read)
insert_index = 0
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and 'Setup and Imports' in "".join(cell['source']):
        insert_index = i + 2 # Insert after the imports code cell
        break

if insert_index == 0:
    insert_index = 3 # Fallback

nb['cells'].insert(insert_index, drive_mount_cell)
print(f"Inserted drive mount cell at index {insert_index}")


# 2. Update Paths & Remove Emojis
changed_paths = 0
removed_emojis = 0

emoji_pattern = re.compile(r'[^\w\s,.:;\'"()\[\]{}/*\-+=<>!@#$%^&|\\n\t\r]')

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        modified = False
        
        for line in source:
            original_line = line
            
            # Update root path
            if "root = Path('ASVspoof2019_root/LA').resolve()" in line:
                line = line.replace("root = Path('ASVspoof2019_root/LA').resolve()", 
                                  "root = Path('/content/drive/MyDrive/ASVspoof2019_root/LA').resolve()")
                changed_paths += 1
            
            # Remove emojis - simple replacement for known ones, or regex
            # Known ones from file view: ⚠️, ✓
            if "⚠️" in line:
                line = line.replace("⚠️", "!")
                removed_emojis += 1
            if "✓" in line:
                line = line.replace("✓", "")
                removed_emojis += 1
                
            if line != original_line:
                modified = True
            
            new_source.append(line)
        
        if modified:
            cell['source'] = new_source

print(f"Updated paths: {changed_paths}")
print(f"Removed emojis: {removed_emojis}")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("Notebook updated.")
