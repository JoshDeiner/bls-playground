# service to insert or update series data


import logging

from sqlalchemy.orm import Session

# change names
from app.models.series import Calculations, Series, SeriesData

# make it work with data coming from the endpoint

# Todo ! then modurlaize functions
# make catalog_id dynamic


def upsert_series(payload, db: Session, catalog_id="SUUR0000SA0"):
    logging.info("init upsert")
    try:
        # series data insert
        logging.info("begin try block")

        # Extract the series part of the payload (catalog-level data)
        series_payload = payload.get("series", {})

        if not series_payload:
            logging.error("No series data found in the payload.")
            return

        # Check if series already exists based on catalog_id
        db_series = db.query(Series).filter(Series.catalog_id == catalog_id).first()
        logging.info("db query")

        # logging.info(f"series:{sesries}")
        # Check if series already exists
        db_series = db.query(Series).filter(catalog_id == Series.catalog_id).first()

        logging.info("db query")

        if not db_series:
            # Create a new series if it doesn't exist
            logging.info("No existing series found, creating new one.")

            db_series = Series(
                catalog_id=series_payload.get("catalog_id", 1),
                catalog_title=series_payload.get("catalog_title", 1),
                seasonality=series_payload.get("seasonality", 1),
                survey_name=series_payload.get("survey_name", 1),
                measure_data_type=series_payload.get("measure_data_type", 1),
                area=series_payload.get("area", 1),
                item=series_payload.get("item", 1),
            )
            db.add(db_series)

        else:
            logging.info(series_payload)

            # If series exists, compare and update fields that are different
            logging.info(f"Found existing series with catalog_id: {catalog_id}")
            updated_fields = False

            if db_series.catalog_title != series_payload.get("catalog_title"):
                db_series.catalog_title = series_payload.get("catalog_title", 1)
                updated_fields = True

            if db_series.seasonality != series_payload.get("seasonality"):
                db_series.seasonality = series_payload.get("seasonality", 1)
                updated_fields = True

            if db_series.survey_name != series_payload.get("survey_name"):
                db_series.survey_name = series_payload.get("survey_name", 1)
                updated_fields = True

            if db_series.measure_data_type != series_payload.get("measure_data_type"):
                db_series.measure_data_type = series_payload.get("measure_data_type", 1)
                updated_fields = True

            if db_series.area != series_payload.get("area"):
                db_series.area = series_payload.get("area", 1)
                updated_fields = True

            if db_series.item != series_payload.get("item"):
                db_series.item = series_payload.get("item", 1)
                updated_fields = True

            if updated_fields:
                logging.info(f"Updating series with catalog_id: {catalog_id}")
                db.commit()
                db.refresh(db_series)
            # Create a new series if it doesn't exist

        # Final save if series was newly created or updated
        db.commit()
        db.refresh(db_series)
        logging.info(f"Successfully inserted/updated series: {db_series.catalog_id}")

        # insert series data to series_data table

        series_data_list = payload.get("series_data", [])
        print(db_series.id)

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
                logging.info(
                    f"Inserted new series data for year {data_point.get('year')} and period {data_point.get('period')}."
                )
            else:
                # If the data exists, check if it has changed and update it if necessary
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

            if has_changes:
                db.commit()
                db.refresh(db_series_data)
                print(
                    f"Updated series data for year {data_point.get('year')} and period {data_point.get('period')}."
                )
            else:
                print(
                    f"No changes detected for year {data_point.get('year')} and period {data_point.get('period')}."
                )

        # calculations insert
        calc_payload = payload.get("calculations", [])
        print("calc", calc_payload)

        # Iterate over each calculation object in the list
        for calc_item in calc_payload:
            series_data_id = calc_item.get("series_data_id")
            pct_changes = calc_item.get("pct_changes", {})
            net_changes = calc_item.get("net_changes", {})

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
                db.commit()
                db.refresh(db_calculations)
                logging.info(
                    f"Inserted new calculations for series_data_id {series_data_id}."
                )
            else:
                if db_calculations.pct_changes != pct_changes:
                    db_calculations.pct_changes = pct_changes
                    has_changes = True

                if db_calculations.net_changes != net_changes:
                    db_calculations.net_changes = net_changes
                    has_changes = True

                if has_changes:
                    db.commit()
                    db.refresh(db_calculations)
                    logging.info(
                        f"Updated calculations for series_data_id {series_data_id}."
                    )
                else:
                    logging.info(
                        f"No changes detected for calculations for series_data_id {series_data_id}."
                    )

    except Exception as e:
        db.rollback()  # Rollback the session in case of errors
        print(f"Error inserting/updating series: {e}")
        raise e
