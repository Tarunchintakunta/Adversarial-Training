import json

file_path = '/Users/tarunchintakunta/Downloads/soukya/FINAL_COMPLETED_v1.ipynb'

def find_plots(path):
    with open(path, 'r', encoding='utf-8') as f:
        # Read lines to track line numbers manually since json.load doesn't give them
        lines = f.readlines()
    
    # Simple text scan to find lines
    print("Searching for plots...")
    for i, line in enumerate(lines):
        if ".plot(" in line or "df.plot" in line or "def plot_" in line:
             print(f"Line {i+1}: {line.strip()[:100]}...")
        if "history.history" in line and "plt" in line:
             print(f"Line {i+1} [History]: {line.strip()[:100]}...")

if __name__ == "__main__":
    find_plots(file_path)
