from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.models.database import get_db
from app.models.schemas import ProductionData, ProductionDataCreate
from app.core.security import get_current_user

router = APIRouter()

@router.post("/production/", response_model=ProductionData)
async def create_production_record(
    production_data: ProductionDataCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_production = ProductionData(**production_data.dict())
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

@router.get("/production/", response_model=List[ProductionData])
async def get_production_records(
    machine_id: int = None,
    shift_date: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    query = db.query(ProductionData)
    
    if machine_id:
        query = query.filter(ProductionData.machine_id == machine_id)
    
    if shift_date:
        query = query.filter(ProductionData.shift_date == shift_date)
    
    production_data = query.offset(skip).limit(limit).all()
    return production_data

@router.get("/production/{production_id}", response_model=ProductionData)
async def get_production_record(
    production_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    production = db.query(ProductionData).filter(ProductionData.id == production_id).first()
    if not production:
        raise HTTPException(status_code=404, detail="Production record not found")
    return production

@router.put("/production/{production_id}", response_model=ProductionData)
async def update_production_record(
    production_id: int,
    production_data: ProductionDataCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_production = db.query(ProductionData).filter(ProductionData.id == production_id).first()
    if not db_production:
        raise HTTPException(status_code=404, detail="Production record not found")
    
    for key, value in production_data.dict().items():
        setattr(db_production, key, value)
    
    db.commit()
    db.refresh(db_production)
    return db_production

@router.delete("/production/{production_id}")
async def delete_production_record(
    production_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    production = db.query(ProductionData).filter(ProductionData.id == production_id).first()
    if not production:
        raise HTTPException(status_code=404, detail="Production record not found")
    
    db.delete(production)
    db.commit()
    return {"message": "Production record deleted successfully"}
