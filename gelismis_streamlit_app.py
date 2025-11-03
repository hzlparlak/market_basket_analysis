"""
GELİŞMİŞ STREAMLIT UYGULAMASI
Market Basket Analysis için ileri seviye web arayüzü
Öğrencinin konuyu derinlemesine anladığını gösteren özellikler içerir
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import networkx as nx

# Sayfa ayarları
st.set_page_config(
    page_title="Gelişmiş Market Sepeti Analizi",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    .insight-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.title("🛒 Gelişmiş Market Sepeti Analizi")
st.markdown("**İleri Seviye Market Basket Analysis Uygulaması**")
st.markdown("---")

# Yan menü
st.sidebar.title("📋 Analiz Menüsü")
st.sidebar.markdown("*Gelişmiş özelliklerle donatılmış analiz platformu*")

sayfa = st.sidebar.selectbox(
    "Analiz Modülü Seçin:",
    [
        "🏠 Ana Sayfa & İstatistikler",
        "📊 Veri Keşfi & Görselleştirme", 
        "🔍 Tek & Çift Ürün Analizi",
        "🎯 3'lü Kombinasyon Analizi",  # YENİ
        "🔗 Network Analizi (Ağ Grafiği)",  # YENİ
        "📋 Gelişmiş Kural Analizi",
        "🎲 Sepet Segmentasyonu",  # YENİ
        "⚖️ Negatif Birliktelikler",  # YENİ
        "🚀 Akıllı Öneri Sistemi"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **İpucu:** Her modül farklı analiz perspektifi sunar!")

@st.cache_data
def veri_yukle():
    """Veriyi yükler ve işler"""
    try:
        veri = pd.read_csv('data/basket_analysis.csv', index_col=0)
        
        # Sepetleri oluştur
        sepetler = []
        for i, satir in veri.iterrows():
            sepet = []
            for urun in veri.columns:
                if satir[urun] == True or satir[urun] == 'True':
                    sepet.append(urun)
            if sepet:
                sepetler.append(sepet)
        
        return veri, sepetler
    except FileNotFoundError:
        st.error("❌ data/basket_analysis.csv dosyası bulunamadı!")
        return None, None

def urun_sayilarini_hesapla(sepetler):
    """Her ürünün kaç sepette olduğunu hesaplar"""
    urun_sayilari = {}
    for sepet in sepetler:
        for urun in sepet:
            urun_sayilari[urun] = urun_sayilari.get(urun, 0) + 1
    return urun_sayilari

def birliktelik_hesapla(sepetler, min_support=0.05):
    """İki ürün birlikteliklerini hesaplar"""
    toplam_sepet = len(sepetler)
    min_sepet_sayisi = int(min_support * toplam_sepet)
    
    birliktelik_sayilari = {}
    
    for sepet in sepetler:
        if len(sepet) >= 2:
            for urun1, urun2 in combinations(sepet, 2):
                if urun1 > urun2:
                    urun1, urun2 = urun2, urun1
                
                cift = (urun1, urun2)
                birliktelik_sayilari[cift] = birliktelik_sayilari.get(cift, 0) + 1
    
    # Minimum desteği geçenleri filtrele
    onemli_birliktelikler = {}
    for cift, sayi in birliktelik_sayilari.items():
        if sayi >= min_sepet_sayisi:
            support = sayi / toplam_sepet
            onemli_birliktelikler[cift] = {
                'sepet_sayisi': sayi,
                'support': support
            }
    
    return onemli_birliktelikler

def uclu_kombinasyon_hesapla(sepetler, min_support=0.03):
    """3'lü ürün kombinasyonlarını hesaplar - İLERİ SEVİYE"""
    toplam_sepet = len(sepetler)
    min_sepet_sayisi = int(min_support * toplam_sepet)
    
    uclu_sayilari = {}
    
    for sepet in sepetler:
        if len(sepet) >= 3:
            for urun1, urun2, urun3 in combinations(sepet, 3):
                # Alfabetik sıraya koy
                uclu = tuple(sorted([urun1, urun2, urun3]))
                uclu_sayilari[uclu] = uclu_sayilari.get(uclu, 0) + 1
    
    # Minimum desteği geçenleri filtrele
    onemli_uclular = {}
    for uclu, sayi in uclu_sayilari.items():
        if sayi >= min_sepet_sayisi:
            support = sayi / toplam_sepet
            onemli_uclular[uclu] = {
                'sepet_sayisi': sayi,
                'support': support
            }
    
    return onemli_uclular

def kural_olustur(birliktelikler, urun_sayilari, toplam_sepet, min_confidence=0.3):
    """Association rules oluşturur"""
    kurallar = []
    
    for (urun1, urun2), bilgi in birliktelikler.items():
        birlikte_sayi = bilgi['sepet_sayisi']
        
        # Kural 1: urun1 → urun2
        confidence1 = birlikte_sayi / urun_sayilari[urun1]
        if confidence1 >= min_confidence:
            lift1 = confidence1 / (urun_sayilari[urun2] / toplam_sepet)
            kurallar.append({
                'antecedent': urun1,
                'consequent': urun2,
                'support': bilgi['support'],
                'confidence': confidence1,
                'lift': lift1
            })
        
        # Kural 2: urun2 → urun1
        confidence2 = birlikte_sayi / urun_sayilari[urun2]
        if confidence2 >= min_confidence:
            lift2 = confidence2 / (urun_sayilari[urun1] / toplam_sepet)
            kurallar.append({
                'antecedent': urun2,
                'consequent': urun1,
                'support': bilgi['support'],
                'confidence': confidence2,
                'lift': lift2
            })
    
    return sorted(kurallar, key=lambda x: x['confidence'], reverse=True)

def negatif_birliktelik_hesapla(sepetler, urun_sayilari):
    """Negatif birliktelikleri bulur - birlikte alınMAyan ürünler"""
    toplam_sepet = len(sepetler)
    tum_urunler = list(urun_sayilari.keys())
    
    # Beklenen vs gerçek birliktelikleri karşılaştır
    negatif_ciftler = []
    
    for urun1, urun2 in combinations(tum_urunler, 2):
        if urun1 > urun2:
            urun1, urun2 = urun2, urun1
        
        # Gerçek birlikte alım sayısı
        birlikte_sayi = 0
        for sepet in sepetler:
            if urun1 in sepet and urun2 in sepet:
                birlikte_sayi += 1
        
        # Beklenen birlikte alım (bağımsızlık varsayımı)
        beklenen = (urun_sayilari[urun1] / toplam_sepet) * (urun_sayilari[urun2] / toplam_sepet) * toplam_sepet
        
        # Lift hesapla
        if birlikte_sayi > 0:
            gercek_support = birlikte_sayi / toplam_sepet
            urun1_support = urun_sayilari[urun1] / toplam_sepet
            urun2_support = urun_sayilari[urun2] / toplam_sepet
            lift = gercek_support / (urun1_support * urun2_support)
            
            # Negatif birliktelik: Lift < 0.8 (beklenenin %80'inden az)
            if lift < 0.8 and birlikte_sayi >= 5:  # En az 5 sepette görülmüş olsun
                negatif_ciftler.append({
                    'urun1': urun1,
                    'urun2': urun2,
                    'gercek_sayi': birlikte_sayi,
                    'beklenen_sayi': beklenen,
                    'lift': lift,
                    'fark': beklenen - birlikte_sayi
                })
    
    # Farka göre sırala (en büyük fark = en güçlü negatif ilişki)
    return sorted(negatif_ciftler, key=lambda x: x['fark'], reverse=True)

