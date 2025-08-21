from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app.models.database import get_db
from app.services.oee_service import OEEService
from app.core.security import get_current_user

router = APIRouter()

@router.get("/reports/oee/daily")
async def get_daily_oee_report(
    machine_id: int,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format: YYYY-MM-DD")
    
    if (end_dt - start_dt).days > 31:
        raise HTTPException(status_code=400, detail="Date range cannot exceed 31 days")
    
    results = []
    current_date = start_dt
    
    while current_date <= end_dt:
        day_start = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0)
        day_end = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)
        
        oee_data = OEEService.calculate_oee(db, machine_id, day_start, day_end)
        
        results.append({
            "date": current_date.date().isoformat(),
            "availability": oee_data["availability"],
            "performance": oee_data["performance"],
            "quality": oee_data["quality"],
            "oee": oee_data["oee"]
        })
        
        current_date += timedelta(days=1)
    
    return results

@router.get("/reports/downtime")
async def get_downtime_report(
    machine_id: int = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    query = """
        SELECT category, 
               SUM(EXTRACT(EPOCH FROM duration)) as total_downtime_seconds,
               COUNT(*) as incident_count
        FROM downtime_reasons
        WHERE resolved = true
    """
    
    params = {}
    
    if machine_id:
        query += " AND machine_id = :machine_id"
        params["machine_id"] = machine_id
    
    if start_date and end_date:
        query += " AND start_time BETWEEN :start_date AND :end_date"
        params["start_date"] = start_date
        params["end_date"] = end_date
    
    query += " GROUP BY category ORDER BY total_downtime_seconds DESC"
    
    result = db.execute(query, params).fetchall()
    
    return [
        {
            "category": row[0],
            "total_downtime_hours": round(row[1] / 3600, 2),
            "incident_count": row[2]
        }
        for row in result
    ]

@router.get("/reports/production")
async def get_production_report(
    machine_id: int = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    query = """
        SELECT shift_date,
               SUM(good_parts) as total_good,
               SUM(defective_parts) as total_defective,
               SUM(good_parts + defective_parts) as total_produced,
               ROUND(SUM(good_parts) * 100.0 / NULLIF(SUM(good_parts + defective_parts), 0), 2) as quality_rate
        FROM production_data
        WHERE 1=1
    """
    
    params = {}
    
    if machine_id:
        query += " AND machine_id = :machine_id"
        params["machine_id"] = machine_id
    
    if start_date and end_date:
        query += " AND shift_date BETWEEN :start_date AND :end_date"
        params["start_date"] = start_date
        params["end_date"] = end_date
    
    query += " GROUP BY shift_date ORDER BY shift_date"
    
    result = db.execute(query, params).fetchall()
    
    return [
        {
            "date": row[0],
            "good_parts": row[1],
            "defective_parts": row[2],
            "total_parts": row[3],
            "quality_rate": row[4]
        }
        for row in result
    ]
