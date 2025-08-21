import React from 'react';

const ProductionCounter = ({ goodParts, defectiveParts, onProductionRecord }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">Üretim Sayacı</h3>
      
      <div className="grid grid-cols-2 gap-4">
        {/* İyi Ürün Sayacı */}
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-800 mb-2">İyi Ürün</div>
          <div className="text-4xl font-bold text-green-600 mb-4">{goodParts}</div>
          <button
            onClick={() => onProductionRecord(true)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            + İyi Ürün Ekle
          </button>
        </div>

        {/* Hatalı Ürün Sayacı */}
        <div className="text-center p-4 bg-red-50 rounded-lg">
          <div className="text-2xl font-bold text-red-800 mb-2">Hatalı Ürün</div>
          <div className="text-4xl font-bold text-red-600 mb-4">{defectiveParts}</div>
          <button
            onClick={() => onProductionRecord(false)}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            + Hatalı Ürün Ekle
          </button>
        </div>
      </div>

      {/* Toplam ve Oranlar */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-sm text-blue-600">Toplam</div>
            <div className="text-xl font-bold text-blue-800">
              {goodParts + defectiveParts}
            </div>
          </div>
          <div>
            <div className="text-sm text-green-600">Kalite Oranı</div>
            <div className="text-xl font-bold text-green-800">
              {goodParts + defectiveParts > 0 
                ? `${Math.round((goodParts / (goodParts + defectiveParts)) * 100)}%`
                : '0%'
              }
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Hata Oranı</div>
            <div className="text-xl font-bold text-gray-800">
              {goodParts + defectiveParts > 0 
                ? `${Math.round((defectiveParts / (goodParts + defectiveParts)) * 100)}%`
                : '0%'
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductionCounter;
