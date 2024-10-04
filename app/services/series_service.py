from sqlalchemy.orm import Session


# change names
from app.models.series import Calculations, Series, SeriesData

import logging


# Function to insert or update series data



#### the question is no how should this function going forward
## should catalog_id be dynamic
## should this be modularized by insert to have a long function is you just use it once a month. you just
## need to ensure it works with data in it.

## potentially it's okay to 

# can this work with data already existing at any stage. what will happen then.

def upsert_series(payload, db: Session, catalog_id="SUUR0000SA0"):
    logging.info("init upsert")
    try:
        # series data insert
        logging.info("begin try block")
        series_payload = payload.get("series_data", 1)
        # logging.info(f"series:{sesries}")
        # Check if series already exists
        db_series = db.query(Series).filter(catalog_id == Series.catalog_id).first()

        # db_series = db.query(series).first()
        logging.info("db query")

        if not db_series:
            logging.info("no db_series")
            
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
            logging.info(f"Successfully inserted series: {db_series.catalog_id}")

        series_payload = payload.get("series_data", 1)

        # series data insert
        for data_point in series_payload:
#             # print("data_point", data_point, data_point.get("series_id", 1))
            db_series_data = (
                db.query(SeriesData)
                .filter(
                    SeriesData.series_id == data_point.get("series_id", 1),
                    SeriesData.year == data_point.get("year", 1),
                    SeriesData.period == data_point.get("period", 1),
                )
                .first()
            )

            if not db_series_data:
        #         # Create new series data entry
                db_series_data = SeriesData(
                    series_id=db_series.id,
                    year=data_point.get("year", 1),
                    period=data_point.get("period", 1),
                    period_name=data_point.get("period_name", 1),
                    value=data_point.get("value", 1),
                )
                db.add(db_series_data)
                db.commit()
                db.refresh(db_series_data)
            else:
                print("db series already created")


# calculations insert
        calc_payload = payload.get("calculations", [])
        print("calc", calc_payload)

        # Iterate over each calculation object in the list
        for calc_item in calc_payload:
            series_data_id = calc_item.get('series_data_id')
            pct_changes = calc_item.get('pct_changes', {})
            net_changes = calc_item.get('net_changes', {})

            # Query for existing calculations with matching series_data_id
            db_calculations = (
                db.query(Calculations)
                .filter(Calculations.series_data_id == series_data_id)
                .first()
            )
            print("db_calculations", db_calculations)

            if not db_calculations:
            # Create new calculations entry
                db_calculations = Calculations(
                    series_data_id=series_data_id,
                    pct_changes=pct_changes,
                    net_changes=net_changes,
                )
                db.add(db_calculations)
            else:
                # Update existing calculations
                db_calculations.pct_changes = pct_changes
                db_calculations.net_changes = net_changes

            db.commit()

        if calc_payload:
            logging.info("inside calc block")
            # db_calculations = (
            #     db.query(Calculations)
            #     .filter(Calculations.series_data_id == db_series_data.id)
            #     .first()
            # )
            print("db", db_calculations)

            if not db_calculations:
        #         # Create new calculations entry
                db_calculations = Calculations(
                    series_data_id=db_series_data.id,
                    pct_changes=calc_payload.get("pct_changes", 1),
                    net_changes=calculations.get("net_changes", 1),
                )
                db.add(db_calculations)
            else:
                # Update existing calculations
                db_calculations.pct_changes = calculations.pct_changes
                db_calculations.net_changes = calculations.net_changes
            db.commit()

    except Exception as e:
        db.rollback()  # Rollback the session in case of errors
        print(f"Error inserting/updating series: {e}")
        raise e

