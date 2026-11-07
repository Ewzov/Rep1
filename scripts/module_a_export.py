from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = (
    ROOT
    / "data/raw/contest/contest_bi_analyst_participant_final"
    / "base_tables"
)
OUTPUT_DIR = ROOT / "outputs/module_a"
EXPORT_DIR = OUTPUT_DIR / "postgres"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

events = pd.read_csv(
    DATA / "base_events.csv",
    dtype={"event_id": str, "source_page": str}
)
links = pd.read_csv(
    OUTPUT_DIR / "stg_competency_event_link.csv",
    dtype={"comp_id": str}
)
facts = pd.read_csv(
    OUTPUT_DIR / "stg_fact_results_enriched.csv",
    dtype={
        "result_id": str,
        "event_id": str,
        "comp_id": str,
        "region_id": str
    }
)

event_lookup = events[
    ["event_id", "event_name_norm", "source_page"]
].rename(columns={
    "source_page": "event_source_page"
})

links_export = links.merge(
    event_lookup,
    on="event_source_page",
    how="left",
    validate="many_to_one"
)

links_export = links_export.rename(columns={
    "event_name": "event_name_html",
    "event_name_norm": "event_name_norm",
    "event_source_page": "event_page",
    "competency_source_page": "source_page"
})

links_export["match_method"] = "source_page_exact"

link_columns = [
    "comp_id",
    "event_id",
    "event_name_html",
    "event_name_norm",
    "event_page",
    "source_page",
    "match_method"
]

links_export = links_export[link_columns]

facts_export = facts.copy()

facts_export["html_source_page"] = (
    facts_export["competency_source_page"]
)
facts_export["match_method"] = (
    facts_export["html_link_found"].map({
        True: "source_page_exact",
        False: "no_html_match"
    })
)
fact_columns = [
    "result_id",
    "event_id",
    "comp_id",
    "region_id",
    "place",
    "is_medal",
    "weight",
    "cnt_people",
    "source_pages",
    "category",
    "lead_region_name",
    "short_description",
    "status_text",
    "comment_text",
    "html_source_page",
    "match_method"
]
facts_export = facts_export[fact_columns]

print("Связи компетенций и мероприятий:")
print("Строк:", len(links_export))
print("Пропуски event_id:", links_export["event_id"].isna().sum())
print("Дубликаты пар:", links_export.duplicated(
    subset=["comp_id", "event_id"]).sum())
print("\nОбогащённые результаты:")
print("Строк:", len(facts_export))
print("Столбцов:", len(facts_export.columns))
print("Дубликаты result_id:", facts_export["result_id"].duplicated().sum())
print("Пропуски event_id:", facts_export["event_id"].isna().sum())
print("Методы сопоставления:")
print(facts_export["match_method"].value_counts(dropna=False))

assert links_export["event_id"].notna().all(), (
    "Не для всех HTML-связей найден event_id"
)
assert links_export.duplicated(
    subset=["comp_id", "event_id"]
).sum() == 0, "Есть дубликаты связей"
assert facts_export["result_id"].is_unique, (
    "Есть дубликаты result_id"
)
assert facts_export["event_id"].notna().all()
assert facts_export["comp_id"].notna().all()
assert facts_export["region_id"].notna().all()
assert facts_export["match_method"].eq(
    "source_page_exact"
).all(), "Есть результаты без HTML-сопоставления"

links_export.to_csv(
    EXPORT_DIR / "stg_competency_event_link.csv",
    index=False,
    encoding="utf-8"
)
facts_export.to_csv(
    EXPORT_DIR / "stg_fact_results_enriched.csv",
    index=False,
    encoding="utf-8"
)
competencies = pd.read_csv(
    OUTPUT_DIR / "stg_competency_html.csv",
    dtype={"comp_id": str}
)
competencies.to_csv(
    EXPORT_DIR / "stg_competency_html.csv",
    index=False,
    encoding="utf-8"
)
print("\nЭкспорт завершён")
print("Файлики сохранены в:", EXPORT_DIR)
