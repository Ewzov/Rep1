# BI Competition - Module A
## Описание проекта
Проект посвящён подготовке данных для аналитической системы чемпионатов профессионального мастерства.
В модуле А выполнены:
- изучение исходных CSV и HTML-данных;
- извлечение сведений о компетенциях из HTML;
- извлечение связей «компетенция — мероприятие»;
- объединение результатов с данными мероприятий, регионов и компетенций;
- проверки качества данных;
- загрузка подготовленных таблиц в PostgreSQL.

## Структура проекта

```text
BI_Competition/
├── data/
│   └── raw/
│       └── contest/
│           └── contest_bi_analyst_participant_final/
│               ├── base_tables/
│               └── module_a_html/
├── scripts/
│   ├── lesson_01.py
│   ├── module_a.py
│   ├── module_a_links.py
│   ├── module_a_enrich.py
│   ├── module_a_quality.py
│   ├── module_a_schema.py
│   └── module_a_export.py
├── sql/
│   ├── 01_create_tables.sql
│   └── 03_quality_checks.sql
├── outputs/
│   └── module_a/
│       ├── postgres/
│       ├── quality_checks.csv
│       ├── stg_competency_html.csv
│       ├── stg_competency_event_link.csv
│       └── stg_fact_results_enriched.csv
├── docs/
│   └── model_description.md
└── README.md
```

## Используемые технологии

- Python
- pandas
- BeautifulSoup4
- PostgreSQL
- SQL
- DBeaver

## Установка зависимостей
Активировать виртуальное окружение и установить библиотеки:

```powershell
pip install pandas beautifulsoup4
```

## Порядок выполнения обработки
Запускать скрипты из корневой папки проекта:

```powershell
python scripts/module_a.py
python scripts/module_a_links.py
python scripts/module_a_enrich.py
python scripts/module_a_quality.py
python scripts/module_a_schema.py
python scripts/module_a_export.py
```

Скрипты выполняются последовательно: каждый следующий этап использует результаты предыдущего.

## Результаты обработки
| Таблица | Количество записей |
|---|---:|
| stg_competency_html | 318 |
| stg_competency_event_link | 916 |
| stg_fact_results_enriched | 11 790 |

## PostgreSQL
Подготовленные таблицы загружены в базу данных `prof`, схема `public`.
Создание таблиц выполняется скриптом:

```text
sql/01_create_tables.sql
```

Проверки после загрузки:

```text
sql/03_quality_checks.sql
```

## Проверки качества
Проверены:
- уникальность идентификаторов;
- отсутствие пропусков в обязательных полях;
- соответствие веса результата занятому месту;
- соответствие признака медали занятому месту;
- наличие HTML-связей;
- отсутствие дублирующихся связей;
- корректность объединения таблиц.

Все выполненные проверки пройдены.

## Безопасность
Учётные данные PostgreSQL не должны храниться в исходном коде или публиковаться в репозитории. В репозиторий не включаются виртуальное окружение `.venv`, временные файлы и лишние выгрузки.
