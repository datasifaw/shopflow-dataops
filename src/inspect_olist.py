
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

csv_files = sorted(DATA_DIR.glob("*.csv"))

print(f"Nombre de fichiers CSV : {len(csv_files)}")

for file in csv_files:
    df = pd.read_csv(file)

    print(f"\n--- {file.name} ---")
    print(f"Nombre de lignes : {df.shape[0]}")
    print(f"Nombre de colonnes : {df.shape[1]}")
    print(f"Colonnes : {', '.join(df.columns)}")
  