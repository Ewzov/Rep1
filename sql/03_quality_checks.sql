-- 1. Проверяем количество строк во всех таблицах
SELECT 'stg_competency_html' AS table_name,
       COUNT(*) AS row_count
FROM public.stg_competency_html

UNION ALL

SELECT 'stg_competency_event_link',
       COUNT(*)
FROM public.stg_competency_event_link

UNION ALL

SELECT 'stg_fact_results_enriched',
       COUNT(*)
FROM public.stg_fact_results_enriched;


-- 2. Проверяем пропуски в обязательных полях результатов
SELECT
    COUNT(*) FILTER (WHERE result_id IS NULL) AS missing_result_id,
    COUNT(*) FILTER (WHERE event_id IS NULL) AS missing_event_id,
    COUNT(*) FILTER (WHERE comp_id IS NULL) AS missing_comp_id,
    COUNT(*) FILTER (WHERE region_id IS NULL) AS missing_region_id,
    COUNT(*) FILTER (WHERE match_method IS NULL) AS missing_match_method
FROM public.stg_fact_results_enriched;


-- 3. Проверяем логическую корректность weight
SELECT COUNT(*) AS weight_errors
FROM public.stg_fact_results_enriched
WHERE weight <> CASE
    WHEN place = 1 THEN 3
    WHEN place = 2 THEN 2
    WHEN place = 3 THEN 1
    ELSE 0
END;


-- 4. Проверяем соответствие is_medal месту
SELECT COUNT(*) AS medal_errors
FROM public.stg_fact_results_enriched
WHERE is_medal <> CASE
    WHEN place <= 3 THEN 1
    ELSE 0
END;


-- 5. Проверяем связи результатов с компетенциями и мероприятиями
SELECT COUNT(*) AS unmatched_results
FROM public.stg_fact_results_enriched f
LEFT JOIN public.stg_competency_event_link l
    ON f.comp_id = l.comp_id
   AND f.event_id = l.event_id
WHERE l.comp_id IS NULL;


-- 6. Смотрим распределение методов сопоставления
SELECT
    match_method,
    COUNT(*) AS row_count
FROM public.stg_fact_results_enriched
GROUP BY match_method;
