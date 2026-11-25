select 'events' as table_name, count(*) from rep1.raw_base_events
union all
select 'regions', count(*) from rep1.raw_base_regions
union all 
select 'results', count(*) from rep1.raw_base_fact_results
union all 
select 'news', count(*) from rep1.raw_base_news_text 
union all 
select 'competencies', count(*) from rep1.raw_base_competency_full 
union all 
select 'stages', count(*) from rep1.raw_ref_stage_type;


alter table rep1.stg_competency_event_link 
alter column event_name type text;

delete from rep1.stg_competency_event_link;


select 'stg_competency_html' as table_name,
	count(*) as row_count
from rep1.stg_competency_html
union all
select 'stg_competency_event_link',
	count(*)
from rep1.stg_competency_event_link;

select 
	count(*) as total_results,
	count(c.comp_id) as matched_competencies,
	count(*) - count(c.comp_id) as unmatched_competencies
from rep1.raw_base_fact_results f
left join rep1.stg_competency_html c
	on f.comp_id = c.comp_id;

INSERT INTO rep1.stg_fact_results_enriched
SELECT
    f.*,
    c.category,
    c.lead_region_name,
    c.short_description,
    c.status_text,
    c.comment_text,
    c.source_page,
    CASE
        WHEN c.comp_id IS NOT NULL THEN 'comp_id'
        ELSE 'no_html_match'
    END
FROM rep1.raw_base_fact_results f
LEFT JOIN rep1.stg_competency_html c
    ON f.comp_id = c.comp_id
ON CONFLICT (result_id) DO UPDATE SET
    category = EXCLUDED.category,
    lead_region_name = EXCLUDED.lead_region_name,
    short_description = EXCLUDED.short_description,
    status_text = EXCLUDED.status_text,
    comment_text = EXCLUDED.comment_text,
    html_source_page = EXCLUDED.html_source_page,
    match_method = EXCLUDED.match_method;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT result_id) AS unique_results,
    COUNT(*) FILTER (
        WHERE match_method = 'comp_id'
    ) AS matched,
    COUNT(*) FILTER (
        WHERE match_method = 'no_html_match'
    ) AS unmatched
FROM rep1.stg_fact_results_enriched;


-- 1. Количество результатов и уникальных ключей
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT result_id) AS unique_results
FROM rep1.stg_fact_results_enriched;


-- 2. Проверка обязательных ключей
SELECT
    COUNT(*) FILTER (WHERE result_id IS NULL) AS null_result_id,
    COUNT(*) FILTER (WHERE event_id IS NULL) AS null_event_id,
    COUNT(*) FILTER (WHERE comp_id IS NULL) AS null_comp_id,
    COUNT(*) FILTER (WHERE region_id IS NULL) AS null_region_id
FROM rep1.stg_fact_results_enriched;


-- 3. Проверка дублей результатов
SELECT result_id, COUNT(*) AS duplicate_count
FROM rep1.stg_fact_results_enriched
GROUP BY result_id
HAVING COUNT(*) > 1;


-- 4. Проверка дублей компетенций
SELECT comp_id, COUNT(*) AS duplicate_count
FROM rep1.stg_competency_html
GROUP BY comp_id
HAVING COUNT(*) > 1;


-- 5. Проверка дублей связей компетенция–событие
SELECT comp_id, event_id, COUNT(*) AS duplicate_count
FROM rep1.stg_competency_event_link
GROUP BY comp_id, event_id
HAVING COUNT(*) > 1;


-- 6. Проверка связей с событиями
SELECT COUNT(*) AS unmatched_events
FROM rep1.stg_fact_results_enriched f
LEFT JOIN rep1.raw_base_events e
    ON f.event_id = e.event_id
WHERE e.event_id IS NULL;


-- 7. Проверка связей с компетенциями
SELECT COUNT(*) AS unmatched_competencies
FROM rep1.stg_fact_results_enriched f
LEFT JOIN rep1.stg_competency_html c
    ON f.comp_id = c.comp_id
WHERE c.comp_id IS NULL;


-- 8. Проверка связей с регионами
SELECT COUNT(*) AS unmatched_regions
FROM rep1.stg_fact_results_enriched f
LEFT JOIN rep1.raw_base_regions r
    ON f.region_id = r.region_id
WHERE r.region_id IS NULL;


-- 9. Проверка связей компетенция–событие
SELECT COUNT(*) AS unmatched_links
FROM rep1.stg_competency_event_link l
LEFT JOIN rep1.raw_base_events e
    ON l.event_id = e.event_id
LEFT JOIN rep1.stg_competency_html c
    ON l.comp_id = c.comp_id
WHERE e.event_id IS NULL
   OR c.comp_id IS NULL;







