import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class DataLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()
    
    def load_machine_data(self, machine_id: int, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Makine verilerini yükle"""
        query = text("""
            SELECT timestamp, status, current_consumption, temperature, cycle_count
            FROM machine_data
            WHERE machine_id = :machine_id
            AND timestamp BETWEEN :start_date AND :end_date
            ORDER BY timestamp
        """)
        
        params = {
            'machine_id': machine_id,
            'start_date': start_date,
            'end_date': end_date
        }
        
        return pd.read_sql(query, self.connection, params=params)
    
    def load_production_data(self, machine_id: Optional[int] = None, 
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Üretim verilerini yükle"""
        query = """
            SELECT p.*, m.name as machine_name
            FROM production_data p
            JOIN machines m ON p.machine_id = m.id
            WHERE 1=1
        """
        
        params = {}
        
        if machine_id:
            query += " AND p.machine_id = :machine_id"
            params['machine_id'] = machine_id
        
        if start_date:
            query += " AND p.shift_date >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            query += " AND p.shift_date <= :end_date"
            params['end_date'] = end_date
        
        query += " ORDER BY p.shift_date, p.shift_number"
        
        return pd.read_sql(text(query), self.connection, params=params)
    
    def load_downtime_data(self, machine_id: Optional[int] = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Duruş verilerini yükle"""
        query = """
            SELECT dr.*, m.name as machine_name
            FROM downtime_reasons dr
            JOIN machines m ON dr.machine_id = m.id
            WHERE dr.resolved = true
        """
        
        params = {}
        
        if machine_id:
            query += " AND dr.machine_id = :machine_id"
            params['machine_id'] = machine_id
        
        if start_date:
            query += " AND dr.start_time >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            query += " AND dr.start_time <= :end_date"
            params['end_date'] = end_date
        
        query += " ORDER BY dr.start_time"
        
        return pd.read_sql(text(query), self.connection, params=params)
    
    def load_oee_data(self, machine_id: Optional[int] = None,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> pd.DataFrame:
        """OEE verilerini yükle"""
        query = """
            SELECT * FROM oee_calculations
            WHERE 1=1
        """
        
        params = {}
        
        if machine_id:
            query += " AND machine_id = :machine_id"
            params['machine_id'] = machine_id
        
        if start_date:
            query += " AND timestamp >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            query += " AND timestamp <= :end_date"
            params['end_date'] = end_date
        
        query += " ORDER BY timestamp"
        
        return pd.read_sql(text(query), self.connection, params=params)
    
    def get_machine_list(self) -> List[Dict]:
        """Makine listesini getir"""
        query = "SELECT id, name, type FROM machines ORDER BY name"
        result = self.connection.execute(text(query))
        return [dict(row) for row in result]
    
    def close(self):
        """Bağlantıyı kapat"""
        self.connection.close()
        self.engine.dispose()

# Yardımcı fonksiyonlar
def resample_time_series(df: pd.DataFrame, time_col: str, value_col: str, freq: str = '1H') -> pd.DataFrame:
    """Zaman serisi verilerini yeniden örnekle"""
    if df.empty:
        return df
    
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    df.set_index(time_col, inplace=True)
    
    resampled = df[value_col].resample(freq).mean().reset_index()
    return resampled

def calculate_moving_average(df: pd.DataFrame, column: str, window: int = 7) -> pd.Series:
    """Hareketli ortalama hesapla"""
    return df[column].rolling(window=window, min_periods=1).mean()

def detect_outliers(df: pd.DataFrame, column: str, threshold: float = 2.0) -> pd.Series:
    """Aykırı değerleri tespit et"""
    mean = df[column].mean()
    std = df[column].std()
    
    if std == 0:
        return pd.Series([False] * len(df))
    
    z_scores = (df[column] - mean) / std
    return abs(z_scores) > threshold
