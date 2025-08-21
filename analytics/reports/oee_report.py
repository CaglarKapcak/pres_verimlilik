import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import numpy as np

class OEEReportGenerator:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
    
    def generate_daily_report(self, machine_id, start_date, end_date):
        """Günlük OEE raporu oluştur"""
        query = f"""
            SELECT date(timestamp) as date,
                   AVG(availability) as avg_availability,
                   AVG(performance) as avg_performance,
                   AVG(quality) as avg_quality,
                   AVG(oee) as avg_oee
            FROM oee_calculations
            WHERE machine_id = {machine_id}
            AND timestamp BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY date(timestamp)
            ORDER BY date
        """
        
        df = pd.read_sql(query, self.engine)
        self._create_charts(df, machine_id, start_date, end_date)
        return df
    
    def _create_charts(self, df, machine_id, start_date, end_date):
        """Grafikler oluştur"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # OEE Trendi
        ax1.plot(df['date'], df['avg_oee'], marker='o', linewidth=2)
        ax1.set_title('Günlük OEE Trendi')
        ax1.set_ylabel('OEE (%)')
        ax1.grid(True, alpha=0.3)
        
        # Bileşenler
        ax2.plot(df['date'], df['avg_availability'], label='Kullanılabilirlik', marker='s')
        ax2.plot(df['date'], df['avg_performance'], label='Performans', marker='^')
        ax2.plot(df['date'], df['avg_quality'], label='Kalite', marker='d')
        ax2.set_title('OEE Bileşenleri')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Duruş analizi
        downtime_df = self._get_downtime_data(machine_id, start_date, end_date)
        ax3.pie(downtime_df['total_downtime'], labels=downtime_df['category'], autopct='%1.1f%%')
        ax3.set_title('Duruş Nedenleri Dağılımı')
        
        # Üretim verileri
        production_df = self._get_production_data(machine_id, start_date, end_date)
        ax4.bar(production_df['shift_date'], production_df['good_parts'], label='İyi Ürün')
        ax4.bar(production_df['shift_date'], production_df['defective_parts'], 
                bottom=production_df['good_parts'], label='Hatalı Ürün')
        ax4.set_title('Günlük Üretim')
        ax4.legend()
        
        plt.tight_layout()
        filename = f'oee_report_{machine_id}_{start_date}_{end_date}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Rapor oluşturuldu: {filename}")

# Kullanım
if __name__ == "__main__":
    generator = OEEReportGenerator("postgresql://admin:factory123@localhost/factory_db")
    report = generator.generate_daily_report(
        machine_id=1,
        start_date='2024-01-01',
        end_date='2024-01-31'
    )
    print(report)
