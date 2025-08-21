from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class MachineBase(BaseModel):
    name: str
    type: str
    ideal_cycle_time: float
    status: str = "stopped"

class MachineCreate(MachineBase):
    pass

class Machine(MachineBase):
    id: int
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class MachineDataBase(BaseModel):
    machine_id: int
    status: str
    current_consumption: Optional[float] = None
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    cycle_count: Optional[int] = None

class MachineDataCreate(MachineDataBase):
    pass

class MachineData(MachineDataBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ProductionDataBase(BaseModel):
    machine_id: int
    shift_date: str
    shift_number: int
    good_parts: int = 0
    defective_parts: int = 0
    target_count: int

class ProductionDataCreate(ProductionDataBase):
    pass

class ProductionData(ProductionDataBase):
    id: int
    operator_id: Optional[int] = None
    completed: bool = False
    
    class Config:
        from_attributes = True

class OEEData(BaseModel):
    machine_id: int
    availability: float = Field(..., ge=0, le=1)
    performance: float = Field(..., ge=0, le=1)
    quality: float = Field(..., ge=0, le=1)
    oee: float = Field(..., ge=0, le=1)
    timestamp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
