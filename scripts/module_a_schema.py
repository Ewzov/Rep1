from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs/module_a"

files = [
    "stg_competency_html.csv",
    "stg_competency_event_link.csv",
    "stg_fact_results_enriched.csv"
]

for file_name in files:
    path = OUTPUT_DIR / file_name
    df = pd.read_csv(path, nrows=5)
    print("ФАЙЛ:", file_name)

    for column, dtype in df.dtypes.items():
        print(f"{column:35} {dtype}")
