from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Sales(Base):
    __tablename__ = 'sales'

    sales_id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(String, ForeignKey('car_model.model_id'))
    year = Column(Integer)
    units_sold = Column(Integer)
    region = Column(String)  # always 'UK' — dataset is UK/GB only

    car_model = relationship('CarModel', back_populates='sales')
