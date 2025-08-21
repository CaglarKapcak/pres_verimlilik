from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # press, welding, injection
    ideal_cycle_time = Column(Float, nullable=False)
    status = Column(String, default="stopped")
    last_maintenance = Column(DateTime, nullable=True)
    next_maintenance = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    data = relationship("MachineData", back_populates="machine")
    production_data = relationship("ProductionData", back_populates="machine")
    downtime_reasons = relationship("DowntimeReason", back_populates="machine")

class MachineData(Base):
    __tablename__ = "machine_data"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    current_consumption = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    cycle_count = Column(Integer, nullable=True)
    operator_id = Column(Integer, nullable=True)
    
    # Relationships
    machine = relationship("Machine", back_populates="data")

class ProductionData(Base):
    __tablename__ = "production_data"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"))
    shift_date = Column(String, nullable=False)
    shift_number = Column(Integer, nullable=False)
    good_parts = Column(Integer, default=0)
    defective_parts = Column(Integer, default=0)
    target_count = Column(Integer, nullable=False)
    operator_id = Column(Integer, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    machine = relationship("Machine", back_populates="production_data")

class DowntimeReason(Base):
    __tablename__ = "downtime_reasons"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"))
    reason = Column(String, nullable=False)
    category = Column(String, nullable=False)  # mechanical, electrical, operational
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Interval, nullable=True)
    operator_id = Column(Integer, nullable=True)
    resolved = Column(Boolean, default=False)
    
    # Relationships
    machine = relationship("Machine", back_populates="downtime_reasons")

class Operator(Base):
    __tablename__ = "operators"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="operator")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
