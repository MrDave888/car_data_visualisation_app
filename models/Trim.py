from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Trim(Base):
    __tablename__ = 'trim'

    trim_id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(String, ForeignKey('car_model.model_id'))
    trim_name = Column(String)
    year = Column(Integer)
    engine_type = Column(String)   # Fuel_type in CSV
    engine_size = Column(Integer)  # in cc, e.g. 1368
    selling_price = Column(Numeric)

    car_model = relationship('CarModel', back_populates='trims')
