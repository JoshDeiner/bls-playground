from sqlalchemy.orm import Session


# change names
from app.models.series import Calculations, Series, SeriesData

import logging


# Function to insert or update series data

def upsert_series(payload, db: Session, catalog_id="SUUR0000SA0"):
    logging.info("init upsert")
    try:
        logging.info("begin try block")
        # logging.info(f"series:{sesries}")
        # Check if series already exists
        db_series = db.query(Series).filter(catalog_id == Series.catalog_id).first()

        # db_series = db.query(series).first()
        logging.info("db query")

        # print(f"Query result for series: {db_series}") 

        if not db_series:
            logging.info("no db_series")
            
            db_series = Series(
                catalog_id=payload.get("catalog_id", 1),
                catalog_title=payload.get('catalog_title', 1),
                seasonality=payload.get("seasonality", 1),
                survey_name=payload.get("survey_name", 1),
                measure_data_type=payload.get("measure_data_type", 1),
                area=payload.get("area", 1),
                item=payload.get("item", 1),
            )
            db.add(db_series)
            db.commit()
            db.refresh(db_series)
            logging.info(f"Successfully inserted series: {db_series.catalog_id}")
        else:
            print("Series already exists.")
    except Exception as e:
        db.rollback()  # Rollback the session in case of errors
        print(f"Error inserting/updating series: {e}")
        raise e

# def upsert_series(db: Session, series: SeriesRequest):
#     # Check if series already exists
#     db_series = db.query(Series).filter(Series.catalog_id == series.seriesID).first()

#     if not db_series:
#         # Create a new series if it doesn't exist
#         db_series = Series(
#             catalog_id=series.seriesID,
#             catalog_title=series.catalog.series_title,
#             seasonality=series.catalog.seasonality,
#             survey_name=series.catalog.survey_name,
#             measure_data_type=series.catalog.measure_data_type,
#             area=series.catalog.area,
#             item=series.catalog.item,
#         )
#         db.add(db_series)
#         db.commit()
#         db.refresh(db_series)
#         print(f"Successfully inserted series: {db_series.catalog_id}")
#     else:
#         print("Series already exists.")

    # Now insert or update the series data
    # for data_point in series.data:
    #     db_series_data = (
    #         db.query(SeriesData)
    #         .filter(
    #             SeriesData.series_id == db_series.id,
    #             SeriesData.year == data_point.year,
    #             SeriesData.period == data_point.period,
    #         )
    #         .first()
        # )

        # if not db_series_data:
        #     # Create new series data entry
        #     db_series_data = SeriesData(
        #         series_id=db_series.id,
        #         year=data_point.year,
        #         period=data_point.period,
        #         period_name=data_point.period_name,
        #         value=data_point.value,
        #     )
        #     db.add(db_series_data)
        #     db.commit()
        #     db.refresh(db_series_data)

        # Insert or update calculations
        # calculations = data_point.calculations
        # if calculations:
        #     db_calculations = (
        #         db.query(Calculations)
        #         .filter(Calculations.series_data_id == db_series_data.id)
        #         .first()
        #     )

        #     if not db_calculations:
        #         # Create new calculations entry
        #         db_calculations = Calculations(
        #             series_data_id=db_series_data.id,
        #             pct_changes=calculations.pct_changes,
        #             net_changes=calculations.net_changes,
        #         )
        #         db.add(db_calculations)
        #     else:
        #         # Update existing calculations
        #         db_calculations.pct_changes = calculations.pct_changes
        #         db_calculations.net_changes = calculations.net_changes
        #     db.commit()
