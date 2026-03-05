from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base import Base


class CarModel(Base):
    __tablename__ = 'car_model'

    model_id = Column(String, primary_key=True)  # e.g. "2_1"
    brand_name = Column(String)
    model_name = Column(String)

    trims = relationship('Trim', back_populates='car_model')
    prices = relationship('Price', back_populates='car_model')
    sales = relationship('Sales', back_populates='car_model')
    advertisements = relationship('Advertisement', back_populates='car_model')
