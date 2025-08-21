import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

class DowntimeReportGenerator:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
    
    def generate_downtime_analysis(self, machine_id=None, start_date=None, end_date=None):
        """Duruş analizi raporu oluştur"""
        if not end_date:
            end_date = datetime.now().date()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        query = """
            SELECT dr.category,
                   dr.reason,
                   SUM(EXTRACT(EPOCH FROM dr.duration)) as total_downtime_seconds,
                   COUNT(*) as incident_count,
                   m.name as machine_name
            FROM downtime_reasons dr
            JOIN machines m ON dr.machine_id = m.id
            WHERE dr.resolved = true
            AND dr.start_time BETWEEN :start_date AND :end_date
        """
        
        params = {'start_date': start_date, 'end_date': end_date}
        
        if machine_id:
            query += " AND dr.machine_id = :machine_id"
            params['machine_id'] = machine_id
        
        query += " GROUP BY dr.category, dr.reason, m.name ORDER BY total_downtime_seconds DESC"
        
        df = pd.read_sql(query, self.engine, params=params)
        
        if df.empty:
            return None
        
        # Toplam duruş süresi
        total_downtime_hours = df['total_downtime_seconds'].sum() / 3600
        
        # Kategori bazlı analiz
        category_analysis = df.groupby('category').agg({
            'total_downtime_seconds': 'sum',
            'incident_count': 'sum'
        }).reset_index()
        
        category_analysis['downtime_hours'] = category_analysis['total_downtime_seconds'] / 3600
        category_analysis['avg_downtime_per_incident'] = category_analysis['total_downtime_seconds'] / category_analysis['incident_count']
        
        # Grafik oluştur
        self._create_downtime_charts(category_analysis, df, start_date, end_date, machine_id)
        
        return {
            'total_downtime_hours': round(total_downtime_hours, 2),
            'total_incidents': df['incident_count'].sum(),
            'category_analysis': category_analysis.to_dict('records'),
            'top_reasons': df.head(10).to_dict('records'),
            'report_period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
    
    def _create_downtime_charts(self, category_analysis, detailed_df, start_date, end_date, machine_id):
        """Duruş analizi grafikleri oluştur"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Kategori dağılımı (Pasta grafik)
        categories = category_analysis['category']
        downtime_hours = category_analysis['downtime_hours']
        
        ax1.pie(downtime_hours, labels=categories, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Duruş Kategori Dağılımı')
        
        # Kategori bazlı çubuk grafik
        y_pos = np.arange(len(categories))
        ax2.barh(y_pos, downtime_hours, align='center')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(categories)
        ax2.invert_yaxis()
        ax2.set_xlabel('Duruş Süresi (Saat)')
        ax2.set_title('Kategori Bazlı Duruş Süreleri')
        
        # Zaman içinde duruş trendi
        time_query = """
            SELECT DATE(start_time) as date,
                   SUM(EXTRACT(EPOCH FROM duration)) as daily_downtime
            FROM downtime_reasons
            WHERE start_time BETWEEN :start_date AND :end_date
        """
        
        if machine_id:
            time_query += " AND machine_id = :machine_id"
        
        time_query += " GROUP BY DATE(start_time) ORDER BY date"
        
        time_params = {'start_date': start_date, 'end_date': end_date}
        if machine_id:
            time_params['machine_id'] = machine_id
        
        time_df = pd.read_sql(time_query, self.engine, params=time_params)
        time_df['downtime_hours'] = time_df['daily_downtime'] / 3600
        
        ax3.plot(time_df['date'], time_df['downtime_hours'], marker='o')
        ax3.set_title('Günlük Duruş Trendi')
        ax3.set_ylabel('Duruş Süresi (Saat)')
        ax3.grid(True, alpha=0.3)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        # En sık karşılaşılan nedenler
        top_reasons = detailed_df.head(10)
        y_pos_reasons = np.arange(len(top_reasons))
        
        ax4.barh(y_pos_reasons, top_reasons['incident_count'], align='center')
        ax4.set_yticks(y_pos_reasons)
        ax4.set_yticklabels(top_reasons['reason'])
        ax4.invert_yaxis()
        ax4.set_xlabel('Olay Sayısı')
        ax4.set_title('En Sık Karşılaşılan Duruş Nedenleri')
        
        plt.tight_layout()
        
        filename = f'downtime_report_{start_date}_{end_date}'
        if machine_id:
            filename += f'_machine_{machine_id}'
        filename += '.png'
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Duruş raporu kaydedildi: {filename}")

# Kullanım örneği
if __name__ == "__main__":
    generator = DowntimeReportGenerator("postgresql://admin:factory123@localhost/factory_db")
    report = generator.generate_downtime_analysis(
        machine_id=1,
        start_date='2024-01-01',
        end_date='2024-01-31'
    )
    
    if report:
        print("Toplam Duruş Süresi:", report['total_downtime_hours'], "saat")
        print("Toplam Olay Sayısı:", report['total_incidents'])
