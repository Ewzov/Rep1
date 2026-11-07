from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = (
    ROOT
    / "data/raw/contest/contest_bi_analyst_participant_final"
)
HTML_ROOT = DATA / "module_a_html"
OUTPUT_DIR = ROOT / "outputs/module_a"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

competencies = pd.read_csv(
    OUTPUT_DIR / "stg_competency_html.csv",
    dtype={"comp_id": "string"}
)

links = []
for _, row in competencies.iterrows():
    html_path = HTML_ROOT / row["source_page"]
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    event_elements = soup.select("a[data-event-page]")
    for element in event_elements:
        event_page = element.get("data-event-page")
        event_name = element.get("data-event-name")
        links.append({
            "comp_id": row["comp_id"],
            "event_source_page": event_page,
            "event_name": event_name,
            "competency_source_page": row["source_page"]
        })

df_links = pd.DataFrame(links)

print("Количество связей:", len(df_links))
print(
    "Уникальных пар компетенция-мероприятие:",
    df_links[
        ["comp_id", "event_source_page"]
    ].drop_duplicates().shape[0]
)
print(
    "Пропуски:",
    df_links.isna().sum()
)
print(
    "Дубликаты пар:",
    df_links.duplicated(
        subset=["comp_id", "event_source_page"]
    ).sum()
)

output_file = OUTPUT_DIR / "stg_competency_event_link.csv"
df_links.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)
print("\nФайлик сохранён:", output_file)