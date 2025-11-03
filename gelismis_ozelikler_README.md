# 🚀 GELİŞMİŞ MARKET BASKET ANALYSIS UYGULAMASI

## ✨ EKLENEN YENİ ÖZELLİKLER

### 1. 🎯 3'lü Ürün Kombinasyonu Analizi


**Özellikler:**
- 3 ürünün birlikte alınma paternlerini tespit eder
- Support threshold'a göre filtreleme
- Bundle/paket stratejileri için kritik veri
- Kompleks müşteri davranışlarını ortaya çıkarır

**İş Değeri:**
```
Örnek: Milk + Bread + Butter kombinasyonu
→ "Kahvaltı Paketi" kampanyası
→ Sabah saatlerinde özel fiyat
→ 3 ürün bir arada %20 indirim
```

**Kullanım:**
- Minimum support ayarlayın (varsayılan: %3)
- Top 20 kombinasyonu görün
- Her kombinasyon için sepet sayısı ve support oranı
- En güçlü kombinasyon için detaylı iş önerileri

---

### 2. 🔗 Network Analizi (Ağ Grafiği)
**Neden Önemli:** Ürün ilişkilerini görsel olarak anlamak

**Özellikler:**
- NetworkX ile interaktif ağ grafiği
- Node büyüklüğü = Ürün popülaritesi
- Edge kalınlığı = Birliktelik gücü (Lift)
- Renk kodlaması ile ilişki gücü gösterimi
- Merkezilik (centrality) metrikleri

**Metrikler:**
- **Degree Centrality:** Hangi ürünler hub (merkez) konumunda?
- **Network Density:** Ürünler arası bağlantı yoğunluğu
- **Average Degree:** Ortalama bağlantı sayısı

**İş Değeri:**
```
Hub Products (Merkezi Ürünler):
→ Milk: 8 farklı ürünle güçlü bağlantı
→ Mağaza stratejisi: Milk'i merkezi konuma koyun
→ Cross-selling: Milk yanına en çok bağlantılı ürünleri yerleştirin
```

**Kullanım:**
- Min Support ve Min Lift ayarlayın
- Max node sayısı seçin (5-20)
- Interaktif grafikte hover ile detay görün
- En merkezi ürünleri belirleyin

---

### 3. 🎲 Sepet Segmentasyonu
**Neden Önemli:** Farklı müşteri tipleri farklı davranır

