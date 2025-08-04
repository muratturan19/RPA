"""
Karmaşık RPA Sistemi - Streamlit Arayüzü
Çoklu Excel dosya yükleme ve işleme başlatma
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import subprocess
import sys
import os
import time
import threading
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(
    page_title="🤖 Karmaşık RPA Sistemi",
    page_icon="🤖",
    layout="wide"
)

# CSS ile özel stil
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9ff;
        margin: 1rem 0;
    }
    .file-info {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown("""
<div class="main-header">
    <h1>🤖 Karmaşık RPA Sistemi</h1>
    <p>Enterprise Seviye Otomatik Veri İşleme Platformu</p>
</div>
""", unsafe_allow_html=True)

# Session state başlatma
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "processing_status" not in st.session_state:
    st.session_state.processing_status = "idle"
if "results" not in st.session_state:
    st.session_state.results = []
if "current_file_index" not in st.session_state:
    st.session_state.current_file_index = 0

# Ana layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📁 Excel Dosya Yükleme")
    
    # Dosya yükleme alanı
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Excel dosyalarını buraya sürükleyip bırakın",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        help="Birden fazla Excel dosyası seçebilirsiniz. Her dosya sırayla işlenecektir."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Yüklenen dosyaları göster
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        
        st.markdown("### 📋 Yüklenen Dosyalar")
        for i, file in enumerate(uploaded_files, 1):
            # Dosya bilgilerini göster
            file_size = len(file.getvalue()) / 1024  # KB
            st.markdown(f"""
            <div class="file-info">
                <strong>📄 {i}. {file.name}</strong><br>
                📏 Boyut: {file_size:.1f} KB<br>
                📅 Yükleme: {datetime.now().strftime('%H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)
            
            # Dosya önizlemesi
            if st.button(f"👁️ Önizle", key=f"preview_{i}"):
                try:
                    df = pd.read_excel(file, nrows=5)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Önizleme hatası: {e}")

with col2:
    st.markdown("### 📊 İstatistikler")
    
    # İstatistik kartları
    total_files = len(st.session_state.uploaded_files)
    processed_files = len(st.session_state.results)
    
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="color: #667eea;">📁 {total_files}</h3>
        <p>Toplam Dosya</p>
    </div>
    <div class="stats-card">
        <h3 style="color: #52c41a;">✅ {processed_files}</h3>
        <p>İşlenmiş Dosya</p>
    </div>
    <div class="stats-card">
        <h3 style="color: #fa8c16;">⏳ {total_files - processed_files}</h3>
        <p>Bekleyen Dosya</p>
    </div>
    """, unsafe_allow_html=True)

# İşleme bölümü
st.markdown("---")
st.markdown("### 🚀 RPA İşleme Başlatma")

col3, col4 = st.columns([3, 1])

with col3:
    if not uploaded_files:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Dikkat:</strong> RPA işlemini başlatmak için önce Excel dosyalarını yükleyin.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>Hazır:</strong> {len(uploaded_files)} dosya işlenmeye hazır.
            RPA sistemi her dosyayı sırayla işleyecek ve sonuçları raporlayacaktır.
        </div>
        """, unsafe_allow_html=True)

with col4:
    # Ana başlat butonu
    start_processing = st.button(
        "🚀 RPA BAŞLAT",
        disabled=(not uploaded_files or st.session_state.processing_status == "running"),
        use_container_width=True,
        type="primary"
    )

# İşleme durumu gösterimi
if st.session_state.processing_status == "running":
    st.markdown("### ⚡ İşlem Durumu")
    
    # İlerleme çubuğu
    current_file = st.session_state.current_file_index
    total = len(st.session_state.uploaded_files)
    progress = current_file / total if total > 0 else 0
    
    st.progress(progress)
    st.write(f"📄 İşleniyor: {current_file + 1}/{total} - "
             f"{st.session_state.uploaded_files[current_file].name if current_file < total else 'Tamamlandı'}")
    
    # Durum güncellemesi (gerçek zamanlı)
    status_placeholder = st.empty()
    with status_placeholder.container():
        st.info("🤖 RPA sistemi çalışıyor... GUI açıldı ve otomasyon başladı.")

# RPA işlemini başlat
if start_processing:
    st.session_state.processing_status = "running"
    st.session_state.current_file_index = 0
    st.session_state.results = []
    
    # Dosyaları kaydet
    save_dir = Path("uploaded_files")
    save_dir.mkdir(exist_ok=True)
    
    saved_paths = []
    for file in uploaded_files:
        file_path = save_dir / file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        saved_paths.append(str(file_path))
    
    # RPA sistemini başlat (main.py'deki seçenek 3'ün işini yap)
    st.success("🎬 RPA Sistemi başlatılıyor...")
    st.info("📊 Karmaşık GUI açılacak ve otomasyon başlayacak...")
    
    # main.py'yi çağır ve dosya listesini geç
    try:
        # Ana RPA sistemini çağır
        subprocess.Popen([
            sys.executable, "main.py", 
            "--files"] + saved_paths,
            cwd=Path(__file__).parent
        )
        
        st.markdown("""
        <div class="success-box">
            🎉 <strong>Başarılı!</strong> RPA sistemi başlatıldı.<br>
            🖥️ Karmaşık GUI açılacak ve otomasyon başlayacak.<br>
            📊 İşlem tamamlandığında sonuçlar burada görünecek.
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"RPA başlatma hatası: {e}")
        st.session_state.processing_status = "idle"

# Sonuçlar bölümü
if st.session_state.results:
    st.markdown("---")
    st.markdown("### 📈 İşlem Sonuçları")
    
    # Sonuç tablosu
    results_df = pd.DataFrame(st.session_state.results)
    st.dataframe(results_df, use_container_width=True)
    
    # Özet istatistikler
    total_records = results_df['records'].sum() if 'records' in results_df.columns else 0
    successful_records = results_df['success'].sum() if 'success' in results_df.columns else 0
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Toplam Kayıt", total_records)
    with col6:
        st.metric("Başarılı İşlem", successful_records)
    with col7:
        success_rate = (successful_records / total_records * 100) if total_records > 0 else 0
        st.metric("Başarı Oranı", f"{success_rate:.1f}%")
    
    # Rapor indirme
    if st.button("📄 PDF Raporu İndir"):
        st.info("PDF raporu oluşturuluyor...")
        # PDF oluşturma kodu buraya gelecek

# Alt bilgi
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🤖 <strong>Karmaşık RPA Sistemi v3.0</strong> | 
    Enterprise Seviye Otomasyon Platformu |
    Gelişmiş GUI ve Çoklu Dosya İşleme Desteği
</div>
""", unsafe_allow_html=True)