def sepet_segmentleri_analiz_et(sepetler):
    """Sepetleri büyüklüklerine göre segmentlere ayırır"""
    sepet_boyutlari = [len(sepet) for sepet in sepetler]
    
    # Kuartillere göre segmentler
    q1 = np.percentile(sepet_boyutlari, 25)
    q2 = np.percentile(sepet_boyutlari, 50)
    q3 = np.percentile(sepet_boyutlari, 75)
    
    segmentler = {
        'Küçük Sepetler': [],
        'Orta Sepetler': [],
        'Büyük Sepetler': [],
        'Mega Sepetler': []
    }
    
    for sepet in sepetler:
        boyut = len(sepet)
        if boyut <= q1:
            segmentler['Küçük Sepetler'].append(sepet)
        elif boyut <= q2:
            segmentler['Orta Sepetler'].append(sepet)
        elif boyut <= q3:
            segmentler['Büyük Sepetler'].append(sepet)
        else:
            segmentler['Mega Sepetler'].append(sepet)
    
    return segmentler, (q1, q2, q3)

# Veriyi yükle
veri, sepetler = veri_yukle()

if veri is not None and sepetler is not None:
    urun_sayilari = urun_sayilarini_hesapla(sepetler)
    
    # ============ ANA SAYFA ============
    if sayfa == "🏠 Ana Sayfa & İstatistikler":
        st.header("📊 Detaylı Veri İstatistikleri")
        
        # Üst metrikler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🛒 Toplam Sepet", len(sepetler))
        
        with col2:
            st.metric("📦 Ürün Çeşidi", len(urun_sayilari))
        
        with col3:
            ortalama_urun = np.mean([len(sepet) for sepet in sepetler])
            st.metric("📊 Ort. Ürün/Sepet", f"{ortalama_urun:.2f}")
        
        with col4:
            toplam_islem = sum([len(sepet) for sepet in sepetler])
            st.metric("💰 Toplam İşlem", f"{toplam_islem:,}")
        
        st.markdown("---")
        
        # Sepet dağılımı analizi
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Sepet Büyüklüğü Dağılımı")
            sepet_boyutlari = [len(sepet) for sepet in sepetler]
            
            fig = px.histogram(
                x=sepet_boyutlari,
                nbins=20,
                title="Sepetlerdeki Ürün Sayısı Dağılımı",
                labels={'x': 'Ürün Sayısı', 'y': 'Sepet Sayısı'},
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # İstatistikler
            st.markdown(f"""
            **Dağılım İstatistikleri:**
            - Minimum: {min(sepet_boyutlari)} ürün
            - Q1 (25%): {np.percentile(sepet_boyutlari, 25):.0f} ürün
            - Medyan: {np.median(sepet_boyutlari):.0f} ürün
            - Q3 (75%): {np.percentile(sepet_boyutlari, 75):.0f} ürün
            - Maximum: {max(sepet_boyutlari)} ürün
            - Std. Sapma: {np.std(sepet_boyutlari):.2f}
            """)
        
        with col2:
            st.subheader("🏆 Top 10 Popüler Ürün")
            
            sorted_urunler = sorted(urun_sayilari.items(), key=lambda x: x[1], reverse=True)[:10]
            urun_isimleri = [item[0] for item in sorted_urunler]
            urun_sayilari_list = [item[1] for item in sorted_urunler]
            yuzdeler = [(sayi/len(sepetler))*100 for sayi in urun_sayilari_list]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=urun_sayilari_list,
                    y=urun_isimleri,
                    orientation='h',
                    marker_color=yuzdeler,
                    marker_colorscale='Viridis',
                    text=[f'{y:.1f}%' for y in yuzdeler],
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="En Çok Satılan Ürünler",
                xaxis_title="Sepet Sayısı",
                yaxis_title="",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Teorik bilgiler
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📖 Market Basket Analysis")
            st.markdown("""
            Market Basket Analysis, müşteri satın alma davranışlarını anlamak için kullanılan 
            güçlü bir veri madenciliği tekniğidir.
            
            **Temel Kavramlar:**
            
            - **Support (Destek):** Bir item'ın veya item kombinasyonunun tüm işlemlerdeki oranı
              - Formül: `Support(X) = n(X) / N`
              - Örnek: Eğer 1000 sepetten 300'ünde Milk varsa, Support(Milk) = 0.30
            
            - **Confidence (Güven):** X alındığında Y'nin de alınma olasılığı
              - Formül: `Confidence(X→Y) = Support(X,Y) / Support(X)`
              - Örnek: Milk alanların %60'ı Bread alıyorsa, Confidence = 0.60
            
            - **Lift:** İki ürünün birlikteliğinin tesadüfilikten ne kadar güçlü olduğu
              - Formül: `Lift(X→Y) = Confidence(X→Y) / Support(Y)`
              - Lift > 1: Pozitif birliktelik
              - Lift = 1: Bağımsızlık
              - Lift < 1: Negatif birliktelik
            """)
        
        with col2:
            st.subheader("💡 İş Uygulamaları")
            st.markdown("""
            **1. Cross-Selling (Çapraz Satış)**
            - Birlikte alınan ürünleri tespit edin
            - Müşterilere hedefli öneriler sunun
            - Sepet büyüklüğünü artırın
            
            **2. Ürün Yerleşimi**
            - İlgili ürünleri yakın raflara yerleştirin
            - Müşteri gezinti rotasını optimize edin
            - İmpuls alışverişi teşvik edin
            
            **3. Kampanya Planlaması**
            - Birlikte satışta indirim kampanyaları
            - Bundle (paket) ürün fırsatları
            - Hedefli pazarlama stratejileri
            
            **4. Stok Yönetimi**
            - İlgili ürünlerin stoklarını birlikte planlayın
            - Talep tahmini yapın
            - Tedarik zincirini optimize edin
            
            **5. Müşteri Segmentasyonu**
            - Alışveriş davranışlarına göre müşteri grupları
            - Kişiselleştirilmiş deneyimler
            - Sadakat programları tasarımı
            """)
    
    # ============ VERİ KEŞFİ ============
    elif sayfa == "📊 Veri Keşfi & Görselleştirme":
        st.header("📊 Detaylı Veri Keşfi")
        
        tab1, tab2, tab3 = st.tabs(["📋 Ham Veri", "🎨 Isı Haritası", "📊 Korelasyon Matrisi"])
        
        with tab1:
            st.subheader("Ham Veri Görünümü")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                gosterilecek_satir = st.slider("Gösterilecek satır sayısı:", 5, 100, 20)
            with col2:
                rastgele = st.checkbox("Rastgele örnekle", value=False)
            
            if rastgele:
                st.dataframe(veri.sample(gosterilecek_satir), use_container_width=True)
            else:
                st.dataframe(veri.head(gosterilecek_satir), use_container_width=True)
            
            st.subheader("Örnek Sepetler")
            for i in range(min(5, len(sepetler))):
                with st.expander(f"Sepet {i+1} ({len(sepetler[i])} ürün)"):
                    st.write(", ".join(sepetler[i]))
        
        with tab2:
            st.subheader("🎨 Ürün Birliktelik Isı Haritası")
            st.info("Bu harita hangi ürünlerin birlikte ne sıklıkla alındığını gösterir")
            
            # Top 15 ürünü al
            sorted_urunler = sorted(urun_sayilari.items(), key=lambda x: x[1], reverse=True)[:15]
            top_urunler = [item[0] for item in sorted_urunler]
            
            # Co-occurrence matrix oluştur
            cooc_matrix = pd.DataFrame(0, index=top_urunler, columns=top_urunler)
            
            for sepet in sepetler:
                for urun1 in top_urunler:
                    if urun1 in sepet:
                        for urun2 in top_urunler:
                            if urun2 in sepet:
                                cooc_matrix.loc[urun1, urun2] += 1
            
            fig = px.imshow(
                cooc_matrix,
                labels=dict(x="Ürün", y="Ürün", color="Birlikte Alım"),
                x=top_urunler,
                y=top_urunler,
                color_continuous_scale='YlOrRd',
                aspect="auto"
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("📊 Lift Tabanlı Korelasyon Matrisi")
            st.info("Lift değerleri kullanılarak ürün ilişki gücü gösterimi")
            
            # Lift matrix oluştur
            top_urunler_15 = [item[0] for item in sorted(urun_sayilari.items(), key=lambda x: x[1], reverse=True)[:12]]
            lift_matrix = pd.DataFrame(1.0, index=top_urunler_15, columns=top_urunler_15)
            
            for urun1 in top_urunler_15:
                for urun2 in top_urunler_15:
                    if urun1 != urun2:
                        # Birlikte alım sayısı
                        birlikte = sum(1 for sepet in sepetler if urun1 in sepet and urun2 in sepet)
                        
                        if birlikte > 0:
                            support_xy = birlikte / len(sepetler)
                            support_x = urun_sayilari[urun1] / len(sepetler)
                            support_y = urun_sayilari[urun2] / len(sepetler)
                            
                            lift = support_xy / (support_x * support_y)
                            lift_matrix.loc[urun1, urun2] = lift
            
            fig = px.imshow(
                lift_matrix,
                labels=dict(x="Ürün", y="Ürün", color="Lift Değeri"),
                x=top_urunler_15,
                y=top_urunler_15,
                color_continuous_scale='RdYlGn',
                color_continuous_midpoint=1.0,
                aspect="auto"
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Lift Yorumlama:**
            - 🟢 Yeşil (>1.0): Güçlü pozitif ilişki
            - 🟡 Sarı (~1.0): Nötr/bağımsız
            - 🔴 Kırmızı (<1.0): Negatif ilişki
            """)
    
    # ============ TEK & ÇİFT ÜRÜN ANALİZİ ============
    elif sayfa == "🔍 Tek & Çift Ürün Analizi":
        st.header("🔍 Bireysel ve İkili Ürün Analizi")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Parametreler")
            min_support = st.slider(
                "Minimum Support:", 
                0.01, 0.20, 0.05, 0.01,
                help="Ürün çiftinin minimum destek oranı"
            )
            
            analiz_turu = st.radio(
                "Analiz Türü:",
                ["Tüm Çiftler", "Belirli Ürün İçin"]
            )
            
            if analiz_turu == "Belirli Ürün İçin":
                secilen_urun = st.selectbox(
                    "Ürün seçin:",
                    sorted(urun_sayilari.keys())
                )
        
        with col2:
            if st.button("🔍 Analiz Yap", type="primary"):
                birliktelikler = birliktelik_hesapla(sepetler, min_support)
                
                if birliktelikler:
                    st.success(f"✅ {len(birliktelikler)} ürün çifti bulundu!")
                    
                    # Dataframe oluştur
                    birliktelik_listesi = []
                    for (urun1, urun2), bilgi in birliktelikler.items():
                        if analiz_turu == "Tüm Çiftler" or urun1 == secilen_urun or urun2 == secilen_urun:
                            birliktelik_listesi.append({
                                'Ürün 1': urun1,
                                'Ürün 2': urun2,
                                'Sepet Sayısı': bilgi['sepet_sayisi'],
                                'Support': bilgi['support'],
                                'Support %': f"{bilgi['support']*100:.2f}%"
                            })
                    
                    df_birliktelik = pd.DataFrame(birliktelik_listesi)
                    df_birliktelik = df_birliktelik.sort_values('Sepet Sayısı', ascending=False)
                    
                    # Grafik
                    st.subheader("📊 Top 15 Ürün Çifti")
                    top_15 = df_birliktelik.head(15).copy()
                    top_15['Ürün Çifti'] = top_15['Ürün 1'] + ' + ' + top_15['Ürün 2']
                    
                    fig = px.bar(
                        top_15,
                        x='Sepet Sayısı',
                        y='Ürün Çifti',
                        orientation='h',
                        title=f'En Güçlü 15 Birliktelik (Support ≥ {min_support*100}%)',
                        color='Support',
                        color_continuous_scale='Blues',
                        hover_data=['Support %']
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detaylı tablo
                    st.subheader("📋 Detaylı Sonuçlar")
                    st.dataframe(
                        df_birliktelik,
                        use_container_width=True,
                        height=400
                    )
                    
                    # Session state'e kaydet
                    st.session_state['birliktelikler'] = birliktelikler
                    
                else:
                    st.warning("❌ Hiç birliktelik bulunamadı. Support değerini düşürün.")
    
    # ============ 3'LÜ KOMBİNASYON ANALİZİ (YENİ) ============
    elif sayfa == "🎯 3'lü Kombinasyon Analizi":
        st.header("🎯 3'lü Ürün Kombinasyonları Analizi")
        st.info("⚡ **İleri Seviye:** Bu analiz 3 ürünün birlikte alınma paternlerini ortaya çıkarır")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Parametreler")
            min_support_3 = st.slider(
                "Minimum Support:", 
                0.01, 0.15, 0.03, 0.01,
                help="3'lü kombinasyonlar için minimum destek oranı"
            )
            
            st.markdown("---")
            st.markdown("""
            **Neden 3'lü Analiz?**
            
            2'li analizden daha güçlü çünkü:
            - Daha kompleks paternler
            - Bundle stratejileri
            - Cross-category fırsatlar
            """)
        
        with col2:
            if st.button("🎯 3'lü Analiz Başlat", type="primary"):
                with st.spinner("3'lü kombinasyonlar hesaplanıyor..."):
                    uclu_kombinasyonlar = uclu_kombinasyon_hesapla(sepetler, min_support_3)
                
                if uclu_kombinasyonlar:
                    st.success(f"✅ {len(uclu_kombinasyonlar)} adet 3'lü kombinasyon bulundu!")
                    
                    # Top 20'yi göster
                    sorted_uclu = sorted(uclu_kombinasyonlar.items(), 
                                        key=lambda x: x[1]['support'], 
                                        reverse=True)[:20]
                    
                    # Görselleştirme için veri hazırla
                    uclu_data = []
                    for uclu, bilgi in sorted_uclu:
                        uclu_data.append({
                            'Kombinasyon': ' + '.join(uclu),
                            'Ürün 1': uclu[0],
                            'Ürün 2': uclu[1],
                            'Ürün 3': uclu[2],
                            'Sepet Sayısı': bilgi['sepet_sayisi'],
                            'Support': bilgi['support'],
                            'Support %': f"{bilgi['support']*100:.2f}%"
                        })
                    
                    df_uclu = pd.DataFrame(uclu_data)
                    
                    # Sunburst chart - Hiyerarşik görselleştirme
                    st.subheader("🌟 Top 15 - 3'lü Kombinasyonlar")
                    
                    fig = px.bar(
                        df_uclu.head(15),
                        x='Sepet Sayısı',
                        y='Kombinasyon',
                        orientation='h',
                        color='Support',
                        color_continuous_scale='Reds',
                        title="En Güçlü 3'lü Kombinasyonlar"
                    )
                    fig.update_layout(height=600)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detaylı tablo
                    st.subheader("📊 Detaylı 3'lü Kombinasyon Tablosu")
                    st.dataframe(df_uclu, use_container_width=True, height=400)
                    
                    # En güçlü kombinasyon analizi
                    st.subheader("🏆 En Güçlü Kombinasyon Analizi")
                    en_guclu = sorted_uclu[0]
                    uclu, bilgi = en_guclu
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Sepet Sayısı", bilgi['sepet_sayisi'])
                    with col_b:
                        st.metric("Support Oranı", f"{bilgi['support']*100:.2f}%")
                    with col_c:
                        toplam_musteri_etkisi = (bilgi['support'] * len(sepetler))
                        st.metric("Müşteri Etkisi", f"~{int(toplam_musteri_etkisi)}")
                    
                    st.markdown(f"""
                    <div class="insight-box">
                    <h4>💡 İş Önerisi: {' + '.join(uclu)}</h4>
                    <p><strong>Bu 3 ürün sepetlerin %{bilgi['support']*100:.1f}'inde birlikte görülüyor!</strong></p>
                    <ul>
                        <li>📦 <strong>Bundle Fırsatı:</strong> Bu 3 ürünü paket halinde %15 indirimle sunun</li>
                        <li>🏪 <strong>Raf Yerleşimi:</strong> Bu ürünleri aynı koridora yerleştirin</li>
                        <li>🎁 <strong>Kampanya:</strong> "3 al 2 öde" kampanyası düzenleyin</li>
                        <li>📧 <strong>E-posta Pazarlama:</strong> Bu kombinasyonu alan müşterilere özel teklifler</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Session'a kaydet
                    st.session_state['uclu_kombinasyonlar'] = uclu_kombinasyonlar
                    
                else:
                    st.warning("❌ 3'lü kombinasyon bulunamadı. Support değerini düşürün.")
    
    # ============ NETWORK ANALİZİ (YENİ) ============
    elif sayfa == "🔗 Network Analizi (Ağ Grafiği)":
        st.header("🔗 Ürün İlişki Ağı Görselleştirmesi")
        st.info("🎨 **Görsel Analiz:** Ürünler arası ilişkileri ağ grafiği olarak görün")
        
        # Parametreler
        col1, col2, col3 = st.columns(3)
        with col1:
            min_support_net = st.slider("Min Support:", 0.02, 0.15, 0.05, 0.01)
        with col2:
            min_lift = st.slider("Min Lift:", 1.0, 3.0, 1.2, 0.1)
        with col3:
            max_nodes = st.slider("Max Ürün Sayısı:", 5, 20, 12, 1)
        
        if st.button("🔗 Network Grafiği Oluştur", type="primary"):
            with st.spinner("Network grafiği hazırlanıyor..."):
                # En popüler ürünleri al
                sorted_urunler = sorted(urun_sayilari.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
                secili_urunler = [item[0] for item in sorted_urunler]
                
                # Graph oluştur
                G = nx.Graph()
                
                # Node'ları ekle
                for urun in secili_urunler:
                    G.add_node(urun, size=urun_sayilari[urun])
                
                # Edge'leri ekle (birlikteliklere göre)
                for sepet in sepetler:
                    sepetteki_secili = [u for u in sepet if u in secili_urunler]
                    if len(sepetteki_secili) >= 2:
                        for u1, u2 in combinations(sepetteki_secili, 2):
                            if G.has_edge(u1, u2):
                                G[u1][u2]['weight'] += 1
                            else:
                                G.add_edge(u1, u2, weight=1)
                
                # Lift hesapla ve zayıf bağlantıları kaldır
                edges_to_remove = []
                for u1, u2, data in G.edges(data=True):
                    birlikte_sayi = data['weight']
                    support_xy = birlikte_sayi / len(sepetler)
                    support_x = urun_sayilari[u1] / len(sepetler)
                    support_y = urun_sayilari[u2] / len(sepetler)
                    lift = support_xy / (support_x * support_y)
                    
                    if support_xy < min_support_net or lift < min_lift:
                        edges_to_remove.append((u1, u2))
                    else:
                        G[u1][u2]['lift'] = lift
                        G[u1][u2]['support'] = support_xy
                
                for edge in edges_to_remove:
                    G.remove_edge(*edge)
                
                # Plotly ile görselleştir
                pos = nx.spring_layout(G, k=2, iterations=50)
                
                # Edge traces
                edge_traces = []
                for edge in G.edges(data=True):
                    u1, u2, data = edge
                    x0, y0 = pos[u1]
                    x1, y1 = pos[u2]
                    
                    # Lift'e göre renk ve kalınlık
                    lift = data.get('lift', 1.0)
                    width = min(10, lift * 2)
                    
                    edge_trace = go.Scatter(
                        x=[x0, x1, None],
                        y=[y0, y1, None],
                        mode='lines',
                        line=dict(width=width, color=f'rgba(100,100,250,{min(1, lift/3)})'),
                        hoverinfo='text',
                        text=f"{u1} ↔ {u2}<br>Lift: {lift:.2f}<br>Support: {data['support']*100:.1f}%",
                        showlegend=False
                    )
                    edge_traces.append(edge_trace)
                
                # Node trace
                node_x = []
                node_y = []
                node_text = []
                node_size = []
                
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    
                    # Node büyüklüğü support oranına göre
                    size = (urun_sayilari[node] / len(sepetler)) * 1000
                    node_size.append(size)
                    
                    # Hover text
                    connections = len(list(G.neighbors(node)))
                    node_text.append(f"{node}<br>Sepet: {urun_sayilari[node]}<br>Bağlantı: {connections}")
                
                node_trace = go.Scatter(
                    x=node_x,
                    y=node_y,
                    mode='markers+text',
                    text=[node for node in G.nodes()],
                    textposition="top center",
                    hovertext=node_text,
                    hoverinfo='text',
                    marker=dict(
                        size=node_size,
                        color='#FF6B6B',
                        line=dict(width=2, color='white')
                    ),
                    showlegend=False
                )
                
                # Figure oluştur
                fig = go.Figure(data=edge_traces + [node_trace])
                fig.update_layout(
                    title=f"Ürün İlişki Ağı (Support≥{min_support_net*100}%, Lift≥{min_lift})",
                    showlegend=False,
                    hovermode='closest',
                    height=700,
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    plot_bgcolor='rgba(240,240,240,0.5)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Network metrikleri
                st.subheader("📊 Ağ Metrikleri")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Toplam Node", G.number_of_nodes())
                with col2:
                    st.metric("Toplam Bağlantı", G.number_of_edges())
                with col3:
                    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
                    st.metric("Ort. Bağlantı", f"{avg_degree:.1f}")
                with col4:
                    density = nx.density(G)
                    st.metric("Ağ Yoğunluğu", f"{density:.2%}")
                
                # En merkezi ürünler
                st.subheader("🎯 En Merkezi Ürünler (Hub Products)")
                degree_cent = nx.degree_centrality(G)
                sorted_central = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]
                
                for i, (urun, cent) in enumerate(sorted_central, 1):
                    st.write(f"{i}. **{urun}** - Merkezilik: {cent:.2%} (Diğer {len(list(G.neighbors(urun)))} ürünle bağlantılı)")
    
    # ============ GELİŞMİŞ KURAL ANALİZİ ============
    elif sayfa == "📋 Gelişmiş Kural Analizi":
        st.header("📋 Gelişmiş Association Rules Analizi")
        
        if 'birliktelikler' not in st.session_state:
            st.warning("⚠️ Önce 'Tek & Çift Ürün Analizi' yapmalısınız!")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_confidence = st.slider("Min Confidence:", 0.1, 0.9, 0.3, 0.05)
            with col2:
                min_lift = st.slider("Min Lift:", 0.5, 3.0, 1.0, 0.1)
            with col3:
                siralama = st.selectbox("Sıralama:", ["Confidence", "Lift", "Support"])
            
            if st.button("📋 Kural Analizi Yap", type="primary"):
                birliktelikler = st.session_state['birliktelikler']
                kurallar = kural_olustur(birliktelikler, urun_sayilari, len(sepetler), min_confidence)
                
                # Lift filtrele
                kurallar = [k for k in kurallar if k['lift'] >= min_lift]
                
                # Sırala
                if siralama == "Lift":
                    kurallar = sorted(kurallar, key=lambda x: x['lift'], reverse=True)
                elif siralama == "Support":
                    kurallar = sorted(kurallar, key=lambda x: x['support'], reverse=True)
                # Confidence zaten sıralı
                
                if kurallar:
                    st.success(f"✅ {len(kurallar)} kural bulundu!")
                    
                    # Kural dağılımı
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Confidence Dağılımı")
                        confidence_values = [k['confidence'] for k in kurallar]
                        fig = px.histogram(
                            x=confidence_values,
                            nbins=20,
                            title="Kuralların Confidence Dağılımı",
                            labels={'x': 'Confidence', 'y': 'Kural Sayısı'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("📊 Lift Dağılımı")
                        lift_values = [k['lift'] for k in kurallar]
                        fig = px.histogram(
                            x=lift_values,
                            nbins=20,
                            title="Kuralların Lift Dağılımı",
                            labels={'x': 'Lift', 'y': 'Kural Sayısı'},
                            color_discrete_sequence=['#FF6B6B']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Scatter plot: Confidence vs Lift
                    st.subheader("🎯 Support-Confidence-Lift İlişkisi")
                    
                    kural_df = pd.DataFrame([
                        {
                            'Kural': f"{k['antecedent']} → {k['consequent']}",
                            'Confidence': k['confidence'],
                            'Lift': k['lift'],
                            'Support': k['support'],
                            'Support %': k['support'] * 100
                        }
                        for k in kurallar[:50]  # İlk 50 kural
                    ])
                    
                    fig = px.scatter(
                        kural_df,
                        x='Confidence',
                        y='Lift',
                        size='Support %',
                        hover_data=['Kural'],
                        title="Kural Analizi: Confidence vs Lift (Bubble size = Support)",
                        color='Lift',
                        color_continuous_scale='Viridis'
                    )
                    fig.add_hline(y=1.0, line_dash="dash", line_color="red", 
                                 annotation_text="Lift = 1 (Bağımsızlık)")
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Top kurallar tablosu
                    st.subheader("🏆 En Güçlü Kurallar")
                    
                    kural_listesi = []
                    for i, kural in enumerate(kurallar[:30], 1):
                        kural_listesi.append({
                            '#': i,
                            'Öncül': kural['antecedent'],
                            '→': '→',
                            'Sonuç': kural['consequent'],
                            'Support': f"{kural['support']*100:.2f}%",
                            'Confidence': f"{kural['confidence']*100:.2f}%",
                            'Lift': f"{kural['lift']:.2f}",
                            'Kategori': '🔥 Güçlü' if kural['lift'] > 1.5 else '✅ İyi' if kural['lift'] > 1.2 else '⚠️ Zayıf'
                        })
                    
                    df_kurallar = pd.DataFrame(kural_listesi)
                    st.dataframe(df_kurallar, use_container_width=True, height=500)
                    
                    # En güçlü 3 kural açıklaması
                    st.subheader("💡 Top 3 Kural Yorumu")
                    for i, kural in enumerate(kurallar[:3], 1):
                        with st.expander(f"🏆 Kural {i}: {kural['antecedent']} → {kural['consequent']}"):
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Support", f"{kural['support']*100:.1f}%")
                            with col_b:
                                st.metric("Confidence", f"{kural['confidence']*100:.1f}%")
                            with col_c:
                                st.metric("Lift", f"{kural['lift']:.2f}")
                            
                            st.markdown(f"""
                            **📖 Yorum:**
                            - {kural['antecedent']} alan müşterilerin **%{kural['confidence']*100:.0f}'i** {kural['consequent']} da alıyor
                            - Bu birliktelik tesadüften **{kural['lift']:.1f} kat** daha güçlü
                            - Bu iki ürün sepetlerin **%{kural['support']*100:.1f}'inde** birlikte görülüyor
                            
                            **💼 İş Önerisi:**
                            1. {kural['antecedent']} satın alanlara {kural['consequent']} önerin
                            2. Bu ürünlerde bundle kampanya yapın
                            3. Mağazada bu ürünleri yakın konumlara yerleştirin
                            """)
                    
                    st.session_state['kurallar'] = kurallar
                    
                else:
                    st.warning("❌ Kural bulunamadı. Parametreleri gevşetin.")
    
    # ============ SEPET SEGMENTASYONU (YENİ) ============
    elif sayfa == "🎲 Sepet Segmentasyonu":
        st.header("🎲 Sepet Büyüklüğüne Göre Segmentasyon")
        st.info("🔍 Farklı sepet büyüklüklerindeki müşteri davranışlarını analiz edin")
        
        # Segmentleri hesapla
        segmentler, kuartiller = sepet_segmentleri_analiz_et(sepetler)
        q1, q2, q3 = kuartiller
        
        # Genel bakış
        st.subheader("📊 Segment Dağılımı")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🛍️ Küçük Sepetler",
                len(segmentler['Küçük Sepetler']),
                f"≤{int(q1)} ürün"
            )
        
        with col2:
            st.metric(
                "📦 Orta Sepetler",
                len(segmentler['Orta Sepetler']),
                f"{int(q1)+1}-{int(q2)} ürün"
            )
        
        with col3:
            st.metric(
                "🛒 Büyük Sepetler",
                len(segmentler['Büyük Sepetler']),
                f"{int(q2)+1}-{int(q3)} ürün"
            )
        
        with col4:
            st.metric(
                "🎁 Mega Sepetler",
                len(segmentler['Mega Sepetler']),
                f">{int(q3)} ürün"
            )
        
        # Segment analizi
        st.markdown("---")
        secili_segment = st.selectbox(
            "Detaylı analiz için segment seçin:",
            list(segmentler.keys())
        )
        
        if st.button("🔍 Segment Analizi Yap", type="primary"):
            segment_sepetleri = segmentler[secili_segment]
            
            if segment_sepetleri:
                st.subheader(f"📊 {secili_segment} Analizi ({len(segment_sepetleri)} sepet)")
                
                # Bu segmentteki ürün popülaritesi
                segment_urun_sayilari = urun_sayilarini_hesapla(segment_sepetleri)
                sorted_segment_urunler = sorted(segment_urun_sayilari.items(), 
                                               key=lambda x: x[1], reverse=True)[:15]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Top 15 Ürün (Bu Segmentte)**")
                    urun_isimleri = [item[0] for item in sorted_segment_urunler]
                    urun_sayilari_list = [item[1] for item in sorted_segment_urunler]
                    
                    fig = px.bar(
                        x=urun_sayilari_list,
                        y=urun_isimleri,
                        orientation='h',
                        title=f"{secili_segment} - Popüler Ürünler",
                        labels={'x': 'Sepet Sayısı', 'y': ''},
                        color=urun_sayilari_list,
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(showlegend=False, height=500)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Genel popülariteyle karşılaştırma
                    st.markdown("**Genel Popülariteyle Karşılaştırma**")
                    
                    karsilastirma_data = []
                    for urun, segment_sayi in sorted_segment_urunler[:10]:
                        genel_sayi = urun_sayilari.get(urun, 0)
                        segment_oran = (segment_sayi / len(segment_sepetleri)) * 100
                        genel_oran = (genel_sayi / len(sepetler)) * 100
                        fark = segment_oran - genel_oran
                        
                        karsilastirma_data.append({
                            'Ürün': urun,
                            'Segment %': segment_oran,
                            'Genel %': genel_oran,
                            'Fark': fark
                        })
                    
                    df_karsilastirma = pd.DataFrame(karsilastirma_data)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Bu Segment',
                        x=df_karsilastirma['Ürün'],
                        y=df_karsilastirma['Segment %'],
                        marker_color='#FF6B6B'
                    ))
                    fig.add_trace(go.Bar(
                        name='Genel Ortalama',
                        x=df_karsilastirma['Ürün'],
                        y=df_karsilastirma['Genel %'],
                        marker_color='#4ECDC4'
                    ))
                    
                    fig.update_layout(
                        title="Segment vs Genel Popülarite",
                        barmode='group',
                        height=500,
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # En çok değişen ürünler
                st.subheader("🔥 Bu Segmente Özel Ürünler")
                df_sorted = df_karsilastirma.sort_values('Fark', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📈 Bu Segmentte Daha Popüler**")
                    for i, row in df_sorted.head(5).iterrows():
                        st.write(f"• **{row['Ürün']}**: +{row['Fark']:.1f}% fark")
                
                with col2:
                    st.markdown("**📉 Bu Segmentte Daha Az Popüler**")
                    for i, row in df_sorted.tail(5).iterrows():
                        st.write(f"• **{row['Ürün']}**: {row['Fark']:.1f}% fark")
                
                # İş önerileri
                st.markdown("---")
                st.subheader("💡 Segment-Spesifik İş Önerileri")
                
                if secili_segment == "Küçük Sepetler":
                    st.markdown("""
                    <div class="insight-box">
                    <h4>🛍️ Küçük Sepet Stratejileri</h4>
                    <ul>
                        <li><strong>Hızlı alışveriş deneyimi:</strong> Express kasa</li>
                        <li><strong>İmpuls ürünler:</strong> Kasa önü ürün yerleşimi</li>
                        <li><strong>Combo teklifleri:</strong> "2. ürüne %50 indirim"</li>
                        <li><strong>Minimum tutar kampanyaları:</strong> Sepeti büyütme teşvikleri</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif secili_segment == "Mega Sepetler":
                    st.markdown("""
                    <div class="insight-box">
                    <h4>🎁 Mega Sepet Stratejileri</h4>
                    <ul>
                        <li><strong>Sadakat programı:</strong> Bu müşterileri ödüllendirin</li>
                        <li><strong>Toplu alım indirimleri:</strong> "100 TL üzeri %10"</li>
                        <li><strong>Premium hizmetler:</strong> Ücretsiz teslimat</li>
                        <li><strong>Kişisel alışveriş asistanı:</strong> VIP müşteri deneyimi</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    st.markdown("""
                    <div class="insight-box">
                    <h4>📦 Orta/Büyük Sepet Stratejileri</h4>
                    <ul>
                        <li><strong>Cross-selling:</strong> İlgili ürün önerileri</li>
                        <li><strong>Kategori kampanyaları:</strong> "Gıda ürünlerinde %15"</li>
                        <li><strong>Sepet analizi:</strong> Eksik ürünleri tespit edin</li>
                        <li><strong>E-posta pazarlama:</strong> Kişiselleştirilmiş teklifler</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ============ NEGATİF BİRLİKTELİKLER (YENİ) ============
    elif sayfa == "⚖️ Negatif Birliktelikler":
        st.header("⚖️ Negatif Birliktelik Analizi")
        st.info("🔍 **İlginç Keşif:** Hangi ürünler birlikte alınMIYOR?")
        
        st.markdown("""
        **Negatif birliktelik nedir?**
        
        Bazı ürün çiftleri tesadüfi olarak beklenenden **daha az** birlikte alınır. 
        Bu durum şu sebeplerden olabilir:
        - Ürünler birbirinin alternatifi (Coca Cola vs Pepsi)
        - Farklı müşteri segmentleri (Bebek ürünleri vs Alkol)
        - Tamamlayıcı olmayan kategoriler (Et vs Vejetaryen ürünler)
        
        **Lift < 1.0** olan ürün çiftleri negatif birliktelik gösterir.
        """)
        
        if st.button("⚖️ Negatif Birliktelikleri Bul", type="primary"):
            with st.spinner("Negatif birliktelikler hesaplanıyor..."):
                negatif_ciftler = negatif_birliktelik_hesapla(sepetler, urun_sayilari)
            
            if negatif_ciftler:
                st.success(f"✅ {len(negatif_ciftler)} negatif birliktelik bulundu!")
                
                # Top 20
                top_negatif = negatif_ciftler[:20]
                
                # Görselleştirme
                df_negatif = pd.DataFrame([
                    {
                        'Ürün Çifti': f"{item['urun1']} vs {item['urun2']}",
                        'Ürün 1': item['urun1'],
                        'Ürün 2': item['urun2'],
                        'Gerçek Sayı': item['gercek_sayi'],
                        'Beklenen Sayı': f"{item['beklenen_sayi']:.1f}",
                        'Lift': f"{item['lift']:.3f}",
                        'Fark': f"{item['fark']:.1f}"
                    }
                    for item in top_negatif
                ])
                
                # Bar chart
                st.subheader("📊 En Güçlü Negatif Birliktelikler")
                
                lift_values = [item['lift'] for item in top_negatif]
                urun_ciftleri = [f"{item['urun1']} vs {item['urun2']}" for item in top_negatif]
                
                fig = px.bar(
                    x=lift_values,
                    y=urun_ciftleri,
                    orientation='h',
                    title="Negatif Birliktelik Gücü (Lift Değerleri)",
                    labels={'x': 'Lift Değeri', 'y': ''},
                    color=lift_values,
                    color_continuous_scale='Reds_r'
                )
                fig.add_vline(x=1.0, line_dash="dash", line_color="green", 
                             annotation_text="Bağımsızlık (Lift=1)")
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
                
                # Detaylı tablo
                st.subheader("📋 Detaylı Negatif Birliktelik Tablosu")
                st.dataframe(df_negatif, use_container_width=True, height=400)
                
                # En güçlü negatif birliktelik açıklaması
                st.subheader("💡 En Güçlü Negatif İlişki")
                en_guclu_negatif = negatif_ciftler[0]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gerçek Birlikte Alım", en_guclu_negatif['gercek_sayi'])
                with col2:
                    st.metric("Beklenen Alım", f"{en_guclu_negatif['beklenen_sayi']:.0f}")
                with col3:
                    st.metric("Lift", f"{en_guclu_negatif['lift']:.3f}")
                
                st.markdown(f"""
                <div class="insight-box">
                <h4>🔍 Analiz: {en_guclu_negatif['urun1']} vs {en_guclu_negatif['urun2']}</h4>
                <p><strong>Bu iki ürün beklenenden {en_guclu_negatif['fark']:.0f} daha az birlikte alınıyor!</strong></p>
                
                <p><strong>Olası Sebepler:</strong></p>
                <ul>
                    <li>🔄 <strong>Alternatif ürünler:</strong> Müşteriler birini seçiyor</li>
                    <li>👥 <strong>Farklı segmentler:</strong> Farklı müşteri grupları tercih ediyor</li>
                    <li>🏷️ <strong>Kategori ayrımı:</strong> Birbirini tamamlamıyor</li>
                </ul>
                
                <p><strong>💼 İş İçgörüleri:</strong></p>
                <ul>
                    <li>Bu ürünleri ayrı kampanyalarda değerlendirin</li>
                    <li>Farklı müşteri segmentlerine hitap ettiklerini kabul edin</li>
                    <li>Mağaza yerleşiminde farklı bölgelere koyun</li>
                    <li>Bundle kampanyası yapmayın</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.info("Belirgin negatif birliktelik bulunamadı.")
    
    # ============ AKILLI ÖNERİ SİSTEMİ ============
    elif sayfa == "🚀 Akıllı Öneri Sistemi":
        st.header("🚀 Gelişmiş Ürün Öneri Sistemi")
        
        if 'kurallar' not in st.session_state:
            st.warning("⚠️ Önce 'Gelişmiş Kural Analizi' yapmalısınız!")
        else:
            kurallar = st.session_state['kurallar']
            
            st.subheader("🛒 Sepet Simülasyonu")
            st.info("💡 Müşteri sepetine ürün ekleyin, sistem size akıllı öneriler sunsun!")
            
            # Çoklu ürün seçimi
            tum_urunler = sorted(urun_sayilari.keys())
            secili_urunler = st.multiselect(
                "Sepete ürün ekleyin:",
                tum_urunler,
                default=[]
            )
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                oneri_sayisi = st.slider("Gösterilecek öneri sayısı:", 3, 15, 8)
            
            with col2:
                min_confidence_oneri = st.slider("Min Confidence:", 0.1, 0.9, 0.2, 0.05)
            
            if secili_urunler and st.button("🎯 Öneri Getir", type="primary"):
                # Tüm seçili ürünler için kuralları topla
                tum_oneriler = {}
                
                for secili_urun in secili_urunler:
                    uygun_kurallar = [k for k in kurallar 
                                     if k['antecedent'] == secili_urun 
                                     and k['confidence'] >= min_confidence_oneri
                                     and k['consequent'] not in secili_urunler]
                    
                    for kural in uygun_kurallar:
                        urun = kural['consequent']
                        if urun not in tum_oneriler:
                            tum_oneriler[urun] = {
                                'max_confidence': kural['confidence'],
                                'max_lift': kural['lift'],
                                'kaynak_urunler': [secili_urun],
                                'skor': kural['confidence'] * kural['lift']
                            }
                        else:
                            # Birden fazla ürünle ilişkiliyse, en iyi skorları güncelle
                            tum_oneriler[urun]['max_confidence'] = max(
                                tum_oneriler[urun]['max_confidence'], 
                                kural['confidence']
                            )
                            tum_oneriler[urun]['max_lift'] = max(
                                tum_oneriler[urun]['max_lift'], 
                                kural['lift']
                            )
                            tum_oneriler[urun]['kaynak_urunler'].append(secili_urun)
                            tum_oneriler[urun]['skor'] += kural['confidence'] * kural['lift']
                
                if tum_oneriler:
                    # Skora göre sırala
                    sorted_oneriler = sorted(tum_oneriler.items(), 
                                           key=lambda x: x[1]['skor'], 
                                           reverse=True)[:oneri_sayisi]
                    
                    st.success(f"✅ {len(sorted_oneriler)} öneri bulundu!")
                    
                    # Önerileri göster
                    st.subheader("🎁 Size Özel Öneriler")
                    
                    col1, col2 = st.columns([2, 3])
                    
                    with col1:
                        for i, (urun, bilgi) in enumerate(sorted_oneriler, 1):
                            with st.container():
                                st.markdown(f"""
                                <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #2196f3;">
                                    <h4>{i}. {urun}</h4>
                                    <p><strong>Öneri Skoru:</strong> {bilgi['skor']:.2f}</p>
                                    <p><strong>Max Confidence:</strong> {bilgi['max_confidence']*100:.1f}%</p>
                                    <p><strong>Max Lift:</strong> {bilgi['max_lift']:.2f}</p>
                                    <p><strong>İlgili ürünler:</strong> {', '.join(bilgi['kaynak_urunler'][:3])}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**Öneri Gücü Grafiği**")
                        
                        oneri_df = pd.DataFrame([
                            {
                                'Ürün': urun,
                                'Öneri Skoru': bilgi['skor'],
                                'Confidence': bilgi['max_confidence'],
                                'Lift': bilgi['max_lift'],
                                'İlişkili Sayı': len(bilgi['kaynak_urunler'])
                            }
                            for urun, bilgi in sorted_oneriler
                        ])
                        
                        fig = px.scatter(
                            oneri_df,
                            x='Confidence',
                            y='Lift',
                            size='Öneri Skoru',
                            color='İlişkili Sayı',
                            hover_data=['Ürün'],
                            title="Öneri Analizi: Confidence vs Lift",
                            color_continuous_scale='Viridis'
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Bar chart
                        fig2 = px.bar(
                            oneri_df,
                            x='Öneri Skoru',
                            y='Ürün',
                            orientation='h',
                            title="Öneri Sıralaması",
                            color='Öneri Skoru',
                            color_continuous_scale='Blues'
                        )
                        fig2.update_layout(height=400)
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    # İş stratejisi
                    st.markdown("---")
                    st.subheader("💼 Uygulanabilir İş Stratejileri")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("""
                        **🛒 E-Ticaret**
                        - "Sıklıkla birlikte alınan" bölümü
                        - Sepet sayfasında popup öneriler
                        - E-posta ile kişiselleştirilmiş teklifler
                        """)
                    
                    with col2:
                        st.markdown("""
                        **🏪 Fiziksel Mağaza**
                        - Yakın raf yerleşimi
                        - Kasa önü impulse placement
                        - Mağaza asistanı önerileri
                        """)
                    
                    with col3:
                        st.markdown("""
                        **📱 Mobil Uygulama**
                        - Push notification
                        - In-app banner'lar
                        - Gamification (puanlar)
                        """)
                    
                    # Sepet analizi özeti
                    st.markdown("---")
                    st.subheader("📊 Sepet Analizi Özeti")
                    
                    toplam_sepet_degeri = len(secili_urunler)
                    potansiyel_ekleme = len(sorted_oneriler)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Mevcut Sepet", f"{toplam_sepet_degeri} ürün")
                    with col2:
                        st.metric("Öneri Sayısı", f"{potansiyel_ekleme} ürün")
                    with col3:
                        potansiyel_buyume = (potansiyel_ekleme / toplam_sepet_degeri * 100) if toplam_sepet_degeri > 0 else 0
                        st.metric("Büyüme Potansiyeli", f"{potansiyel_buyume:.0f}%")
                    with col4:
                        avg_confidence = np.mean([bilgi['max_confidence'] for _, bilgi in sorted_oneriler])
                        st.metric("Ort. Confidence", f"{avg_confidence:.1%}")
                    
                else:
                    st.warning("❌ Bu ürünler için öneri bulunamadı. Parametreleri değiştirin.")
            
            elif not secili_urunler:
                st.info("👆 Öneri almak için lütfen en az bir ürün seçin")

else:
    st.error("❌ Veri yüklenemedi. Lütfen data/basket_analysis.csv dosyasının mevcut olduğundan emin olun.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>🎓 Gelişmiş Market Basket Analysis Platformu</strong></p>
    <p>Bu uygulama Market Basket Analysis konusunu derinlemesine anlamayı gösterir</p>
    <p>📊 Support • Confidence • Lift • Network Analysis • Segmentation • Negative Associations</p>
</div>
""", unsafe_allow_html=True)
