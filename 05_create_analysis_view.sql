CREATE OR REPLACE VIEW public.vw_results_analysis AS
SELECT
    f.result_id,
    f.event_id,
    e.event_name,
    e.year,
    e.stage_type,

    f.comp_id,
    c.competency_name,
    c.category,

    f.region_id,
    r.region_name,

    f.place,
    f.is_medal,
    f.weight,
    f.cnt_people

FROM public.stg_fact_results_enriched f

LEFT JOIN public.base_events e
    ON f.event_id = e.event_id

LEFT JOIN public.base_regions r
    ON f.region_id = r.region_id

LEFT JOIN public.stg_competency_html c
    ON f.comp_id = c.comp_id;