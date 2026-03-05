from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Advertisement(Base):
    __tablename__ = 'advertisement'

    ad_id = Column(String, primary_key=True)   # e.g. "10_1$$1"
    model_id = Column(String, ForeignKey('car_model.model_id'))
    ad_year = Column(Integer)
    ad_month = Column(Integer)
    color = Column(String)
    reg_year = Column(Integer)
    body_type = Column(String)
    mileage = Column(Integer)
    engine_size = Column(String)   # e.g. "6.8L" — stored as-is from the CSV
    gearbox = Column(String)
    fuel_type = Column(String)
    price = Column(Numeric)
    engine_power = Column(Integer)

    car_model = relationship('CarModel', back_populates='advertisements')
