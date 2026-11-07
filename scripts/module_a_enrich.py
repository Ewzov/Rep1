from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = (
    ROOT
    / "data/raw/contest/contest_bi_analyst_participant_final"
    / "base_tables"
)
OUTPUT_DIR = ROOT / "outputs/module_a"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

facts = pd.read_csv(DATA / "base_fact_results.csv", dtype={
    "result_id": str,
    "event_id": str,
    "comp_id": str,
    "region_id": str
})
events = pd.read_csv(DATA / "base_events.csv", dtype={
    "event_id": str
})
regions = pd.read_csv(DATA / "base_regions.csv", dtype={
    "region_id": str
})
competencies = pd.read_csv(
    OUTPUT_DIR / "stg_competency_html.csv",
    dtype={"comp_id": str}
)
links = pd.read_csv(
    OUTPUT_DIR / "stg_competency_event_link.csv",
    dtype={"comp_id": str}
)

events = events.rename(columns={
    "source_page": "event_source_page"
})
regions = regions.rename(columns={
    "source_page": "region_source_page"
})
competencies = competencies.rename(columns={
    "source_page": "competency_source_page"
})

enriched = facts.merge(
    events,
    on="event_id",
    how="left",
    validate="many_to_one"
)

enriched = enriched.merge(
    regions,
    on="region_id",
    how="left",
    validate="many_to_one"
)

enriched = enriched.merge(
    competencies,
    on="comp_id",
    how="left",
    validate="many_to_one"
)

link_check = links[["comp_id", "event_source_page"]].drop_duplicates()
enriched = enriched.merge(
    link_check.assign(html_link_found=True),
    on=["comp_id", "event_source_page"],
    how="left",
    validate="many_to_one"
)
enriched["html_link_found"] = (
    enriched["html_link_found"].fillna(False)
)

print("Размер итоговой таблицы:", enriched.shape)
print("\nПропуски после объединения:")
print(
    enriched[
        ["event_name", "region_name", "competency_name"]
    ].isna().sum()
)
print("\nКоличество строк без HTML-связи:")
print((~enriched["html_link_found"]).sum())
print("\nКоличество дубликатов result_id:")
print(enriched["result_id"].duplicated().sum())

output_file = OUTPUT_DIR / "stg_fact_results_enriched.csv"

enriched.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nФайлик сохранён:", output_file)
