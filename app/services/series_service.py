from sqlalchemy.orm import Session

from app.models.series import Calculations, Series, SeriesData
from app.schemas.series import (CalculationsCreate, SeriesDataCreate,
                                SeriesRequest)


# Function to insert or update series data
def upsert_series(db: Session, series: SeriesRequest):
    # Check if series already exists
    db_series = db.query(Series).filter(Series.catalog_id == series.seriesID).first()

    if not db_series:
        # Create a new series if it doesn't exist
        db_series = Series(
            catalog_id=series.seriesID,
            catalog_title=series.catalog.series_title,
            seasonality=series.catalog.seasonality,
            survey_name=series.catalog.survey_name,
            measure_data_type=series.catalog.measure_data_type,
            area=series.catalog.area,
            item=series.catalog.item,
        )
        db.add(db_series)
        db.commit()
        db.refresh(db_series)

    # Now insert or update the series data
    for data_point in series.data:
        db_series_data = (
            db.query(SeriesData)
            .filter(
                SeriesData.series_id == db_series.id,
                SeriesData.year == data_point.year,
                SeriesData.period == data_point.period,
            )
            .first()
        )

        if not db_series_data:
            # Create new series data entry
            db_series_data = SeriesData(
                series_id=db_series.id,
                year=data_point.year,
                period=data_point.period,
                period_name=data_point.period_name,
                value=data_point.value,
            )
            db.add(db_series_data)
            db.commit()
            db.refresh(db_series_data)

        # Insert or update calculations
        calculations = data_point.calculations
        if calculations:
            db_calculations = (
                db.query(Calculations)
                .filter(Calculations.series_data_id == db_series_data.id)
                .first()
            )

            if not db_calculations:
                # Create new calculations entry
                db_calculations = Calculations(
                    series_data_id=db_series_data.id,
                    pct_changes=calculations.pct_changes,
                    net_changes=calculations.net_changes,
                )
                db.add(db_calculations)
            else:
                # Update existing calculations
                db_calculations.pct_changes = calculations.pct_changes
                db_calculations.net_changes = calculations.net_changes
            db.commit()
