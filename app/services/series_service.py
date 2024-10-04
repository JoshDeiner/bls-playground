# service to insert or update series data


from sqlalchemy.orm import Session

from app.models.series import Calculations, Series, SeriesData

import logging


# Insert or update a series
def upsert_series(series_payload, db: Session, catalog_id: str):
    logging.info("Upserting series with catalog_id: %s", catalog_id)
    
    db_series = db.query(Series).filter(Series.catalog_id == catalog_id).first()

    if not db_series:
        logging.info("No existing series found, creating new one.")
        db_series = Series(
            catalog_id=series_payload.get("catalog_id", 1),
            catalog_title=series_payload.get('catalog_title', 1),
            seasonality=series_payload.get("seasonality", 1),
            survey_name=series_payload.get("survey_name", 1),
            measure_data_type=series_payload.get("measure_data_type", 1),
            area=series_payload.get("area", 1),
            item=series_payload.get("item", 1),
        )
        db.add(db_series)
        db.commit()
        db.refresh(db_series)
        logging.info(f"Inserted new series with catalog_id: {catalog_id}")
    else:
        logging.info("Found existing series. Checking for updates.")
        updated_fields = update_series_fields(db_series, series_payload)
        if updated_fields:
            logging.info(f"Updating series with catalog_id: {catalog_id}")
            db.commit()
            db.refresh(db_series)

    return db_series

# Update fields of an existing series if they differ from payload
def update_series_fields(db_series, series_payload):
    updated_fields = False

    if db_series.catalog_title != series_payload.get("catalog_title"):
        db_series.catalog_title = series_payload.get("catalog_title")
        updated_fields = True

    if db_series.seasonality != series_payload.get("seasonality"):
        db_series.seasonality = series_payload.get("seasonality")
        updated_fields = True

    if db_series.survey_name != series_payload.get("survey_name"):
        db_series.survey_name = series_payload.get("survey_name")
        updated_fields = True

    if db_series.measure_data_type != series_payload.get("measure_data_type"):
        db_series.measure_data_type = series_payload.get("measure_data_type")
        updated_fields = True

    if db_series.area != series_payload.get("area"):
        db_series.area = series_payload.get("area")
        updated_fields = True

    if db_series.item != series_payload.get("item"):
        db_series.item = series_payload.get("item")
        updated_fields = True

    return updated_fields

# Insert or update series data
def upsert_series_data(series_data_list, db: Session, db_series):
    for data_point in series_data_list:
        db_series_data = (
            db.query(SeriesData)
            .filter(
                SeriesData.series_id == db_series.id,
                SeriesData.year == data_point.get("year", 1),
                SeriesData.period == data_point.get("period", 1),
            )
            .first()
        )

        if not db_series_data:
            db_series_data = SeriesData(
                series_id=db_series.id,
                year=data_point.get("year", 1),
                period=data_point.get("period", 1),
                period_name=data_point.get("period_name", 1),
                value=float(data_point.get("value", 1)),
            )
            db.add(db_series_data)
            db.commit()
            db.refresh(db_series_data)
            logging.info(f"Inserted new series data for year {data_point.get('year')} and period {data_point.get('period')}.")
        else:
            has_changes = update_series_data_fields(db_series_data, data_point)
            if has_changes:
                db.commit()
                db.refresh(db_series_data)
                logging.info(f"Updated series data for year {data_point.get('year')} and period {data_point.get('period')}.")

# Update series data fields if they differ from payload
def update_series_data_fields(db_series_data, data_point):
    has_changes = False

    if db_series_data.period_name != data_point.get("period_name"):
        db_series_data.period_name = data_point.get("period_name")
        has_changes = True

    if db_series_data.year != data_point.get("year"):
        db_series_data.year = data_point.get("year")
        has_changes = True

    if db_series_data.period != data_point.get("period"):
        db_series_data.period = data_point.get("period")
        has_changes = True

    if db_series_data.value != float(data_point.get("value", 1)):
        db_series_data.value = float(data_point.get("value", 1))
        has_changes = True

    return has_changes

# Insert or update calculations
def upsert_calculations(calc_payload, db: Session):
    for calc_item in calc_payload:
        series_data_id = calc_item.get('series_data_id')
        pct_changes = calc_item.get('pct_changes', {})
        net_changes = calc_item.get('net_changes', {})

        db_calculations = (
            db.query(Calculations)
            .filter(Calculations.series_data_id == series_data_id)
            .first()
        )

        if not db_calculations:
            db_calculations = Calculations(
                series_data_id=series_data_id,
                pct_changes=pct_changes,
                net_changes=net_changes,
            )
            db.add(db_calculations)
            db.commit()
            db.refresh(db_calculations)
            logging.info(f"Inserted new calculations for series_data_id {series_data_id}.")
        else:
            has_changes = update_calculations(db_calculations, pct_changes, net_changes)
            if has_changes:
                db.commit()
                db.refresh(db_calculations)
                logging.info(f"Updated calculations for series_data_id {series_data_id}.")

# Update calculation fields if they differ from payload
def update_calculations(db_calculations, pct_changes, net_changes):
    has_changes = False

    if db_calculations.pct_changes != pct_changes:
        db_calculations.pct_changes = pct_changes
        has_changes = True

    if db_calculations.net_changes != net_changes:
        db_calculations.net_changes = net_changes
        has_changes = True

    return has_changes

# Main function to orchestrate upsert for series, series data, and calculations
def upsert_series_payload(payload, db: Session, catalog_id: str):
    try:
        # Upsert the series
        db_series = upsert_series(payload.get("series", {}), db, catalog_id)

        # Upsert the series data
        upsert_series_data(payload.get("series_data", []), db, db_series)

        # Upsert calculations
        upsert_calculations(payload.get("calculations", []), db)

    except Exception as e:
        db.rollback()
        logging.error(f"Error inserting/updating series: {e}")
        raise e


