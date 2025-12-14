import json
import os

file_path = '/Users/tarunchintakunta/Downloads/soukya/FINAL_COMPLETED_v1.ipynb'

def update_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    style_added = False
    cm_replaced_count = 0

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            new_source = []
            for line in source:
                # Add global style after first plt import
                if "import matplotlib.pyplot as plt" in line and not style_added:
                    new_source.append(line)
                    # Add style command
                    # Ensure formatting (newlines)
                    if line.endswith('\n'):
                        new_source.append("plt.style.use('seaborn-v0_8-whitegrid')\n")
                    else:
                        new_source.append("\nplt.style.use('seaborn-v0_8-whitegrid')")
                    style_added = True
                    continue
                
                # Replace cmap
                if 'disp.plot(cmap="Blues")' in line:
                    new_line = line.replace('cmap="Blues"', 'cmap="YlOrBr"')
                    new_source.append(new_line)
                    cm_replaced_count += 1
                elif "disp.plot(cmap='Blues')" in line:
                     new_line = line.replace("cmap='Blues'", "cmap='YlOrBr'")
                     new_source.append(new_line)
                     cm_replaced_count += 1
                else:
                    new_source.append(line)
            
            cell['source'] = new_source

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)

    print(f"Notebook updated. Style added: {style_added}. CM replaced: {cm_replaced_count}")

if __name__ == "__main__":
    if os.path.exists(file_path):
        update_notebook(file_path)
    else:
        print(f"File not found: {file_path}")
