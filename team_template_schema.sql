CREATE SCHEMA IF NOT EXISTS rep1;

-- Base raw layer: files from base_tables/
CREATE TABLE IF NOT EXISTS rep1.raw_base_events (
    event_id text PRIMARY KEY,
    event_name text NOT NULL,
    event_name_norm text NOT NULL,
    event_date date,
    year integer,
    stage_type text,
    city text,
    source_page text
);

CREATE TABLE IF NOT EXISTS rep1.raw_base_regions (
    region_id text PRIMARY KEY,
    region_name text NOT NULL,
    region_name_norm text NOT NULL,
    source_page text
);

CREATE TABLE IF NOT EXISTS rep1.raw_base_fact_results (
    result_id text PRIMARY KEY,
    event_id text NOT NULL,
    comp_id text NOT NULL,
    region_id text NOT NULL,
    place integer,
    is_medal integer,
    weight integer,
    cnt_people integer,
    source_pages text
);

CREATE TABLE IF NOT EXISTS rep1.raw_base_news_text (
    news_id text PRIMARY KEY,
    event_id text,
    event_name text,
    news_title text,
    summary_text text,
    status_text text,
    source_page text
);

CREATE TABLE IF NOT EXISTS rep1.raw_base_competency_full (
    comp_id text primary key,
    competency_name text,
    category text,
    lead_text text,
    description_text text,
    task_text text,
    criteria_text text,
    status_text text, 
    comment_text text,
    full_text text,
    full_text_chars integer,
    keywords text, 
    source_page text
);

CREATE TABLE IF NOT EXISTS rep1.raw_ref_stage_type (
    stage_type_code text PRIMARY KEY,
    stage_type_name text NOT NULL,
    stage_group text NOT NULL,
    sort_order integer NOT NULL
);

-- Module A outputs after HTML parsing and matching
CREATE TABLE IF NOT EXISTS rep1.stg_competency_html (
    comp_id text PRIMARY KEY,
    competency_name text NOT NULL,
    competency_name_norm text NOT NULL,
    category text,
    lead_region_name text,
    lead_region_name_norm text,
    short_description text,
    status_text text,
    comment_text text,
    source_page text
);

CREATE TABLE IF NOT EXISTS rep1.stg_competency_event_link (
    comp_id text NOT NULL,
    event_id text,
    event_name_html text,
    event_name_norm text,
    event_page text,
    source_page text,
    match_method text
);

CREATE TABLE IF NOT EXISTS rep1.stg_fact_results_enriched (
    result_id text PRIMARY KEY,
    event_id text NOT NULL,
    comp_id text NOT NULL,
    region_id text NOT NULL,
    place integer,
    is_medal integer,
    weight integer,
    cnt_people integer,
    source_pages text,
    category text,
    lead_region_name text,
    short_description text,
    status_text text,
    comment_text text,
    html_source_page text,
    match_method text
);

CREATE INDEX IF NOT EXISTS idx_raw_base_fact_results_event ON rep1.raw_base_fact_results (event_id);
CREATE INDEX IF NOT EXISTS idx_raw_base_fact_results_comp ON rep1.raw_base_fact_results (comp_id);
CREATE INDEX IF NOT EXISTS idx_raw_base_fact_results_region ON rep1.raw_base_fact_results (region_id);
CREATE INDEX IF NOT EXISTS idx_stg_competency_html_norm ON rep1.stg_competency_html (competency_name_norm);
CREATE INDEX IF NOT EXISTS idx_stg_competency_event_link_comp ON rep1.stg_competency_event_link (comp_id);
CREATE INDEX IF NOT EXISTS idx_stg_competency_event_link_event ON rep1.stg_competency_event_link (event_id);
