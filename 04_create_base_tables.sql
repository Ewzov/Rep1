CREATE TABLE IF NOT EXISTS public.base_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT,
    event_name_norm TEXT,
    event_date TEXT,
    year INTEGER,
    stage_type TEXT,
    city TEXT,
    source_page TEXT
);

CREATE TABLE IF NOT EXISTS public.base_regions (
    region_id TEXT PRIMARY KEY,
    region_name TEXT,
    region_name_norm TEXT,
    source_page TEXT
);