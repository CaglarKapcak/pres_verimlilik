import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

class ProductionReportGenerator:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
    
    def generate_production_report(self, machine_id=None, start_date=None, end_date=None):
        """Üretim raporu oluştur"""
        if not end_date:
            end_date = datetime.now().date()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        query = """
            SELECT p.shift_date,
                   m.name as machine_name,
                   p.shift_number,
                   p.good_parts,
                   p.defective_parts,
                   p.good_parts + p.defective_parts as total_parts,
                   ROUND(p.good_parts * 100.0 / NULLIF(p.good_parts + p.defective_parts, 0), 2) as quality_rate,
                   p.target_count,
                   ROUND((p.good_parts + p.defective_parts) * 100.0 / NULLIF(p.target_count, 0), 2) as efficiency_rate
            FROM production_data p
            JOIN machines m ON p.machine_id = m.id
            WHERE p.shift_date BETWEEN :start_date AND :end_date
        """
        
        params = {'start_date': start_date, 'end_date': end_date}
        
        if machine_id:
            query += " AND p.machine_id = :machine_id"
            params['machine_id'] = machine_id
        
        query += " ORDER BY p.shift_date, p.shift_number"
        
        df = pd.read_sql(query, self.engine, params=params)
        
        if df.empty:
            return None
        
        # Toplam metrikler
        total_good = df['good_parts'].sum()
        total_defective = df['defective_parts'].sum()
        total_produced = total_good + total_defective
        overall_quality = total_good / total_produced if total_produced > 0 else 0
        
        # Vardiya bazlı ortalama metrikler
        shift_analysis = df.groupby('shift_number').agg({
            'good_parts': 'mean',
            'defective_parts': 'mean',
            'quality_rate': 'mean',
            'efficiency_rate': 'mean'
        }).reset_index()
        
        # Günlük trendler
        daily_trend = df.groupby('shift_date').agg({
            'good_parts': 'sum',
            'defective_parts': 'sum',
            'total_parts': 'sum',
            'quality_rate': 'mean'
        }).reset_index()
        
        # Grafikler oluştur
        self._create_production_charts(df, daily_trend, shift_analysis, start_date, end_date, machine_id)
        
        return {
            'total_good_parts': total_good,
            'total_defective_parts': total_defective,
            'total_produced': total_produced,
            'overall_quality_rate': round(overall_quality * 100, 2),
            'daily_average_production': round(daily_trend['total_parts'].mean(), 2),
            'shift_analysis': shift_analysis.to_dict('records'),
            'daily_trend': daily_trend.to_dict('records'),
            'report_period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
    
    def _create_production_charts(self, df, daily_trend, shift_analysis, start_date, end_date, machine_id):
        """Üretim raporu grafikleri oluştur"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Günlük üretim trendi
        ax1.bar(daily_trend['shift_date'], daily_trend['good_parts'], label='İyi Ürün')
        ax1.bar(daily_trend['shift_date'], daily_trend['defective_parts'], 
                bottom=daily_trend['good_parts'], label='Hatalı Ürün')
        ax1.set_title('Günlük Üretim Miktarı')
        ax1.set_ylabel('Ürün Sayısı')
        ax1.legend()
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Kalite oranı trendi
        ax2.plot(daily_trend['shift_date'], daily_trend['quality_rate'], marker='o', color='green')
        ax2.set_title('Günlük Kalite Oranı Trendi')
        ax2.set_ylabel('Kalite Oranı (%)')
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # Vardiya bazlı performans
        shifts = shift_analysis['shift_number']
        shift_labels = [f'Vardiya {shift}' for shift in shifts]
        
        x_pos = np.arange(len(shifts))
        width = 0.35
        
        ax3.bar(x_pos - width/2, shift_analysis['quality_rate'], width, label='Kalite Oranı')
        ax3.bar(x_pos + width/2, shift_analysis['efficiency_rate'], width, label='Verimlilik Oranı')
        ax3.set_xlabel('Vardiya')
        ax3.set_ylabel('Oran (%)')
        ax3.set_title('Vardiya Bazlı Performans')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(shift_labels)
        ax3.legend()
        
        # Üretim hedefi karşılaştırması
        if 'target_count' in df.columns:
            df['target_achievement'] = df['total_parts'] / df['target_count'] * 100
            target_analysis = df.groupby('shift_date')['target_achievement'].mean().reset_index()
            
            ax4.bar(target_analysis['shift_date'], target_analysis['target_achievement'])
            ax4.axhline(y=100, color='r', linestyle='--', label='Hedef (100%)')
            ax4.set_title('Hedef Gerçekleşme Oranı')
            ax4.set_ylabel('Hedef Gerçekleşme (%)')
            ax4.legend()
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        filename = f'production_report_{start_date}_{end_date}'
        if machine_id:
            filename += f'_machine_{machine_id}'
        filename += '.png'
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Üretim raporu kaydedildi: {filename}")

# Kullanım örneği
if __name__ == "__main__":
    generator = ProductionReportGenerator("postgresql://admin:factory123@localhost/factory_db")
    report = generator.generate_production_report(
        machine_id=1,
        start_date='2024-01-01',
        end_date='2024-01-31'
    )
    
    if report:
        print("Toplam İyi Ürün:", report['total_good_parts'])
        print("Toplam Hatalı Ürün:", report['total_defective_parts'])
        print("Genel Kalite Oranı:", report['overall_quality_rate'], "%")
