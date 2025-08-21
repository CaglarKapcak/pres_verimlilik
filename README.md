# Fabrika Verimlilik İzleme Sistemi
## Proje Hakkında

Fabrika Verimlilik İzleme Sistemi, Endüstri 4.0 standartlarına uygun, modern bir üretim verimliliği takip ve analiz çözümüdür. Bu sistem, üretim tesislerindeki makinelerin performansını gerçek zamanlı olarak izlemek, verimlilik metriklerini hesaplamak ve detaylı analizler sunmak üzere tasarlanmıştır.

## Sistem Mimarisi
🎯 Temel Özellikler
### ✅ Gerçek Zamanlı Veri İzleme
Makine çalışma durumu ve operasyon modları

Enerji tüketimi ve güç analizi

Üretim adetleri ve cycle time takibi

Anlık veri görselleştirme

### ✅ OEE (Toplam Ekipman Verimliliği) Hesaplama
Kullanılabilirlik: Planlanan üretim süresinde makinenin ne kadarının kullanıldığı

Performans: Makinenin optimum hızına göre ne kadar verimle çalıştığı

Kalite: Üretilen iyi parça oranı

### ✅ Operatör Arayüzü
Tablet ve mobil cihaz uyumlu responsive tasarım

Durum bildirimleri ve alarm yönetimi

Üretim verisi girişi ve makine duruş nedenleri kaydı

### ✅ IoT Entegrasyonu
Sensör verilerinin otomatik olarak toplanması

Analog ve dijital sinyallerin okunması

Gerçek zamanlı veri işleme

### ✅ Kapsamlı Raporlama
Detaylı verimlilik analizleri

PDF formatında rapor oluşturma

Özelleştirilebilir rapor şablonları

Tarih aralığına göre filtreleme

### ✅ WebSocket Desteği
Anlık veri güncellemeleri

Çoklu kullanıcı desteği

Eş zamanlı veri senkronizasyonu
## 🛠 Teknoloji Stack'i
### Backend
FastAPI: Yüksek performanslı Python web framework

PostgreSQL: İlişkisel veritabanı

TimescaleDB: Zaman serisi verileri için PostgreSQL extension'ı

SQLAlchemy: Python ORM (Nesne-İlişkisel Eşleme)

Uvicorn: ASGI sunucusu

### Frontend
React: Modern kullanıcı arayüzü kütüphanesi

TailwindCSS: Utility-first CSS framework

Chart.js: Veri görselleştirme ve grafik kütüphanesi

WebSocket: Gerçek zamanlı veri akışı

### IoT Gateway
Raspberry Pi: Edge computing cihazı

Python 3.9+: Sensör okuma ve veri işleme

ADS1115: Analog'dan dijitale dönüştürücü (ADC)

Çeşitli sensörler: Akım, voltaj, sıcaklık, proximity sensörleri


# 🚀 Kurulum ve Başlangıç
## Gereksinimler
Docker ve Docker Compose

Python 3.9+

Node.js 16+

### Hızlı Kurulum
'''
# Repository'yi klonla
git clone <repository-url>
cd factory-efficiency-system

# Environment dosyalarını hazırla
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Docker container'ları başlat
docker-compose up -d

# Database'i initialize et
docker-compose exec backend python database/init_db.py
'''


## Ortam Değişkenleri Yapılandırması
### Backend (.env)
DATABASE_URL=postgresql://user:password@db:5432/factory_db
SECRET_KEY=your-secret-key
DEBUG=False

### Frontend (.env)

REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws 

## 📈 OEE Hesaplama Metodolojisi
OEE = Kullanılabilirlik × Performans × Kalite

Kullanılabilirlik: Çalışma Süresi / Planlanan Süre

Performans: (Toplam Üretim × Ideal Cycle Time) / Çalışma Süresi

Kalite: İyi Ürün Adedi / Toplam Üretim

## IoT Sensör Entegrasyonu
Sistem aşağıdaki sensörleri desteklemektedir:

Akım Sensörleri: Makine enerji tüketimi izleme

Sıcaklık Sensörleri: Ekipman ısınma kontrolü

Proximity Sensörler: Üretim sayımı ve makine duruş tespiti

Encoderlar: Dönüş hızı ve pozisyon takibi

## 📋 Raporlama Özellikleri
Günlük/haftalık/aylık verimlilik raporları

Makine bazlı performans karşılaştırması

Enerji tüketim analizleri

Dur


