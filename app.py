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

# 2. Styling CSS untuk Konsistensi Tampilan & Anti Ruang Kosong
st.markdown("""
    <style>
    .block-container {
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
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
        padding: 4px 0 8px 0; 
        border-bottom: 1px solid rgba(255,255,255,0.2); 
        margin-bottom: 6px;
    }
    .sidebar-title h3 {
        color: #FFD700 !important; 
        font-size: 12px; 
        font-weight: 800; 
        margin: 0; 
        line-height: 1.3; 
        text-transform: uppercase;
    }
    .sidebar-title p { 
        color: #E0E0E0 !important; 
        font-size: 8.5px; 
        margin: 2px 0 0 0; 
    }
    iframe { border: none; border-radius: 5px; width: 100%; }

    @keyframes pulseGlow {
        0% { box-shadow: 0 2px 5px rgba(0,0,0,0.15); filter: brightness(1); }
        50% { box-shadow: 0 4px 12px rgba(46, 125, 50, 0.4); filter: brightness(1.03); }
        100% { box-shadow: 0 2px 5px rgba(0,0,0,0.15); filter: brightness(1); }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Filter Data
st.sidebar.markdown("""
    <div class="sidebar-title">
        <h3>Hibah BIMA Semenanjung Badran ITERA</h3>
        <p>Program Pengabdian Kepada Masyarakat</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown('### <i class="fa-solid fa-filter"></i> FILTER DATA', unsafe_allow_html=True)
filter_tahun = st.sidebar.selectbox("📅 Tahun", ["Semua", "2025", "2024", "2026"])
filter_bulan = st.sidebar.selectbox("🕒 Bulan", ["Semua", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
filter_jenis_wisatawan = st.sidebar.selectbox("👥 Jenis Wisatawan", ["Semua", "Lampung", "Luar Lampung"])
filter_jenis = st.sidebar.selectbox("⛰️ Jenis Wisata", ["Semua", "Wisata Alam", "Wisata Edukasi", "Kuliner & Outbound"])

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 6px; border-radius: 5px; border: 1px solid rgba(255,255,255,0.2); text-align: center;">
        <p style="font-size: 8.5px; font-weight: 700; color: #FFD700; margin:0; text-transform: uppercase;">Destinasi Unggulan</p>
        <p style="font-size: 10.5px; font-weight: 800; color: white; margin: 2px 0 0 0;">Semenanjung Badran</p>
        <p style="font-size: 7.5px; color: #CCC; margin: 1px 0 0 0;">Desa Badransari</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# PEMISAHAN LOGIKA FILTER & SKALA DATA
# ==========================================
year_factor = 1.0
if filter_tahun == "2024":
    year_factor = 0.88
elif filter_tahun == "2026":
    year_factor = 1.25
elif filter_tahun == "Semua":
    year_factor = 2.45

total_pengunjung = int(4922 * year_factor)
pendapatan_total = round(152.7 * year_factor, 1)
pengunjung_hari_ini = int(176 * (1.1 if filter_tahun != "Semua" else 1.5))
tiket_val = round(78.4 * year_factor, 1)

pokdarwis_val = 3 if filter_tahun != "Semua" else 5
pengelola_val = int(27 * year_factor)
umkm_aktif_val = int(42 * year_factor)
event_val = 8 if filter_tahun != "Semua" else 14
mitra_val = int(12 * year_factor)
relawan_val = int(36 * year_factor)

ig_followers_val = f"{int(3842 * year_factor):,}".replace(",", ".")
tiktok_val = f"{int(2156 * year_factor):,}".replace(",", ".")
fb_reach_val = f"{int(8745 * year_factor):,}".replace(",", ".")
website_val = f"{int(5231 * year_factor):,}".replace(",", ".")
review_val = int(157 * year_factor)

chart_factor = year_factor
if filter_bulan != "Semua": 
    chart_factor *= 0.12

lampung_prop = 75
luar_prop = 25
if filter_jenis_wisatawan == "Lampung":
    chart_factor *= 0.78
    lampung_prop = 100
    luar_prop = 0
elif filter_jenis_wisatawan == "Luar Lampung":
    chart_factor *= 0.35
    lampung_prop = 0
    luar_prop = 100

if filter_jenis == "Wisata Alam":
    chart_factor *= 0.55
elif filter_jenis == "Wisata Edukasi":
    chart_factor *= 0.30
elif filter_jenis == "Kuliner & Outbound":
    chart_factor *= 0.25

chart_factor = max(chart_factor, 0.15)
keterlibatan_masyarakat_val = int(78 * min(chart_factor, 1.2))

# 4. Konten HTML/CSS Dashboard (Compact & Balanced Layout)
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
        body {{ background-color: #F0F4F8; margin: 0; padding: 0; overflow-x: hidden; }}
        
        .top-banner {{
            background: linear-gradient(rgba(15, 50, 85, 0.92), rgba(15, 50, 85, 0.82)), 
                        url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2000&auto=format&fit=crop') center/cover;
            padding: 8px 14px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .logo-area {{ display: flex; align-items: center; gap: 8px; }}
        .logo-badge {{ background: white; color: #0F3255; font-weight: 800; font-size: 9.5px; padding: 3px 6px; border-radius: 3px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }}
        .title-area h1 {{ font-size: 13px; font-weight: 800; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; color: #FFD700; }}
        .title-area p {{ font-size: 8.5px; font-weight: 600; margin: 1px 0 0 0; color: #E0E0E0; }}
        
        .stats-group {{ display: flex; gap: 6px; }}
        .stat-item {{ background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.3); padding: 3px 6px; border-radius: 4px; text-align: center; }}
        .stat-item span {{ display: block; font-size: 6.5px; font-weight: 700; color: #FFD700; text-transform: uppercase; }}
        .stat-item strong {{ font-size: 10.5px; font-weight: 800; color: white; }}

        .three-column-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin-bottom: 4px; width: 100%; }}
        .column-box {{ display: flex; flex-direction: column; gap: 5px; min-width: 0; }}
        
        .card-box {{ background: white; border-radius: 5px; padding: 6px 8px; border: 1px solid #E0E0E0; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }}
        
        .col-header {{ padding: 5px 8px; border-radius: 4px; font-weight: 800; color: white; font-size: 9.5px; margin-bottom: 5px; display: flex; align-items: center; gap: 5px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .bg-green {{ background: #2E7D32; }}
        .bg-blue {{ background: #1565C0; }}
        .bg-purple {{ background: #4A148C; }}

        .metric-subgrid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; }}
        .m-card {{ background: #FAFAFA; border-radius: 4px; padding: 4px 2px; border: 1px solid #EAEAEA; text-align: center; height: 60px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; }}
        .m-icon {{ font-size: 9px; width: 14px; height: 14px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
        .m-title {{ font-size: 6.5px; font-weight: 800; color: #555; text-transform: uppercase; line-height: 1.1; width: 100%; }}
        .m-value {{ font-size: 10px; font-weight: 800; color: #111; margin: 1px 0; }}
        .m-sub {{ font-size: 6px; font-weight: 700; color: #777; }}

        .section-title {{ font-size: 8.5px; font-weight: 800; color: #333; margin-bottom: 5px; display: flex; align-items: center; gap: 4px; text-transform: uppercase; border-bottom: 2px solid #F0F0F0; padding-bottom: 2px; }}

        .proportion-container {{ margin-top: 2px; }}
        .proportion-bar-wrapper {{ display: flex; height: 16px; border-radius: 4px; overflow: hidden; background: #eee; margin: 3px 0; box-shadow: inset 0 1px 2px rgba(0,0,0,0.1); }}
        .prop-segment-1 {{ background: #2E7D32; width: {lampung_prop}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 7.5px; font-weight: 800; white-space: nowrap; overflow: hidden; }}
        .prop-segment-2 {{ background: #1565C0; width: {luar_prop}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 7.5px; font-weight: 800; white-space: nowrap; overflow: hidden; }}
        .prop-legend {{ display: flex; justify-content: space-between; font-size: 7.5px; font-weight: 700; color: #555; margin-top: 2px; }}

        .flow-container {{ display: flex; flex-direction: column; gap: 3px; align-items: center; padding: 2px 0; }}
        .flow-node {{ background: #E8F5E9; border: 1.2px solid #2E7D32; color: #1E3A1E; padding: 5px 8px; border-radius: 5px; font-size: 8px; font-weight: 800; width: 100%; text-align: center; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }}
        .flow-node.blue {{ background: #E3F2FD; border-color: #1565C0; color: #0D47A1; }}
        .flow-node.orange {{ background: #FFF8E1; border-color: #F57F17; color: #E65100; }}
        .flow-node.purple {{ background: #EDE7F6; border-color: #4A148C; color: #311B92; }}
        .flow-arrow {{ font-size: 8px; color: #1565C0; font-weight: bold; margin: -2px 0; }}

        .community-box {{ display: flex; align-items: center; gap: 8px; background: #E8F5E9; padding: 6px 8px; border-radius: 5px; border: 1px solid #C8E6C9; }}
        .community-icons-group {{ display: flex; gap: 2px; color: #2E7D32; font-size: 12px; background: white; padding: 5px 6px; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .community-info {{ flex-grow: 1; }}
        .community-info h4 {{ margin: 0 0 2px 0; font-size: 9px; color: #1E3A1E; font-weight: 800; }}
        .community-info p {{ margin: 0 0 3px 0; font-size: 7px; color: #388E3C; font-weight: 600; line-height: 1.1; }}
        .progress-track {{ background: #C8E6C9; height: 5px; border-radius: 3px; width: 100%; overflow: hidden; }}
        .progress-fill {{ background: #2E7D32; height: 100%; width: {keterlibatan_masyarakat_val}%; border-radius: 3px; }}

        .slogan-card {{ background: linear-gradient(135deg, #0F3255, #1E3A5F, #2E7D32); color: white; padding: 8px 10px; border-radius: 5px; display: flex; flex-direction: column; gap: 5px; border: 1px solid rgba(255,255,255,0.25); animation: pulseGlow 4s infinite ease-in-out; }}
        .slogan-item {{ display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.12); padding: 5px 7px; border-radius: 4px; backdrop-filter: blur(4px); }}
        .slogan-item i {{ color: #FFD700; font-size: 11px; }}
        .slogan-text {{ font-size: 8.5px; font-weight: 700; letter-spacing: 0.3px; }}

        .fade-img-container {{ position: relative; border-radius: 5px; overflow: hidden; border: 1px solid #E0E0E0; max-height: 95px; margin-top: 3px; }}
        .fade-img-container img {{ width: 100%; height: 95px; object-fit: cover; display: block; filter: brightness(0.92); }}
        .fade-overlay {{ position: absolute; bottom: 0; left: 0; right: 0; height: 45px; background: linear-gradient(to top, rgba(15,50,85,0.95), transparent); display: flex; align-items: flex-end; padding: 5px 8px; }}
        .fade-text {{ color: white; font-size: 8px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.4px; }}
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

    <!-- STRUKTUR UTAMA: 3 KOLOM SEIMBANG TANPA RUANG KOSONG -->
    <div class="three-column-grid">
        
        <!-- KOLOM 1: LAYANAN PARIWISATA -->
        <div class="column-box">
            <div class="card-box">
                <div class="col-header bg-green"><i class="fa-solid fa-umbrella-beach"></i> 1. Layanan Pariwisata</div>
                <div class="metric-subgrid">
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-users"></i></div><div class="m-title">Pengunjung</div><div class="m-value">{total_pengunjung:,}</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-person-walking"></i></div><div class="m-title">Hari Ini</div><div class="m-value">{pengunjung_hari_ini}</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-ticket"></i></div><div class="m-title">Tiket</div><div class="m-value">{tiket_val}</div><div class="m-sub">Juta Rp</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-star"></i></div><div class="m-title">Kepuasan</div><div class="m-value">88%</div><div class="m-sub">Sangat Baik</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-store"></i></div><div class="m-title">UMKM</div><div class="m-value">{umkm_aktif_val}</div><div class="m-sub">Unit</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-house"></i></div><div class="m-title">Homestay</div><div class="m-value">{int(15 * year_factor)}</div><div class="m-sub">Unit</div></div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #2E7D32;"></i> Tren Kunjungan Wisatawan</div>
                <canvas id="trendChart" height="95"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-umbrella" style="color: #2E7D32;"></i> Fasilitas Wisata (Jumlah Unit)</div>
                <canvas id="facilityChart" height="95"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-users-rectangle" style="color: #2E7D32;"></i> Jenis Wisatawan (Proporsi)</div>
                <div class="proportion-container">
                    <div class="proportion-bar-wrapper">
                        <div class="prop-segment-1" style="width: {lampung_prop}%;">{"⚡ " + str(lampung_prop) + "% Lampung" if lampung_prop > 0 else ""}</div>
                        <div class="prop-segment-2" style="width: {luar_prop}%;">{"⚡ " + str(luar_prop) + "% Luar" if luar_prop > 0 else ""}</div>
                    </div>
                    <div class="prop-legend">
                        <span style="color: #2E7D32;">■ Domestik Lampung ({lampung_prop}%)</span>
                        <span style="color: #1565C0;">■ Luar Lampung ({luar_prop}%)</span>
                    </div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #2E7D32;"></i> Lokasi Semenanjung Badran</div>
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.6!2d105.3076663!3d-5.0563089!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNcKwMDMnMjIuNyJTIDEwNcKwMTgnMjcuNiJF!5e0!3m2!1sid!2sid!4v1650000000000!5m2!1sid!2sid" 
                        height="125" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
            </div>
        </div>

        <!-- KOLOM 2: MANAJEMEN PARIWISATA -->
        <div class="column-box">
            <div class="card-box">
                <div class="col-header bg-blue"><i class="fa-solid fa-gear"></i> 2. Manajemen Pariwisata</div>
                <div class="metric-subgrid">
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-users-gear"></i></div><div class="m-title">Pokdarwis</div><div class="m-value">{pokdarwis_val}</div><div class="m-sub">Kelompok</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-user-tie"></i></div><div class="m-title">Pengelola</div><div class="m-value">{pengelola_val}</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-shop"></i></div><div class="m-title">UMKM Aktif</div><div class="m-value">{umkm_aktif_val}</div><div class="m-sub">Unit</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-calendar"></i></div><div class="m-title">Event</div><div class="m-value">{event_val}</div><div class="m-sub">Kegiatan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-handshake"></i></div><div class="m-title">Mitra</div><div class="m-value">{mitra_val}</div><div class="m-sub">Instansi</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-hands-holding-child"></i></div><div class="m-title">Relawan</div><div class="m-value">{relawan_val}</div><div class="m-sub">Orang</div></div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-money-bill-trend-up" style="color: #1565C0;"></i> Pendapatan Pariwisata (Juta Rp)</div>
                <canvas id="revenueChart" height="95"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-wallet" style="color: #1565C0;"></i> Pengeluaran Pariwisata (%)</div>
                <canvas id="expenseChart" height="100"></canvas>
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
                <div class="section-title"><i class="fa-solid fa-people-group" style="color: #1565C0;"></i> Keterlibatan Masyarakat</div>
                <div class="community-box">
                    <div class="community-icons-group">
                        <i class="fa-solid fa-user"></i>
                        <i class="fa-solid fa-user" style="opacity: 0.8;"></i>
                        <i class="fa-solid fa-user" style="opacity: 0.6;"></i>
                    </div>
                    <div class="community-info">
                        <h4>{keterlibatan_masyarakat_val}% Partisipasi Aktif</h4>
                        <p>Masyarakat terlibat dalam homestay, event, kuliner & sadar wisata.</p>
                        <div class="progress-track">
                            <div class="progress-fill" style="width: {keterlibatan_masyarakat_val}%;"></div>
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
                    <div class="m-card"><div class="m-icon" style="color: #E1306C; background: #FCE4EC;"><i class="fa-brands fa-instagram"></i></div><div class="m-title">IG Followers</div><div class="m-value">{ig_followers_val}</div><div class="m-sub">Akun</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #000; background: #F5F5F5;"><i class="fa-brands fa-tiktok"></i></div><div class="m-title">TikTok</div><div class="m-value">{tiktok_val}</div><div class="m-sub">Akun</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-brands fa-facebook"></i></div><div class="m-title">FB Reach</div><div class="m-value">{fb_reach_val}</div><div class="m-sub">Jangkauan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #4A148C; background: #EDE7F6;"><i class="fa-solid fa-globe"></i></div><div class="m-title">Website</div><div class="m-value">{website_val}</div><div class="m-sub">Kunjungan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #4A148C; background: #EDE7F6;"><i class="fa-solid fa-comments"></i></div><div class="m-title">Review</div><div class="m-value">{review_val}</div><div class="m-sub">Ulasan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #F57F17; background: #FFF8E1;"><i class="fa-solid fa-star"></i></div><div class="m-title">Rating</div><div class="m-value">4,6</div><div class="m-sub">Sangat Baik</div></div>
                </div>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-circle-info" style="color: #4A148C;"></i> Sumber Informasi Wisatawan (%)</div>
                <canvas id="sourceChart" height="100"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #4A148C;"></i> Engagement Media Sosial</div>
                <canvas id="engagementChart" height="95"></canvas>
            </div>

            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-square-poll-vertical" style="color: #4A148C;"></i> Tingkat Kepuasan Promosi (%)</div>
                <canvas id="satisfactionPromoChart" height="95"></canvas>
            </div>

            <div class="slogan-card">
                <div class="slogan-item">
                    <i class="fa-solid fa-rocket"></i>
                    <span class="slogan-text">Berbasis Data Tepat Sasaran & Digitalisasi</span>
                </div>
                <div class="slogan-item">
                    <i class="fa-solid fa-seedling"></i>
                    <span class="slogan-text">Pariwisata Maju, Masyarakat Badransari Sejahtera</span>
                </div>
            </div>

            <div class="fade-img-container">
                <img src="https://radartv.disway.id/upload/59c6804c4c660241d4c826c4a1f31924.jpg" alt="Semenanjung Badran">
                <div class="fade-overlay">
                    <span class="fade-text">🌿 Pesona Alam Badransari</span>
                </div>
            </div>
        </div>

    </div>

    <script>
        Chart.defaults.font.family = 'Inter';
        Chart.defaults.font.size = 7.5;
        Chart.defaults.color = '#555';

        const informativeTooltip = {{
            backgroundColor: 'rgba(15, 50, 85, 0.95)',
            titleFont: {{ size: 8.5, weight: 'bold' }},
            bodyFont: {{ size: 7.5 }},
            padding: 5,
            cornerRadius: 4,
            displayColors: true,
            callbacks: {{
                label: function(context) {{
                    let label = context.dataset.label || '';
                    if (label) {{ label += ': '; }}
                    if (context.parsed.y !== null && context.parsed.y !== undefined) {{
                        label += context.parsed.y.toLocaleString('id-ID');
                    }} else if (context.parsed !== null && context.parsed !== undefined) {{
                        label += context.parsed.toLocaleString('id-ID');
                    }}
                    return label;
                }}
            }}
        }};

        const cf = {chart_factor};

        const ctxTrend = document.getElementById('trendChart').getContext('2d');
        const gradientTrend = ctxTrend.createLinearGradient(0, 0, 0, 95);
        gradientTrend.addColorStop(0, 'rgba(46, 125, 50, 0.35)');
        gradientTrend.addColorStop(1, 'rgba(46, 125, 50, 0.0)');

        new Chart(ctxTrend, {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
                datasets: [{{
                    label: 'Jumlah Pengunjung',
                    data: [240, 280, 310, 520, 610, 720, 480, 510, 420, 400, 440, 680].map(v => Math.round(v * cf)),
                    borderColor: '#2E7D32',
                    backgroundColor: gradientTrend,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 2
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: informativeTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        new Chart(document.getElementById('facilityChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Parkir', 'Toilet', 'Mushola', 'Gazebo', 'Spot Foto', 'Warung'],
                datasets: [{{
                    label: 'Jumlah Unit',
                    data: [2, 4, 2, 6, 8, 12].map(v => Math.max(1, Math.round(v * (cf > 1 ? 1.2 : cf)))),
                    backgroundColor: '#2E7D32',
                    borderRadius: 3
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: informativeTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        new Chart(document.getElementById('revenueChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Tiket', 'Parkir', 'Sewa', 'Camping', 'UMKM'],
                datasets: [{{
                    label: 'Pendapatan (Juta Rp)',
                    data: [68, 22, 18, 15, 28].map(v => parseFloat((v * cf).toFixed(1))),
                    backgroundColor: '#1565C0',
                    borderRadius: 3
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: informativeTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        new Chart(document.getElementById('expenseChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Kebersihan (30%)', 'Perawatan (25%)', 'Promosi (15%)', 'SDM (15%)', 'Infrastruktur (15%)'],
                datasets: [{{
                    label: 'Persentase',
                    data: [30, 25, 15, 15, 15],
                    backgroundColor: ['#1565C0', '#42A5F5', '#90CAF9', '#BBDEFB', '#E3F2FD'],
                    borderWidth: 1
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 7, font: {{ size: 7 }} }} }}, tooltip: informativeTooltip }} }}
        }});

        new Chart(document.getElementById('sourceChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Media Sosial (45%)', 'Teman/Keluarga (25%)', 'Google (15%)', 'Website (10%)', 'Banner (5%)'],
                datasets: [{{
                    label: 'Proporsi',
                    data: [45, 25, 15, 10, 5],
                    backgroundColor: ['#4A148C', '#7B1FA2', '#AB47BC', '#CE93D8', '#F3E5F5'],
                    borderWidth: 1
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 7, font: {{ size: 7 }} }} }}, tooltip: informativeTooltip }} }}
        }});

        new Chart(document.getElementById('engagementChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [
                    {{ label: 'Likes', data: [1200, 1500, 1800, 2200, 2600, 3100].map(v => Math.round(v * cf)), borderColor: '#4A148C', borderWidth: 2, tension: 0.35, pointRadius: 2 }},
                    {{ label: 'Comments', data: [400, 600, 700, 900, 1100, 1400].map(v => Math.round(v * cf)), borderColor: '#AB47BC', borderWidth: 2, tension: 0.35, pointRadius: 2 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 7, font: {{ size: 7 }} }} }}, tooltip: informativeTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        new Chart(document.getElementById('satisfactionPromoChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Sangat Puas', 'Puas', 'Cukup', 'Kurang'],
                datasets: [{{
                    label: 'Jumlah Responden',
                    data: [85, 62, 18, 5].map(v => Math.round(v * cf)),
                    backgroundColor: '#7B1FA2',
                    borderRadius: 3
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }}, tooltip: informativeTooltip }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(0,0,0,0.03)' }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});
    </script>
</body>
</html>
"""

import streamlit.components.v1 as components
components.html(dashboard_html, height=1210, scrolling=False)