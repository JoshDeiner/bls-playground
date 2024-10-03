CREATE TABLE IF NOT EXISTS calculations (
    id SERIAL PRIMARY KEY,
    data_id INT REFERENCES series_data(id),
    pct_changes JSONB,
    net_changes JSONB
);
