from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


# Series table definition
class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(String, unique=True, index=True)
    catalog_title = Column(String)
    seasonality = Column(String)
    survey_name = Column(String)
    measure_data_type = Column(String)
    area = Column(String)
    item = Column(String)

    # Relationship to SeriesData
    series_data = relationship("SeriesData", back_populates="series")

    # Add the __repr__ method
    def __repr__(self):
        return f"<Series(id={self.id}, catalog_id={self.catalog_id}, catalog_title={self.catalog_title})>"


# SeriesData table definition
class SeriesData(Base):
    __tablename__ = "series_data"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("series.id"))
    year = Column(String)
    period = Column(String)
    period_name = Column(String)
    value = Column(Float)

    # Relationship back to Series
    series = relationship("Series", back_populates="series_data")

    # Relationship to Calculations
    calculations = relationship(
        "Calculations", back_populates="series_data", uselist=False
    )


# Calculations table definition
class Calculations(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    series_data_id = Column(Integer, ForeignKey("series_data.id"))

    # Storing the percentage changes and net changes as JSON
    pct_changes = Column(JSON)  # A JSON field for percentage changes
    net_changes = Column(JSON)  # A JSON field for net changes

    # Relationship back to SeriesData
    series_data = relationship("SeriesData", back_populates="calculations")
