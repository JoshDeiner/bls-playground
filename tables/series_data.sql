CREATE TABLE series_data (
    id SERIAL PRIMARY KEY,
    series_id INT REFERENCES series(id),
    year VARCHAR(4),
    period VARCHAR(10),
    period_name VARCHAR(20),
    value DECIMAL(10, 3),
    footnotes JSONB
);
