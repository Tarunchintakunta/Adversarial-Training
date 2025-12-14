import json

nb_path = '/Users/tarunchintakunta/Downloads/soukya/FINAL_COMPLETED.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

changed_cmap = False
changed_grid = 0

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        modified_cell = False
        
        # heuristic to check context
        full_source_text = "".join(source)
        is_comparison_cell = "Comparison of Baseline, PGD, and FGSM Models" in full_source_text
        
        for line in source:
            # 1. Update Confusion Matrix cmap
            if 'disp.plot(cmap="viridis")' in line:
                new_line = line.replace('disp.plot(cmap="viridis")', 'disp.plot(cmap="Blues")')
                new_source.append(new_line)
                changed_cmap = True
                modified_cell = True
            
            # 2. Update Model Comparison Grid
            elif 'ax.grid(True)' in line and is_comparison_cell:
                new_line = line.replace('ax.grid(True)', 'ax.grid(True, linestyle="--", alpha=0.7)')
                new_source.append(new_line)
                changed_grid += 1
                modified_cell = True
                
            else:
                new_source.append(line)
        
        if modified_cell:
            cell['source'] = new_source

print(f"Cmap updated: {changed_cmap}")
print(f"Grid updated instances: {changed_grid}")

if changed_cmap or changed_grid > 0:
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("Notebook saved.")
else:
    print("No changes made.")