**Özellikler:**
- Kuartillere göre otomatik segmentasyon:
  - 🛍️ Küçük Sepetler (Q1'e kadar)
  - 📦 Orta Sepetler (Q1-Q2 arası)
  - 🛒 Büyük Sepetler (Q2-Q3 arası)
  - 🎁 Mega Sepetler (Q3'ten büyük)
- Her segment için ayrı ürün popülarite analizi
- Genel popülariteyle karşılaştırma
- Segment-spesifik iş önerileri

**İş Değeri:**
```
Küçük Sepetler:
- Hızlı alışveriş deneyimi
- İmpuls ürünler (kasa önü)
- "2. ürüne %50 indirim"

Mega Sepetler:
- Sadakat programı
- Ücretsiz teslimat
- VIP müşteri deneyimi
```

**Kullanım:**
- Segment seçin
- Top 15 ürün grafiği
- Genel ortalama ile karşılaştırma
- Segment'e özel ürünleri görün (+/- fark analizi)

---

### 4. ⚖️ Negatif Birliktelikler
**Neden Önemli:** Hangi ürünler birlikte ALINMIYOR?

**Kavram:**
- **Lift < 1.0:** Negatif birliktelik
- Ürünler tesadüfen beklenenin altında birlikte alınıyor
- Bu ürünler muhtemelen:
  - Alternatif ürünler (Coca Cola vs Pepsi)
  - Farklı segmentler (Bebek vs Alkol)
  - Tamamlayıcı değil

**Özellikler:**
- Beklenen vs gerçek birlikte alım karşılaştırması
- Lift değerine göre negatif ilişki gücü
- Top 20 negatif çift
- Fark analizi (kaç sepet eksik?)

**İş Değeri:**
```
Apple vs Chocolate (Lift: 0.65)
Beklenen: 45 sepet
Gerçek: 29 sepet
→ Bu ürünleri aynı kampanyada kullanma
→ Farklı müşteri segmentlerine hitap ediyor
→ Mağazada ayrı bölgelere yerleştir
```

**Kullanım:**
- Analizi çalıştır
- Top 20 negatif çifti görün
- Lift grafiği (1.0'dan ne kadar uzak)
- En güçlü negatif ilişki için detaylı analiz

---

### 5. 🚀 Akıllı Öneri Sistemi
**Neden Önemli:** Gerçek zamanlı, çoklu ürün bazlı öneri

**Özellikler:**
- **Çoklu ürün seçimi:** Birden fazla ürünle sepet simülasyonu
- **Akıllı skorlama:** Confidence × Lift ile öneri gücü
- **Agregasyon:** Aynı ürün için farklı kaynaklardan gelen kuralları birleştirir
- **Görselleştirme:**
  - Confidence vs Lift scatter plot
  - Öneri sıralaması bar chart
  - Detaylı öneri kartları

**Skorlama Algoritması:**
```python
Öneri Skoru = Σ(Confidence × Lift)
# Birden fazla kaynak ürünle ilişkiliyse skorlar toplanır
```

**İş Değeri:**
```
Sepet: [Milk, Bread]
Öneriler:
1. Butter (Skor: 2.8, Confidence: 65%, Lift: 1.5)
2. Eggs (Skor: 2.3, Confidence: 55%, Lift: 1.4)
3. Cheese (Skor: 2.0, Confidence: 50%, Lift: 1.3)

→ E-ticarette "Bunları da beğenebilirsiniz"
→ Fiziksel mağazada kasada öneri
→ Mobil uygulamada push notification
```

**Kullanım:**
- Sepete 1 veya daha fazla ürün ekle
- Öneri sayısını ayarla (3-15)
- Min confidence belirle
- "Öneri Getir" butonuna tıkla
- Önerileri skor, confidence, lift'e göre gör
- İş stratejilerini incele

---

### 6. 📊 Gelişmiş Görselleştirmeler

#### A) Isı Haritası (Heatmap)
- Top 15 ürün için co-occurrence matrix
- Hangi ürünler ne sıklıkla birlikte alınıyor
- Koyu renkler = Güçlü birliktelik

#### B) Lift Korelasyon Matrisi
- Lift değerleri bazlı ilişki matrisi
- Renk kodlaması:
  - 🟢 Yeşil (>1.0): Pozitif ilişki
  - 🟡 Sarı (~1.0): Bağımsız
  - 🔴 Kırmızı (<1.0): Negatif ilişki

#### C) Scatter Plotlar
- Support-Confidence-Lift 3D analizi
- Bubble size ile support gösterimi
- İnteraktif hover bilgileri

#### D) Network Graph
- Node-edge grafiği
- Spring layout algoritması
- Merkezilik analizi

---

## 🧠 Market Basket Analysis Kavramlarının Uygulanması

### Support (Destek)
```python
Support(X) = n(X) / N

Örnek: Milk 400 sepette, toplam 999 sepet
Support(Milk) = 400/999 = 0.40 = %40
```

**Uygulama:**
- Tek ürün analizi (popülerlik)
- Çift ürün analizi (birliktelik)
- 3'lü kombinasyon analizi
- Filtreleme kriteri (min_support)

---

### Confidence (Güven)
```python
Confidence(X→Y) = Support(X,Y) / Support(X)

Örnek: Milk+Bread 85 sepette, Milk 400 sepette
Confidence(Milk→Bread) = 85/400 = 0.21 = %21
```

**Uygulama:**
- Kural oluşturma (A→B)
- Öneri sistemi temel metrigi
- Kural filtreleme (min_confidence)
- Güven dağılımı histogramı

---

### Lift
```python
Lift(X→Y) = Confidence(X→Y) / Support(Y)

Yorum:
- Lift > 1: Pozitif birliktelik ✅
- Lift = 1: Bağımsızlık 🟡
- Lift < 1: Negatif birliktelik ⚠️

Örnek: Lift = 1.6
"Bu birliktelik tesadüften 1.6 kat daha güçlü"
```

**Uygulama:**
- Network grafiğinde edge kalınlığı
- Kural kalitesi değerlendirmesi
- Negatif birliktelik tespiti
- Lift matrisi görselleştirmesi

---

## 💡 İleri Seviye Özellikler

### 1. Session State Yönetimi
```python
st.session_state['birliktelikler'] = birliktelikler
st.session_state['kurallar'] = kurallar
st.session_state['uclu_kombinasyonlar'] = uclu_kombinasyonlar
```
**Faydası:** Sayfa değişikliklerinde veri kaybı yok

---

### 2. Custom CSS Styling
```python
.insight-box # Özel bilgi kutuları
.stMetric # Metrik kartları
```
**Faydası:** Profesyonel görünüm

---

### 3. Adaptive Thresholding
- Her analiz türü için uygun minimum değerler
- 2'li için: min_support = 0.05
- 3'lü için: min_support = 0.03 (daha düşük)
**Sebep:** 3'lü kombinasyonlar doğal olarak daha az görülür

---

### 4. Multi-Source Aggregation (Öneri Sisteminde)
```python
# Aynı ürün için farklı kaynaklardan gelen kuralları birleştir
if urun in tum_oneriler:
    tum_oneriler[urun]['skor'] += confidence * lift
    tum_oneriler[urun]['kaynak_urunler'].append(secili_urun)
```
**Faydası:** Çoklu ürün seçiminde daha doğru öneriler

---

## 📈 Performans İyileştirmeleri

### 1. Caching
```python
@st.cache_data
def veri_yukle():
    # Veri sadece bir kez yüklenir
```

### 2. Efektif Veri Yapıları
- Dictionary'ler O(1) lookup
- Combinations yerine itertools
- NumPy array operations

### 3. Lazy Loading
- Ağır analizler sadece butona basınca çalışır
- Gereksiz hesaplama yok


## 🚀 Nasıl Çalıştırılır?

### Gereksinimler
```bash
pip install streamlit pandas numpy matplotlib seaborn plotly networkx
```

### Çalıştırma
```bash
streamlit run gelismis_streamlit_app.py
```

### Tarayıcıda Açılacak Modüller
1. 🏠 Ana Sayfa & İstatistikler
2. 📊 Veri Keşfi & Görselleştirme
3. 🔍 Tek & Çift Ürün Analizi
4. 🎯 **3'lü Kombinasyon Analizi** ← YENİ
5. 🔗 **Network Analizi (Ağ Grafiği)** ← YENİ
6. 📋 Gelişmiş Kural Analizi
7. 🎲 **Sepet Segmentasyonu** ← YENİ
8. ⚖️ **Negatif Birliktelikler** ← YENİ
9. 🚀 Akıllı Öneri Sistemi

---

## 💼 İş Uygulamaları - Gerçek Dünya Senaryoları

### Senaryo 1: Süpermarket Zinciri
**Durum:** 1000 mağazalı süpermarket zinciri

**Uygulama:**
1. **3'lü Analiz:** "Kahvaltı Paketi" kombinasyonları bulun
2. **Network Analizi:** Hub ürünleri tespit edin → Stratejik raf konumlandırması
3. **Segmentasyon:** Farklı mağazalar için farklı stratejiler
4. **Öneri Sistemi:** Kasa önü tablet'lerde real-time öneriler

**Sonuç:** %15-20 sepet büyüklüğü artışı

---

### Senaryo 2: E-Ticaret Platformu
**Durum:** Online market

**Uygulama:**
1. **Akıllı Öneri:** Sepet sayfasında "Bunları da beğenebilirsiniz"
2. **Negatif Analiz:** Yararsız önerilerden kaçının
3. **Segmentasyon:** Küçük sepetlere özel "Minimum tutar" kampanyaları
4. **Network:** İlgili ürün önerileri için görsel widget

**Sonuç:** %25 conversion rate artışı

---

### Senaryo 3: Kampanya Optimizasyonu
**Durum:** Haftalık kampanya planlama

**Uygulama:**
1. **Lift Analizi:** En güçlü birlikteliklerde bundle indirim
2. **3'lü Kombinasyon:** Üçlü paket kampanyaları
3. **Segmentasyon:** Her segment için özel kampanya
4. **Negatif Analiz:** Hangi ürünleri aynı kampanyada vermeyin

**Sonuç:** %30 kampanya ROI artışı

---
