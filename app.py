import streamlit as st
import pandas as pd
import random
import warnings
warnings.filterwarnings('ignore')

# 1. Konfigurasi Halaman (Wide Layout & Clean Padding)
st.set_page_config(
    page_title="Smart Tourism Dashboard Desa Badransari", 
    page_icon="🌿", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Styling CSS untuk Mengatasi Cutoff Atas & Sidebar Scrollable
st.markdown("""
    <style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0F3255 !important;
        overflow-y: auto !important;
        max-height: 100vh !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-baseweb="popover"], [data-baseweb="menu"] {
        z-index: 999999 !important;
    }
    
    .sidebar-title {
        text-align: center; 
        padding: 5px 0 12px 0; 
        border-bottom: 1px solid rgba(255,255,255,0.2); 
        margin-bottom: 10px;
    }
    .sidebar-title h3 {
        color: #FFD700 !important; 
        font-size: 13px; 
        font-weight: 800; 
        margin: 0; 
        line-height: 1.4; 
        text-transform: uppercase;
    }
    .sidebar-title p { 
        color: #E0E0E0 !important; 
        font-size: 9px; 
        margin: 3px 0 0 0; 
    }
    iframe { border: none; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Filter Data (Sesuai Permintaan: Tahun, Bulan, Jenis Wisatawan, Jenis Wisata)
st.sidebar.markdown("""
    <div class="sidebar-title">
        <h3>Hibah BIMA Semenanjung Badran ITERA</h3>
        <p>Program Pengabdian Kepada Masyarakat</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown('### <i class="fa-solid fa-filter"></i> FILTER DATA', unsafe_allow_html=True)
filter_tahun = st.sidebar.selectbox("📅 Tahun", ["2024", "2025", "2026"])
filter_bulan = st.sidebar.selectbox("🕒 Bulan", ["Semua", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
filter_jenis_wisatawan = st.sidebar.selectbox("👥 Jenis Wisatawan", ["Semua", "Lampung", "Luar Lampung"])
filter_jenis = st.sidebar.selectbox("⛰️ Jenis Wisata", ["Semua", "Wisata Alam", "Wisata Edukasi", "Kuliner & Outbound"])

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); text-align: center;">
        <p style="font-size: 9px; font-weight: 700; color: #FFD700; margin:0; text-transform: uppercase;">Destinasi Unggulan</p>
        <p style="font-size: 11px; font-weight: 800; color: white; margin: 3px 0 0 0;">Semenanjung Badran</p>
        <p style="font-size: 8px; color: #CCC; margin: 2px 0 0 0;">Desa Badransari</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# LOGIKA DINAMIS BERDASARKAN FILTER
# ==========================================
multiplier = 1.0
if filter_tahun == "2025": 
    multiplier = 1.15
elif filter_tahun == "2026": 
    multiplier = 1.35

if filter_bulan != "Semua": 
    multiplier = multiplier * 0.12

total_pengunjung = int(4280 * multiplier)
pendapatan_total = round(152.7 * multiplier, 1)
pengunjung_hari_ini = int(156 * multiplier * random.uniform(0.9, 1.1))
tiket_val = round(68.2 * multiplier, 1)

# 4. Konten HTML/CSS Dashboard (Chart Dipercantik, Interaktif, & Layout Padat Tanpa Ruang Kosong)
dashboard_html = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ font-family: 'Inter', sans-serif; box-sizing: border-box; }}
        body {{ background-color: #F0F4F8; margin: 0; padding: 0; }}
        
        .top-banner {{
            background: linear-gradient(rgba(15, 50, 85, 0.88), rgba(15, 50, 85, 0.78)), 
                        url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2000&auto=format&fit=crop') center/cover;
            padding: 12px 20px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .logo-area {{ display: flex; align-items: center; gap: 12px; }}
        .logo-badge {{ background: white; color: #0F3255; font-weight: 800; font-size: 11px; padding: 6px 10px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .title-area h1 {{ font-size: 16px; font-weight: 800; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; color: #FFD700; }}
        .title-area p {{ font-size: 10px; font-weight: 600; margin: 2px 0 0 0; color: #E0E0E0; }}
        
        .stats-group {{ display: flex; gap: 8px; }}
        .stat-item {{ background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.3); padding: 5px 10px; border-radius: 8px; text-align: center; }}
        .stat-item span {{ display: block; font-size: 7px; font-weight: 700; color: #FFD700; text-transform: uppercase; }}
        .stat-item strong {{ font-size: 12px; font-weight: 800; color: white; }}

        .three-column-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 10px; }}
        .column-box {{ display: flex; flex-direction: column; gap: 10px; }}
        
        .card-box {{ background: white; border-radius: 8px; padding: 10px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); transition: transform 0.2s ease; }}
        .card-box:hover {{ box-shadow: 0 4px 10px rgba(0,0,0,0.06); }}
        
        .col-header {{ padding: 8px 10px; border-radius: 6px; font-weight: 800; color: white; font-size: 10px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .bg-green {{ background: #2E7D32; }}
        .bg-blue {{ background: #1565C0; }}
        .bg-purple {{ background: #4A148C; }}

        .metric-subgrid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}
        .m-card {{ background: #FAFAFA; border-radius: 6px; padding: 5px 3px; border: 1px solid #EAEAEA; text-align: center; height: 75px; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
        .m-icon {{ font-size: 9px; margin-bottom: 2px; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
        .m-title {{ font-size: 6.5px; font-weight: 800; color: #555; text-transform: uppercase; line-height: 1.1; width: 100%; }}
        .m-value {{ font-size: 11px; font-weight: 800; color: #111; margin: 1px 0; }}
        .m-sub {{ font-size: 6.5px; font-weight: 700; color: #777; }}

        .section-title {{ font-size: 9.5px; font-weight: 800; color: #333; margin-bottom: 8px; display: flex; align-items: center; gap: 5px; text-transform: uppercase; border-bottom: 2px solid #F0F0F0; padding-bottom: 4px; }}

        .proportion-container {{ margin-top: 5px; }}
        .proportion-bar-wrapper {{ display: flex; height: 16px; border-radius: 8px; overflow: hidden; background: #eee; margin: 6px 0; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); }}
        .prop-segment-1 {{ background: #2E7D32; width: 75%; display: flex; align-items: center; justify-content: center; color: white; font-size: 8px; font-weight: 800; }}
        .prop-segment-2 {{ background: #1565C0; width: 25%; display: flex; align-items: center; justify-content: center; color: white; font-size: 8px; font-weight: 800; }}
        .prop-legend {{ display: flex; justify-content: space-between; font-size: 8px; font-weight: 700; color: #555; }}

        .flow-container {{ display: flex; flex-direction: column; gap: 4px; align-items: center; }}
        .flow-node {{ background: #E8F5E9; border: 1px solid #2E7D32; color: #1E3A1E; padding: 5px 10px; border-radius: 5px; font-size: 8.5px; font-weight: 800; width: 100%; text-align: center; }}
        .flow-node.blue {{ background: #E3F2FD; border-color: #1565C0; color: #0D47A1; }}
        .flow-node.orange {{ background: #FFF8E1; border-color: #F57F17; color: #E65100; }}
        .flow-node.purple {{ background: #EDE7F6; border-color: #4A148C; color: #311B92; }}
        .flow-arrow {{ font-size: 9px; color: #666; margin: -2px 0; }}

        .community-box {{ display: flex; align-items: center; gap: 12px; background: #E8F5E9; padding: 8px 10px; border-radius: 8px; border: 1px solid #C8E6C9; }}
        .community-icons-group {{ display: flex; gap: 3px; color: #2E7D32; font-size: 14px; background: white; padding: 6px 8px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .community-info {{ flex-grow: 1; }}
        .community-info h4 {{ margin: 0; font-size: 11px; color: #1E3A1E; font-weight: 800; }}
        .community-info p {{ margin: 2px 0 4px 0; font-size: 8px; color: #388E3C; font-weight: 600; }}
        .progress-track {{ background: #C8E6C9; height: 6px; border-radius: 3px; width: 100%; overflow: hidden; }}
        .progress-fill {{ background: #2E7D32; height: 100%; width: 78%; border-radius: 3px; }}

        .event-list {{ display: flex; flex-direction: column; gap: 4px; }}
        .event-item {{ display: flex; align-items: center; background: #FAFAFA; padding: 4px 6px; border-radius: 5px; border-left: 3px solid #1565C0; font-size: 8.5px; gap: 6px; }}
        .event-date {{ font-weight: 800; color: #1565C0; min-width: 45px; }}
        .event-name {{ font-weight: 600; color: #333; }}

        /* Kartu Analisis Tambahan untuk Menghilangkan Ruang Kosong Bawah */
        .insights-card {{ background: linear-gradient(135deg, #ffffff, #f7f9fb); border-radius: 8px; padding: 12px; border: 1px solid #D0DCE5; margin-bottom: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }}
        .insights-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 8px; }}
        .insight-item {{ background: #FFFFFF; padding: 8px; border-radius: 6px; border-left: 3px solid #2E7D32; border-top: 1px solid #EAEAEA; border-right: 1px solid #EAEAEA; border-bottom: 1px solid #EAEAEA; }}
        .insight-item h5 {{ margin: 0 0 3px 0; font-size: 9px; color: #0F3255; font-weight: 800; text-transform: uppercase; }}
        .insight-item p {{ margin: 0; font-size: 8px; color: #555; line-height: 1.3; }}

        .footer-banner {{ background: linear-gradient(135deg, #0F3255, #1565C0); color: white; padding: 10px 15px; border-radius: 8px; text-align: center; margin-top: 10px; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>

    <!-- Banner Atas -->
    <div class="top-banner">
        <div class="logo-area">
            <div class="logo-badge">ITERA</div>
            <div class="logo-badge" style="background: #2E7D32; color: white;">KKN ITERA</div>
            <div class="title-area">
                <h1>Smart Tourism Dashboard — Desa Badransari</h1>
                <p>Kecamatan Punggur, Kabupaten Lampung Tengah • Program Hibah BIMA ITERA</p>
            </div>
        </div>
        <div class="stats-group">
            <div class="stat-item">
                <span>👥 Total Pengunjung</span>
                <strong>{total_pengunjung:,} Orang</strong>
            </div>
            <div class="stat-item">
                <span>💰 Pendapatan</span>
                <strong>Rp {pendapatan_total} Juta</strong>
            </div>
            <div class="stat-item">
                <span>⭐ Kepuasan</span>
                <strong>88% Baik</strong>
            </div>
        </div>
    </div>

    <!-- STRUKTUR UTAMA: 3 KOLOM -->
    <div class="three-column-grid">
        
        <!-- KOLOM 1: LAYANAN PARIWISATA -->
        <div class="column-box">
            <div class="card-box">
                <div class="col-header bg-green"><i class="fa-solid fa-umbrella-beach"></i> 1. Layanan Pariwisata</div>
                <div class="metric-subgrid">
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-users"></i></div><div class="m-title">Pengunjung</div><div class="m-value">{total_pengunjung}</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-person-walking"></i></div><div class="m-title">Hari Ini</div><div class="m-value">{pengunjung_hari_ini}</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-ticket"></i></div><div class="m-title">Tiket</div><div class="m-value">{tiket_val}</div><div class="m-sub">Juta Rp</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-star"></i></div><div class="m-title">Kepuasan</div><div class="m-value">88%</div><div class="m-sub">Sangat Baik</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-store"></i></div><div class="m-title">UMKM</div><div class="m-value">42</div><div class="m-sub">Unit</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-house"></i></div><div class="m-title">Homestay</div><div class="m-value">15</div><div class="m-sub">Unit</div></div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #2E7D32;"></i> Tren Kunjungan Wisatawan</div>
                <canvas id="trendChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-umbrella" style="color: #2E7D32;"></i> Fasilitas Wisata (Jumlah Unit)</div>
                <canvas id="facilityChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-users-rectangle" style="color: #2E7D32;"></i> Jenis Wisatawan (Proporsi)</div>
                <div class="proportion-container">
                    <div class="proportion-bar-wrapper">
                        <div class="prop-segment-1" title="Lampung: 75%">75% Lampung</div>
                        <div class="prop-segment-2" title="Luar Lampung: 25%">25% Luar Lampung</div>
                    </div>
                    <div class="prop-legend">
                        <span style="color: #2E7D32;">■ Domestik Lampung</span>
                        <span style="color: #1565C0;">■ Luar Lampung</span>
                    </div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #2E7D32;"></i> Lokasi Semenanjung Badran</div>
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.6!2d105.2!3d-5.1!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNcKwMDYnMDAnUzEwNcKwMTInMDAuMCJF!5e0!3m2!1sid!2sid!4v1650000000000!5m2!1sid!2sid" 
                        width="100%" height="130" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-triangle-exclamation" style="color: #2E7D32;"></i> Keluhan Wisatawan</div>
                <canvas id="complaintChart" height="120"></canvas>
            </div>
        </div>

        <!-- KOLOM 2: MANAJEMEN PARIWISATA -->
        <div class="column-box">
            <div class="card-box">
                <div class="col-header bg-blue"><i class="fa-solid fa-gear"></i> 2. Manajemen Pariwisata</div>
                <div class="metric-subgrid">
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-users-gear"></i></div><div class="m-title">Pokdarwis</div><div class="m-value">3</div><div class="m-sub">Kelompok</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-user-tie"></i></div><div class="m-title">Pengelola</div><div class="m-value">27</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-shop"></i></div><div class="m-title">UMKM Aktif</div><div class="m-value">42</div><div class="m-sub">Unit</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-calendar"></i></div><div class="m-title">Event</div><div class="m-value">8</div><div class="m-sub">Kegiatan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-handshake"></i></div><div class="m-title">Mitra</div><div class="m-value">12</div><div class="m-sub">Instansi</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-hands-holding-child"></i></div><div class="m-title">Relawan</div><div class="m-value">36</div><div class="m-sub">Orang</div></div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-sitemap" style="color: #1565C0;"></i> Struktur Pengelolaan</div>
                <div class="flow-container">
                    <div class="flow-node">🏛️ Pemerintah Desa Badransari</div>
                    <div class="flow-arrow">↓</div>
                    <div class="flow-node blue">👥 Pokdarwis (Kelompok Sadar Wisata)</div>
                    <div class="flow-arrow">↓</div>
                    <div class="flow-node orange">🏪 Unit UMKM & Homestay</div>
                    <div class="flow-arrow">↓</div>
                    <div class="flow-node purple">🤝 Masyarakat & Relawan</div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-calendar-days" style="color: #1565C0;"></i> Jadwal Event Tahun Ini</div>
                <div class="event-list">
                    <div class="event-item"><span class="event-date">14 Jan</span><span class="event-name">Festival Desa Badransari</span></div>
                    <div class="event-item"><span class="event-date">18 Feb</span><span class="event-name">Pasar UMKM Kreatif</span></div>
                    <div class="event-item"><span class="event-date">24 Mar</span><span class="event-name">Lomba Perahu Tradisional</span></div>
                    <div class="event-item"><span class="event-date">12 Mei</span><span class="event-name">Camping & Outbound</span></div>
                    <div class="event-item"><span class="event-date">20 Jul</span><span class="event-name">Festival Kuliner Desa</span></div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-money-bill-trend-up" style="color: #1565C0;"></i> Pendapatan Pariwisata (Juta Rp)</div>
                <canvas id="revenueChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-wallet" style="color: #1565C0;"></i> Pengeluaran Pariwisata</div>
                <canvas id="expenseChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-people-group" style="color: #1565C0;"></i> Tingkat Keterlibatan Masyarakat</div>
                <div class="community-box">
                    <div class="community-icons-group">
                        <i class="fa-solid fa-user"></i>
                        <i class="fa-solid fa-user" style="opacity: 0.8;"></i>
                        <i class="fa-solid fa-user" style="opacity: 0.6;"></i>
                    </div>
                    <div class="community-info">
                        <h4>78% Partisipasi Aktif</h4>
                        <p>Masyarakat terlibat dalam homestay, event, kuliner & sadar wisata.</p>
                        <div class="progress-track">
                            <div class="progress-fill"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- KOLOM 3: PEMASARAN PARIWISATA -->
        <div class="column-box">
            <div class="card-box">
                <div class="col-header bg-purple"><i class="fa-solid fa-bullhorn"></i> 3. Pemasaran Pariwisata</div>
                <div class="metric-subgrid">
                    <div class="m-card"><div class="m-icon" style="color: #E1306C; background: #FCE4EC;"><i class="fa-brands fa-instagram"></i></div><div class="m-title">IG Followers</div><div class="m-value">3.842</div><div class="m-sub">Akun</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #000; background: #F5F5F5;"><i class="fa-brands fa-tiktok"></i></div><div class="m-title">TikTok</div><div class="m-value">2.156</div><div class="m-sub">Akun</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-brands fa-facebook"></i></div><div class="m-title">FB Reach</div><div class="m-value">8.745</div><div class="m-sub">Jangkauan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #4A148C; background: #EDE7F6;"><i class="fa-solid fa-globe"></i></div><div class="m-title">Website</div><div class="m-value">5.231</div><div class="m-sub">Kunjungan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #4A148C; background: #EDE7F6;"><i class="fa-solid fa-comments"></i></div><div class="m-title">Review</div><div class="m-value">157</div><div class="m-sub">Ulasan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #F57F17; background: #FFF8E1;"><i class="fa-solid fa-star"></i></div><div class="m-title">Rating</div><div class="m-value">4,6</div><div class="m-sub">Sangat Baik</div></div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #4A148C;"></i> Asal Wisatawan</div>
                <canvas id="originChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-share-nodes" style="color: #4A148C;"></i> Media Promosi (Kontribusi)</div>
                <canvas id="promoChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #4A148C;"></i> Engagement Media Sosial</div>
                <canvas id="engagementChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-circle-info" style="color: #4A148C;"></i> Sumber Informasi Wisatawan</div>
                <canvas id="sourceChart" height="120"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-ranking-star" style="color: #4A148C;"></i> Konten Terpopuler</div>
                <div style="font-size: 8.5px; font-weight: 700; color: #444; display: flex; flex-direction: column; gap: 4px;">
                    <div style="display: flex; justify-content: space-between; background: #F3E5F5; padding: 4px 6px; border-radius: 4px;"><span>1. Spot Foto & Panorama</span><span style="color: #4A148C;">35%</span></div>
                    <div style="display: flex; justify-content: space-between; background: #FAFAFA; padding: 4px 6px; border-radius: 4px;"><span>2. Sunset & Pemandangan</span><span style="color: #4A148C;">25%</span></div>
                    <div style="display: flex; justify-content: space-between; background: #FAFAFA; padding: 4px 6px; border-radius: 4px;"><span>3. Festival & Event Desa</span><span style="color: #4A148C;">20%</span></div>
                </div>
            </div>
        </div>

    </div>

    <!-- KARTU ANALISIS TAMBAHAN (Menghilangkan Ruang Kosong Bawah & Menambah Nilai Informatif) -->
    <div class="insights-card">
        <div class="section-title" style="color: #0F3255; border-bottom-color: #D0DCE5;"><i class="fa-solid fa-lightbulb" style="color: #FFD700; font-size: 11px;"></i> Analisis & Rekomendasi Strategis Smart Tourism Desa Badransari</div>
        <div class="insights-grid">
            <div class="insight-item">
                <h5>🚀 Peningkatan Kunjungan</h5>
                <p>Tren kunjungan melonjak pada pertengahan tahun. Disarankan menambah kapasitas homestay dan event tematik di bulan-bulan tersebut.</p>
            </div>
            <div class="insight-item">
                <h5>📈 Digital Marketing</h5>
                <p>Instagram & TikTok memberikan kontribusi kunjungan tertinggi (60%). Optimalisasi Reels & konten video pendek perlu terus digencarkan.</p>
            </div>
            <div class="insight-item">
                <h5>⭐ Optimalisasi Layanan</h5>
                <p>Keluhan utama terkait kebersihan & fasilitas toilet dapat diatasi dengan memperketat piket kebersihan Pokdarwis dan penambahan signage.</p>
            </div>
        </div>
    </div>

    <!-- Banner Footer Slogan -->
    <div class="footer-banner">
        “Bersama Membangun Pariwisata Desa Badransari yang Berkelanjutan, Berdaya Saing, dan Berbasis Masyarakat”
    </div>

    <script>
        // Konfigurasi Umum Chart.js untuk Tampilan Lebih Estetik & Interaktif
        Chart.defaults.font.family = 'Inter';
        Chart.defaults.font.size = 8;
        Chart.defaults.color = '#555';

        const standardTooltip = {{
            backgroundColor: 'rgba(15, 50, 85, 0.9)',
            titleFont: {{ size: 9, weight: 'bold' }},
            bodyFont: {{ size: 8 }},
            padding: 8,
            cornerRadius: 6,
            displayColors: false
        }};

        // 1. Trend Kunjungan Chart (Gradient Fill)
        const ctxTrend = document.getElementById('trendChart').getContext('2d');
        const gradientTrend = ctxTrend.createLinearGradient(0, 0, 0, 120);
        gradientTrend.addColorStop(0, 'rgba(46, 125, 50, 0.35)');
        gradientTrend.addColorStop(1, 'rgba(46, 125, 50, 0.0)');

        new Chart(ctxTrend, {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
                datasets: [{{
                    data: [240, 280, 310, 520, 610, 720, 480, 510, 420, 400, 440, 680],
                    borderColor: '#2E7D32',
                    backgroundColor: gradientTrend,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 2,
                    pointHoverRadius: 6
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: standardTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // 2. Fasilitas Chart
        new Chart(document.getElementById('facilityChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Parkir', 'Toilet', 'Mushola', 'Gazebo', 'Spot Foto', 'Warung'],
                datasets: [{{
                    data: [2, 4, 2, 6, 8, 12],
                    backgroundColor: '#2E7D32',
                    borderRadius: 4
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: standardTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // 3. Keluhan Wisatawan Chart
        new Chart(document.getElementById('complaintChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Kebersihan', 'Jalan', 'Toilet', 'Parkir', 'Informasi'],
                datasets: [{{
                    data: [28, 22, 20, 15, 9],
                    backgroundColor: '#388E3C',
                    borderRadius: 4
                }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: standardTooltip }}, scales: {{ x: {{ beginAtZero: true, max: 35, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, y: {{ grid: {{ display: false }} }} }} }}
        }});

        // 4. Pendapatan Chart
        new Chart(document.getElementById('revenueChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Tiket', 'Parkir', 'Sewa', 'Camping', 'UMKM'],
                datasets: [{{
                    data: [68, 22, 18, 15, 28],
                    backgroundColor: '#1565C0',
                    borderRadius: 4
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: standardTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // 5. Pengeluaran Chart
        new Chart(document.getElementById('expenseChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Kebersihan', 'Perawatan', 'Promosi', 'SDM', 'Infrastruktur'],
                datasets: [{{
                    data: [30, 25, 15, 15, 15],
                    backgroundColor: ['#1565C0', '#42A5F5', '#90CAF9', '#BBDEFB', '#E3F2FD'],
                    borderWidth: 1
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 6, font: {{ size: 7 }} }} }}, tooltip: standardTooltip }} }}
        }});

        // 6. Asal Wisatawan Chart
        new Chart(document.getElementById('originChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Lampung', 'Sumsel', 'DKI', 'Banten', 'Jabar'],
                datasets: [{{
                    data: [55, 17, 10, 7, 6],
                    backgroundColor: '#4A148C',
                    borderRadius: 4
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: standardTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // 7. Media Promosi Chart
        new Chart(document.getElementById('promoChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Instagram', 'TikTok', 'Facebook', 'Website', 'YouTube'],
                datasets: [{{
                    data: [35, 25, 15, 15, 10],
                    backgroundColor: '#7B1FA2',
                    borderRadius: 4
                }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: standardTooltip }}, scales: {{ x: {{ beginAtZero: true, max: 40, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, y: {{ grid: {{ display: false }} }} }} }}
        }});

        // 8. Engagement Media Sosial Chart
        new Chart(document.getElementById('engagementChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [
                    {{ label: 'Like', data: [1200, 1500, 1800, 2200, 2600, 3100], borderColor: '#4A148C', borderWidth: 2, tension: 0.35, pointRadius: 2 }},
                    {{ label: 'Comment', data: [400, 600, 700, 900, 1100, 1400], borderColor: '#AB47BC', borderWidth: 2, tension: 0.35, pointRadius: 2 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: standardTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // 9. Sumber Informasi Chart
        new Chart(document.getElementById('sourceChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Media Sosial', 'Teman/Keluarga', 'Google', 'Website', 'Banner'],
                datasets: [{{
                    data: [45, 25, 15, 10, 5],
                    backgroundColor: ['#4A148C', '#7B1FA2', '#AB47BC', '#CE93D8', '#F3E5F5'],
                    borderWidth: 1
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 6, font: {{ size: 7 }} }} }}, tooltip: standardTooltip }} }}
        }});
    </script>
</body>
</html>
"""

# Render ke dalam Streamlit Component (Tinggi disesuaikan proporsional)
import streamlit.components.v1 as components
components.html(dashboard_html, height=1880, scrolling=True)