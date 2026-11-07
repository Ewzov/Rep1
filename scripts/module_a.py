from pathlib import Path
import re
import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA =  (
    ROOT
    / 'data/raw/contest/contest_bi_analyst_participant_final'
)
HTML_DIR = DATA / "module_a_html/competencies"
OUTPUT_DIR = ROOT / "outputs/module_a"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def normalize_text(text):
    if not text:
        return ""
    text = text.lower().replace('ё', 'е')
    text = re.sub(r'\s+', " ", text)
    return text.strip()

def parse_competency(html_path):
    html = html_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    def get_field(field_name):
        element = soup.select_one(
            f'[data-field="{field_name}"] dd'
        )
        if element:
            return element.get_text(" ", strip=True)
        return None

    title = soup.select_one("h1")
    description = soup.select_one(
        '[data-block="short_description"] .rich-text'
    )
    competency_name = (
        title.get_text(" ", strip=True)
        if title else None
    )
    short_description = (
        description.get_text(" ", strip=True)
        if description else None
    )

    return {
        'comp_id': get_field('comp_id'),
        'competency_name': competency_name,
        'competency_name_norm': normalize_text(
            competency_name
        ),
        'category': get_field('category'),
        'lead_region_name': get_field('lead_region_name'),
        'lead_region_name_norm': normalize_text(
            get_field('lead_region_name')
        ),
        'short_description': short_description,
        'status_text': get_field('status_text'),
        'comment_text': get_field('comment_text'),
        'source_page': html_path.relative_to(
            DATA / 'module_a_html'
        ).as_posix()
    }

html_files = sorted(
    path for path in HTML_DIR.glob("*.html")
    if path.name != 'registry.html'
)
print('Найдено HTML-карточек:', len(html_files))

competencies = []
for html_path in html_files:
    competency = parse_competency(html_path)
    competencies.append(competency)

df_competencies = pd.DataFrame(competencies)

print("\nРазмер таблицы:", df_competencies.shape)
print('Уникальных comp_id', df_competencies['comp_id'].nunique())
print('\nПропуски:')
print(df_competencies.isna().sum())
print('\nДубликаты comp_id:')
print(df_competencies['comp_id'].duplicated().sum())

output_file = OUTPUT_DIR / 'stg_competency_html.csv'

df_competencies.to_csv(
    output_file,
    index=False,
    encoding='utf-8'
)

print("\nФайлик сохранён:", output_file)