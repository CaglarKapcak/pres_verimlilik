from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.models.database import get_db
from app.models.schemas import Machine, MachineData, OEEData, MachineDataCreate
from app.services.oee_service import OEEService
from app.core.security import get_current_user

router = APIRouter()

@router.get("/machines/", response_model=List[Machine])
async def get_machines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    machines = db.query(Machine).offset(skip).limit(limit).all()
    return machines

@router.get("/machines/{machine_id}", response_model=Machine)
async def get_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.post("/machines/{machine_id}/data")
async def receive_machine_data(
    machine_id: int,
    data: MachineDataCreate,
    db: Session = Depends(get_db)
):
    machine_data = MachineData(**data.dict())
    db.add(machine_data)
    db.commit()
    db.refresh(machine_data)
    
    return {"message": "Data received successfully", "id": machine_data.id}

@router.get("/machines/{machine_id}/oee", response_model=OEEData)
async def get_machine_oee(
    machine_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    oee_data = OEEService.calculate_oee(db, machine_id, start_time, end_time)
    return OEEData(machine_id=machine_id, **oee_data)

@router.get("/machines/{machine_id}/realtime")
async def get_realtime_data(
    machine_id: int,
    hours: int = 1,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    data = db.query(MachineData).filter(
        MachineData.machine_id == machine_id,
        MachineData.timestamp.between(start_time, end_time)
    ).order_by(MachineData.timestamp.desc()).limit(100).all()
    
    return data
