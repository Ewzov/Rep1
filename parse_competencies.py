from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[1]

HTML_DIR = ROOT / "module_a_html" / "competencies"
EVENTS_CSV = ROOT / "base_tables" / "base_events.csv"

OUT_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def read_html(path):
    with open(path, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "lxml")

def normalize_name(value):
    value = str(value or "").lower().replace('ё', 'е')
    value = re.sub(r'[^\w]+', " ", value)
    return " ".join(value.split())

events = pd.read_csv(EVENTS_CSV, dtype=str).fillna("")
events["source_page"] = (
    events["source_page"].str.replace("\\", "/", regex=False).str.lstrip("./")
)

event_lookup = events.set_index("source_page")["event_id"].to_dict()


registry_path = HTML_DIR / "registry.html"
registry = read_html(registry_path)

competencies = []
links = []

registry_rows = registry.select(
    "#competency-registry tbody tr[data-comp-id]"
)

for row in registry_rows:
    comp_id = row.get("data-comp-id", "").strip()

    name_cell = row.select_one('[data-col="competency_name"]')
    category_cell = row.select_one('[data-col="category"]')
    region_cell = row.select_one('[data-col="lead_region_name"]')

    if not comp_id:
        continue

    card_link = name_cell.find("a") if name_cell else None
    if not card_link:
        continue

    card_path = HTML_DIR / card_link.get("href", "")
    if not card_path.exists():
        print(f"Не найдена карточка: {card_path}")
        continue

    card = read_html(card_path)

    def field_value(field):
        element = card.select_one(f'[data-field="{field}"] dd')
        return element.get_text(" ", strip=True) if element else ""

    description_block = card.select_one(
        '[data-block="short_description"] .rich-text'
    )
    short_description = (
        description_block.get_text(" ", strip=True)
        if description_block else ""
    )

    competencies.append({
        "comp_id": comp_id,
        "competency_name": (
            name_cell.get_text(" ", strip=True) if name_cell else ""
        ),
        "competency_name_norm": normalize_name(
            name_cell.get_text(" ", strip=True) if name_cell else ""
        ),
        "category": (
            category_cell.get_text(" ", strip=True) if category_cell else ""
        ),
        "lead_region_name": (
            region_cell.get_text(" ", strip=True) if region_cell else ""
        ),
        "short_description": short_description,
        "status_text": field_value("status_text"),
        "comment_text": field_value("comment_text"),
        "source_page": card_path.relative_to(ROOT).as_posix(),
    })

    for event_link in card.select(
        '[data-list="related_events"] a.event-ref'
    ):
        event_page = event_link.get("data-event-page", "").strip()
        event_page = event_page.replace("\\", "/").lstrip("./")

        links.append({
            "comp_id": comp_id,
            "event_id": event_lookup.get(event_page, ""),
            "event_page": event_page,
            "event_name": event_link.get("data-event-name", "").strip(),
        })


competencies_df = pd.DataFrame(competencies)
links_df = pd.DataFrame(links)

competencies_df.to_csv(
    OUT_DIR / "stg_competency_html.csv",
    index=False,
    encoding="utf-8-sig",
)

links_df.to_csv(
    OUT_DIR / "stg_competency_event_link.csv",
    index=False,
    encoding="utf-8-sig",
)

print("Парсинг завершён")
print("Компетенций:", len(competencies_df))
print("Связей с событиями:", len(links_df))
print("Не сопоставлено событий:", (links_df["event_id"] == "").sum())
print("Результаты сохранены в:", OUT_DIR)
