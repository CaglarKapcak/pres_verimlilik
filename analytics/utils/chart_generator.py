import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ChartGenerator:
    def __init__(self):
        plt.style.use('default')
        sns.set_palette("husl")
    
    def create_oee_trend_chart(self, oee_data: pd.DataFrame, title: str = "OEE Trendi") -> go.Figure:
        """OEE trend grafiği oluştur"""
        fig = make_subplots(rows=2, cols=1, subplot_titles=('OEE Trendi', 'OEE Bileşenleri'))
        
        # OEE trendi
        fig.add_trace(
            go.Scatter(x=oee_data['timestamp'], y=oee_data['oee']*100, 
                      name='OEE', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Bileşenler
        fig.add_trace(
            go.Scatter(x=oee_data['timestamp'], y=oee_data['availability']*100, 
                      name='Kullanılabilirlik', line=dict(color='green')),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=oee_data['timestamp'], y=oee_data['performance']*100, 
                      name='Performans', line=dict(color='orange')),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=oee_data['timestamp'], y=oee_data['quality']*100, 
                      name='Kalite', line=dict(color='red')),
            row=2, col=1
        )
        
        fig.update_layout(height=600, title_text=title)
        fig.update_yaxes(title_text="OEE (%)", row=1, col=1)
        fig.update_yaxes(title_text="Oran (%)", row=2, col=1)
        
        return fig
    
    def create_production_comparison_chart(self, production_data: pd.DataFrame, 
                                         title: str = "Üretim Karşılaştırması") -> go.Figure:
        """Üretim karşılaştırma grafiği"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=production_data['shift_date'],
            y=production_data['good_parts'],
            name='İyi Ürün',
            marker_color='green'
        ))
        
        fig.add_trace(go.Bar(
            x=production_data['shift_date'],
            y=production_data['defective_parts'],
            name='Hatalı Ürün',
            marker_color='red'
        ))
        
        fig.update_layout(
            title=title,
            barmode='stack',
            xaxis_title="Tarih",
            yaxis_title="Ürün Sayısı"
        )
        
        return fig
    
    def create_downtime_analysis_chart(self, downtime_data: pd.DataFrame, 
                                     title: str = "Duruş Analizi") -> go.Figure:
        """Duruş analizi grafiği"""
        fig = make_subplots(rows=1, cols=2, 
                           specs=[[{"type": "pie"}, {"type": "bar"}]],
                           subplot_titles=('Kategori Dağılımı', 'Süre Bazlı Analiz'))
        
        # Pasta grafik - Kategori dağılımı
        category_summary = downtime_data.groupby('category')['duration'].sum().reset_index()
        fig.add_trace(
            go.Pie(labels=category_summary['category'], 
                  values=category_summary['duration'],
                  name="Kategori Dağılımı"),
            row=1, col=1
        )
        
        # Çubuk grafik - Süre bazlı analiz
        time_analysis = downtime_data.groupby('reason')['duration'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(x=time_analysis['duration'], 
                  y=time_analysis['reason'],
                  orientation='h',
                  name="Süre Bazlı Analiz"),
            row=1, col=2
        )
        
        fig.update_layout(height=500, title_text=title)
        fig.update_xaxes(title_text="Süre (saniye)", row=1, col=2)
        
        return fig
    
    def create_correlation_heatmap(self, data: pd.DataFrame, 
                                 columns: List[str], 
                                 title: str = "Korelasyon Matrisi") -> go.Figure:
        """Korelasyon ısı haritası"""
        corr_matrix = data[columns].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu_r',
            zmin=-1,
            zmax=1,
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Değişkenler",
            yaxis_title="Değişkenler"
        )
        
        return fig
    
    def create_control_chart(self, data: pd.DataFrame, value_col: str, 
                           time_col: str, title: str = "Kontrol Grafiği") -> go.Figure:
        """Kontrol grafiği oluştur"""
        mean = data[value_col].mean()
        std = data[value_col].std()
        
        fig = go.Figure()
        
        # Veri noktaları
        fig.add_trace(go.Scatter(
            x=data[time_col],
            y=data[value_col],
            mode='markers+lines',
            name='Değerler'
        ))
        
        # Ortalama çizgisi
        fig.add_hline(y=mean, line_dash="solid", line_color="green", 
                     annotation_text="Ortalama", annotation_position="bottom right")
        
        # Kontrol limitleri
        fig.add_hline(y=mean + 2*std, line_dash="dash", line_color="orange",
                     annotation_text="+2σ", annotation_position="bottom right")
        fig.add_hline(y=mean - 2*std, line_dash="dash", line_color="orange",
                     annotation_text="-2σ", annotation_position="bottom right")
        fig.add_hline(y=mean + 3*std, line_dash="dot", line_color="red",
                     annotation_text="+3σ", annotation_position="bottom right")
        fig.add_hline(y=mean - 3*std, line_dash="dot", line_color="red",
                     annotation_text="-3σ", annotation_position="bottom right")
        
        fig.update_layout(
            title=title,
            xaxis_title="Zaman",
            yaxis_title=value_col
        )
        
        return fig

# Yardımcı fonksiyonlar
def save_plotly_chart(fig: go.Figure, filename: str, width: int = 1200, height: int = 600):
    """Plotly grafiğini kaydet"""
    fig.write_image(filename, width=width, height=height)

def create_combined_dashboard(oee_data: pd.DataFrame, production_data: pd.DataFrame, 
                            downtime_data: pd.DataFrame) -> go.Figure:
    """Kombine dashboard oluştur"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('OEE Trendi', 'Üretim Performansı', 'Duruş Analizi', 'Kalite Oranı'),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "scatter"}]]
    )
    
    # OEE Trendi
    fig.add_trace(
        go.Scatter(x=oee_data['timestamp'], y=oee_data['oee']*100, name='OEE'),
        row=1, col=1
    )
    
    # Üretim Performansı
    fig.add_trace(
        go.Bar(x=production_data['shift_date'], y=production_data['total_parts'], name='Toplam Üretim'),
        row=1, col=2
    )
    
    # Duruş Analizi
    downtime_summary = downtime_data.groupby('category')['duration'].sum()
    fig.add_trace(
        go.Pie(labels=downtime_summary.index, values=downtime_summary.values),
        row=2, col=1
    )
    
    # Kalite Oranı
    fig.add_trace(
        go.Scatter(x=production_data['shift_date'], y=production_data['quality_rate'], name='Kalite Oranı'),
        row=2, col=2
    )
    
    fig.update_layout(height=800, title_text="Üretim Dashboard", showlegend=False)
    return fig
