-- 1. Таблица компетенций, извлечённых из HTML
CREATE TABLE IF NOT EXISTS public.stg_competency_html (
    comp_id TEXT PRIMARY KEY,
    competency_name TEXT,
    competency_name_norm TEXT,
    category TEXT,
    lead_region_name TEXT,
    lead_region_name_norm TEXT,
    short_description TEXT,
    status_text TEXT,
    comment_text TEXT,
    source_page TEXT
);

-- 2. Связи компетенций и мероприятий
CREATE TABLE IF NOT EXISTS public.stg_competency_event_link (
    comp_id TEXT,
    event_id TEXT,
    event_name_html TEXT,
    event_name_norm TEXT,
    event_page TEXT,
    source_page TEXT,
    match_method TEXT,
    PRIMARY KEY (comp_id, event_id)
);

-- 3. Обогащённые результаты
CREATE TABLE IF NOT EXISTS public.stg_fact_results_enriched (
    result_id TEXT PRIMARY KEY,
    event_id TEXT,
    comp_id TEXT,
    region_id TEXT,
    place INTEGER,
    is_medal INTEGER,
    weight INTEGER,
    cnt_people INTEGER,
    source_pages TEXT,
    category TEXT,
    lead_region_name TEXT,
    short_description TEXT,
    status_text TEXT,
    comment_text TEXT,
    html_source_page TEXT,
    match_method TEXT
);
