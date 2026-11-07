
from pathlib import Path
import pandas as pd

ROOT = Path("data/raw")


def load_csv(file_path, rows=None):
    """Читает CSV. Если rows=None, загружает весь файл."""
    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return pd.read_csv(
                file_path,
                sep=None,
                engine="python",
                encoding=encoding,
                nrows=rows
            )
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue

    raise ValueError(f"Не удалось прочитать файл: {file_path}")


def inspect_table(df, table_name):
    """Универсальная проверка качества таблицы."""

    print("\n" + "=" * 60)
    print("ТАБЛИЦА:", table_name)
    print("=" * 60)

    print("\nРазмер (строки, столбцы):")
    print(df.shape)

    print("\nКоличество строк:")
    print(len(df))

    print("\nНазвания столбцов:")
    print(df.columns.tolist())

    print("\nТипы данных:")
    print(df.dtypes)

    print("\nПропуски:")
    print(df.isna().sum())

    print("\nПроцент пропусков:")
    print((df.isna().mean() * 100).round(2))

    print("\nПолные дубликаты:")
    print(df.duplicated().sum())

    print("\nКоличество уникальных значений в столбцах:")
    print(df.nunique(dropna=False))

    print("\nПервые три строки:")
    print(df.head(3))


# 1. Находим файлы
csv_files = list(ROOT.rglob("*.csv"))

print("Найдено CSV-файлов:", len(csv_files))

for file in csv_files:
    print(file.relative_to(ROOT))


# 2. Проверяем три основные таблицы
target_tables = [
    "base_events.csv",
    "base_regions.csv",
    "base_fact_results.csv"
]

tables = {}

for table_name in target_tables:
    matches = list(ROOT.rglob(table_name))

    if not matches:
        print(f"Файл не найден: {table_name}")
        continue

    # Если есть две версии набора, выбираем полную.
    final_matches = [
        p for p in matches
        if "participant_final" in str(p)
    ]

    file_path = final_matches[0] if final_matches else matches[0]

    print("\nВыбранный файл:", file_path)

    # Для разведки загружаем таблицу целиком.
    # Позже для больших файлов будем использовать выборочную загрузку.
    df = load_csv(file_path)

    tables[table_name] = df
    inspect_table(df, table_name)


# 3. Отдельно изучаем таблицу результатов
if "base_fact_results.csv" in tables:

    results = tables["base_fact_results.csv"]

    print("\n" + "=" * 60)
    print("АНАЛИЗ ТАБЛИЦЫ РЕЗУЛЬТАТОВ")
    print("=" * 60)

    print("\nКоличество записей:")
    print(len(results))

    print("\nСтолбцы таблицы результатов:")
    print(results.columns.tolist())

results = tables["base_fact_results.csv"]

check_columns = [
    "place",
    "is_medal",
    "weight",
    "cnt_people"
]

for column in check_columns:
    print(f"\n--- {column} ---")
    print(results[column].value_counts(dropna=False).head(20))

print("\nТипы данных:")
print(results.dtypes)

regions = tables["base_regions.csv"]

# Объединяем результаты со справочником регионов
results_with_regions = results.merge(
    regions[["region_id", "region_name"]],
    on="region_id",
    how="left"
)

print("Размер объединённой таблицы:")
print(results_with_regions.shape)

print("\nПервые строки:")
print(
    results_with_regions[
        ["result_id", "region_id", "region_name", "place"]
    ].head()
)

# Считаем количество записей по регионам
region_stats = (
    results_with_regions
    .groupby("region_name")
    .agg(
        results_count=("result_id", "count"),
        events_count=("event_id", "nunique"),
        competencies_count=("comp_id", "nunique")
    )
    .reset_index()
    .sort_values("results_count", ascending=False)
)

print("\nТоп-10 регионов по количеству записей:")
print(region_stats.head(10).to_string(index=False))

print(
    "Не найден регион:",
    results_with_regions["region_name"].isna().sum()
)

# Сопоставляем place и weight
print(pd.crosstab(results["place"], results["weight"]))

# Проверяем, совпадает ли признак медали с местом в тройке
print("\nСвязь is_medal и place:")
print(
    pd.crosstab(
        results["is_medal"],
        results["place"] <= 3
    )
)

# Проверяем предполагаемое правило weight
expected_weight = (4 - results["place"]).clip(lower=0, upper=3)

print(
    "\nКоличество несовпадений weight:",
    (results["weight"] != expected_weight).sum()
)

region_medals = (
    results_with_regions
    .groupby("region_name")
    .agg(
        results_count=("result_id", "count"),
        medals_count=("is_medal", "sum"),
        competencies_count=("comp_id", "nunique")
    )
    .reset_index()
)

region_medals["medal_share"] = (
    region_medals["medals_count"]
    / region_medals["results_count"]
    * 100
).round(2)

print(
    region_medals
    .sort_values("medal_share", ascending=False)
    .head(10)
    .to_string(index=False)
)


regions = tables["base_regions.csv"]

print("Все названия из справочника:")
for name in sorted(regions["region_name"].dropna().unique()):
    print(name)

print("\nКоличество уникальных названий:")
print(regions["region_name"].nunique())

print("\nКоличество пропусков:")
print(regions.isna().sum())

print("\nПримеры адресов источников:")
print(regions["source_page"].head(15).to_string(index=False))


region_stats = (
    results_with_regions
    .groupby(["region_id", "region_name"])
    .agg(
        results_count=("result_id", "count"),
        medals_count=("is_medal", "sum"),
        weighted_score=("weight", "sum"),
        competencies_count=("comp_id", "nunique"),
        events_count=("event_id", "nunique")
    )
    .reset_index()
)

region_stats["medal_share"] = (
    region_stats["medals_count"]
    / region_stats["results_count"]
    * 100
).round(2)

reliable_groups = region_stats[
    region_stats["results_count"] >= 20
]

print("\nТоп по количеству медальных результатов:")
print(
    reliable_groups
    .sort_values("medals_count", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\nТоп по взвешенному баллу:")
print(
    reliable_groups
    .sort_values("weighted_score", ascending=False)
    .head(10)
    .to_string(index=False)
)

import numpy as np

regions = tables["base_regions.csv"].copy()

# Признаки, характерные для субъектов РФ
pattern = (
    r"область|край|республика|"
    r"автономный округ|автономная область"
)

special_names = [
    "Москва",
    "Санкт-Петербург",
    "г. Севастополь"
]

regions["is_subject_candidate"] = (
    regions["region_name"].str.contains(
        pattern,
        case=False,
        na=False
    )
    | regions["region_name"].isin(special_names)
)

print("Кандидатов на субъекты РФ:")
print(regions["is_subject_candidate"].sum())

print("\nКандидаты:")
print(
    regions.loc[
        regions["is_subject_candidate"],
        "region_name"
    ].sort_values().to_string(index=False)
)

print("\nОстальные записи для проверки:")
print(
    regions.loc[
        ~regions["is_subject_candidate"],
        "region_name"
    ].sort_values().to_string(index=False)
)


subject_ids = regions.loc[
    regions["is_subject_candidate"],
    "region_id"
]

subject_stats = region_stats[
    region_stats["region_id"].isin(subject_ids)
].copy()

print("\nТоп-10 кандидатов по взвешенному баллу:")

print(
    subject_stats
    .sort_values("weighted_score", ascending=False)
    .head(10)
    .to_string(index=False)
)