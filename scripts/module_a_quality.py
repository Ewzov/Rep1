from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs/module_a"
df = pd.read_csv(
    OUTPUT_DIR / "stg_fact_results_enriched.csv"
)

checks = []
def add_check(name, passed, details):
    checks.append({
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "details": details
    })

add_check(
    "Количество строк",
    len(df) == 11790,
    f"Найдено строк: {len(df)}"
)
duplicates = df["result_id"].duplicated().sum()
add_check(
    "Уникальность result_id",
    duplicates == 0,
    f"Дубликатов: {duplicates}"
)
required_columns = [
    "result_id",
    "event_name",
    "region_name",
    "competency_name"
]
missing = df[required_columns].isna().sum().sum()
add_check(
    "Заполнение обязательных полей",
    missing == 0,
    f"Пропусков: {missing}"
)
expected_weight = df["place"].map({
    1: 3,
    2: 2,
    3: 1
}).fillna(0)
weight_errors = (
    df["weight"] != expected_weight
).sum()
add_check(
    "Соответствие weight месту",
    weight_errors == 0,
    f"Ошибок: {weight_errors}"
)
expected_medal = (df["place"] <= 3).astype(int)
medal_errors = (
    df["is_medal"] != expected_medal
).sum()
add_check(
    "Соответствие is_medal месту",
    medal_errors == 0,
    f"Ошибок: {medal_errors}"
)
missing_links = (~df["html_link_found"]).sum()
add_check(
    "Наличие HTML-связей",
    missing_links == 0,
    f"Строк без связи: {missing_links}"
)
report = pd.DataFrame(checks)
print(report.to_string(index=False))

report.to_csv(
    OUTPUT_DIR / "quality_checks.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nОтчёт сохранён в quality_checks.csv")

if (report["status"] == "FAIL").any():
    print("\nВНИМАНИЕ: есть проверки, которые не пройдены!")
else:
    print("\nВсе проверки пройдены!")
