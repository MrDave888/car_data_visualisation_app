from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Price(Base):
    __tablename__ = 'price'

    price_id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(String, ForeignKey('car_model.model_id'))
    year = Column(Integer)
    entry_level_price = Column(Numeric)

    car_model = relationship('CarModel', back_populates='prices')
