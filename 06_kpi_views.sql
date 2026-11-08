-- 1. Общие KPI
CREATE OR REPLACE VIEW public.vw_kpi_overall AS
SELECT
    COUNT(*) AS total_results,
    SUM(is_medal) AS medal_count,
    ROUND(
        100.0 * SUM(is_medal)::numeric / NULLIF(COUNT(*), 0),
        2
    ) AS medal_share_pct,
    SUM(weight) AS weighted_score,
    COUNT(DISTINCT comp_id) AS competencies_count,
    COUNT(DISTINCT event_id) AS events_count
FROM public.vw_results_analysis;


-- 2. KPI по годам
CREATE OR REPLACE VIEW public.vw_kpi_by_year AS
SELECT
    year,
    COUNT(*) AS total_results,
    SUM(is_medal) AS medal_count,
    ROUND(
        100.0 * SUM(is_medal)::numeric / NULLIF(COUNT(*), 0),
        2
    ) AS medal_share_pct,
    SUM(weight) AS weighted_score,
    COUNT(DISTINCT comp_id) AS competencies_count
FROM public.vw_results_analysis
GROUP BY year;


-- 3. KPI по типам этапов
CREATE OR REPLACE VIEW public.vw_kpi_by_stage AS
SELECT
    stage_type,
    COUNT(*) AS total_results,
    SUM(is_medal) AS medal_count,
    ROUND(
        100.0 * SUM(is_medal)::numeric / NULLIF(COUNT(*), 0),
        2
    ) AS medal_share_pct,
    SUM(weight) AS weighted_score
FROM public.vw_results_analysis
GROUP BY stage_type;


-- 4. KPI по компетенциям
CREATE OR REPLACE VIEW public.vw_kpi_by_competency AS
SELECT
    comp_id,
    competency_name,
    category,
    COUNT(*) AS total_results,
    SUM(is_medal) AS medal_count,
    ROUND(
        100.0 * SUM(is_medal)::numeric / NULLIF(COUNT(*), 0),
        2
    ) AS medal_share_pct,
    SUM(weight) AS weighted_score,
    COUNT(DISTINCT event_id) AS events_count
FROM public.vw_results_analysis
GROUP BY comp_id, competency_name, category;


-- 5. KPI по регионам и другим организациям
CREATE OR REPLACE VIEW public.vw_kpi_by_region AS
SELECT
    region_id,
    region_name,
    COUNT(*) AS total_results,
    SUM(is_medal) AS medal_count,
    ROUND(
        100.0 * SUM(is_medal)::numeric / NULLIF(COUNT(*), 0),
        2
    ) AS medal_share_pct,
    SUM(weight) AS weighted_score,
    COUNT(DISTINCT comp_id) AS competencies_count
FROM public.vw_results_analysis
GROUP BY region_id, region_name;




CREATE OR REPLACE VIEW public.vw_kpi_by_category AS
SELECT
    category,
    COUNT(*) AS total_results,
    SUM(is_medal) AS medal_count,
    ROUND(
        100.0 * SUM(is_medal)::numeric / NULLIF(COUNT(*), 0),
        2
    ) AS medal_share_pct,
    SUM(weight) AS weighted_score,
    COUNT(DISTINCT comp_id) AS competencies_count
FROM public.vw_results_analysis
GROUP BY category;