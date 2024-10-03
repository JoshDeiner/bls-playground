CREATE TABLE IF NOT EXISTS series (
    id SERIAL PRIMARY KEY,
    series_id VARCHAR(50) UNIQUE,
    series_title TEXT,
    seasonality VARCHAR(100),
    survey_name VARCHAR(255),
    survey_abbreviation VARCHAR(10),
    measure_data_type VARCHAR(100),
    area VARCHAR(100),
    item VARCHAR(100)
);