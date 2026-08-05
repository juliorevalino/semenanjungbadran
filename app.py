import streamlit as st
import pandas as pd
import random
import warnings
import streamlit.components.v1 as components
warnings.filterwarnings('ignore')

# 1. Konfigurasi Halaman (Wide Layout & Clean Padding)
st.set_page_config(
    page_title="Smart Tourism Dashboard Desa Badransari", 
    page_icon="🌿", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- KONEKSI SUMBER DATA (GOOGLE SHEETS CSV ANDA) ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1urU4z8LupF_t4rxP-lJrKIbqdvc4X1kb7_8dGknWhFE/export?format=csv"

@st.cache_data(ttl=60)
def load_desa_data(url):
    if not url:
        return None
    try:
        df = pd.read_csv(url)
        return df
    except Exception:
        return None

df_desa = load_desa_data(SHEET_URL)

# --- FUNGSI AMBIL DATA DINAMIS DARI SPREADSHEET ---
def get_val(df, col_name, default_val):
    if df is not None and not df.empty and col_name in df.columns:
        try:
            val = df[col_name].dropna().iloc[0]
            return val
        except Exception:
            return default_val
    return default_val

def get_list_col(df, col_name, default_list):
    if df is not None and not df.empty and col_name in df.columns:
        try:
            vals = df[col_name].dropna().tolist()
            if len(vals) > 0:
                return vals
        except Exception:
            return default_list
    return default_list

# Ekstraksi Data Dasar dari Spreadsheet
base_total_pengunjung = int(get_val(df_desa, 'total_pengunjung', 4922))
base_pendapatan_total = float(get_val(df_desa, 'pendapatan_total', 152.7))
base_pengunjung_hari_ini = int(get_val(df_desa, 'pengunjung_hari_ini', 176))
tiket_val = float(get_val(df_desa, 'tiket_val', 78.4))
pokdarwis_val = int(get_val(df_desa, 'pokdarwis_val', 3))
pengelola_val = int(get_val(df_desa, 'pengelola_val', 27))
umkm_aktif_val = int(get_val(df_desa, 'umkm_aktif_val', 42))
event_val = int(get_val(df_desa, 'event_val', 8))
mitra_val = int(get_val(df_desa, 'mitra_val', 12))
relawan_val = int(get_val(df_desa, 'relawan_val', 36))

ig_followers_val = str(get_val(df_desa, 'ig_followers', '3.842'))
tiktok_val = str(get_val(df_desa, 'tiktok', '2.156'))
fb_reach_val = str(get_val(df_desa, 'fb_reach', '8.745'))
website_val = str(get_val(df_desa, 'website', '5.231'))
review_val = int(get_val(df_desa, 'review_val', 157))

lampung_prop = int(get_val(df_desa, 'propinsi_lampung_pct', 75))
luar_prop = int(get_val(df_desa, 'propinsi_luar_pct', 25))

# 2. Sidebar Filter Data & Gambar Kiri Atas
st.sidebar.markdown("""
    <div style="position: relative; text-align: center; border-radius: 8px; overflow: hidden; margin-bottom: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
        <img src="https://i.ytimg.com/vi/8PHHFvzMDac/maxresdefault.jpg" style="width: 100%; height: 130px; object-fit: cover; display: block;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(15,50,85,0.2), rgba(15,50,85,0.9)); display: flex; flex-direction: column; justify-content: flex-end; padding: 10px;">
            <h3 style="color: #FFD700 !important; font-size: 14px !important; font-weight: 800 !important; margin: 0; text-transform: uppercase;">
                Desa Wisata Semenanjung Badran
            </h3>
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown('### <i class="fa-solid fa-filter"></i> FILTER DATA', unsafe_allow_html=True)
filter_tahun = st.sidebar.selectbox("📅 Tahun", ["Semua", "2026", "2025", "2024"])
filter_bulan = st.sidebar.selectbox("🕒 Bulan", ["Semua", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
filter_jenis_wisatawan = st.sidebar.selectbox("👥 Jenis Wisatawan", ["Semua", "Lampung", "Luar Lampung"])
filter_jenis = st.sidebar.selectbox("⛰️ Jenis Wisata", ["Semua", "Wisata Alam", "Wisata Edukasi", "Kuliner & Outbound"])

# --- PENERAPAN LOGIKA FILTER INTERAKTIF ---
multiplier = 1.0
if filter_tahun == "2025": multiplier = 0.85
elif filter_tahun == "2024": multiplier = 0.70
if filter_jenis_wisatawan == "Lampung": multiplier *= (lampung_prop / 100)
elif filter_jenis_wisatawan == "Luar Lampung": multiplier *= (luar_prop / 100)

total_pengunjung_val = int(base_total_pengunjung * multiplier)
pendapatan_total_val = round(base_pendapatan_total * multiplier, 1)
pengunjung_hari_ini_val = int(base_pengunjung_hari_ini * multiplier)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); text-align: center;">
        <p style="font-size: 10px; font-weight: 700; color: #FFD700; margin:0; text-transform: uppercase;">Status Filter Aktif</p>
        <p style="font-size: 10px; font-weight: 600; color: white; margin: 3px 0 0 0;">Tahun: {filter_tahun} | Wisatawan: {filter_jenis_wisatawan}</p>
    </div>
""", unsafe_allow_html=True)

# Ambil data Grafik & Event
trend_data = get_list_col(df_desa, 'trend_pengunjung', [240, 280, 310, 520, 610, 720, 480, 510, 420, 400, 440, 680])
facility_data = get_list_col(df_desa, 'fasilitas_unit', [2, 4, 2, 6, 8, 12])
revenue_data = get_list_col(df_desa, 'pendapatan_kategori', [68, 22, 18, 15, 28])
origin_data = get_list_col(df_desa, 'asal_wisatawan_pct', [55, 17, 10, 7, 6])
promo_data = get_list_col(df_desa, 'promo_kontribusi', [35, 25, 15, 15, 10])

event_dates = get_list_col(df_desa, 'event_tanggal', ["14 Jan", "18 Feb", "24 Mar", "12 Mei", "20 Jul"])
event_names = get_list_col(df_desa, 'event_nama', ["Festival Desa Badransari", "Pasar UMKM Kreatif", "Lomba Perahu Tradisional", "Camping & Outbound", "Festival Kuliner Desa"])
current_events = list(zip(event_dates, event_names))
event_html_items = "".join([f'<div class="event-item"><span class="event-date">{date}</span><span class="event-name">{name}</span></div>' for date, name in current_events])

# 3. Styling CSS untuk Sidebar & Konsistensi Tampilan
st.markdown("""
    <style>
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0F3255 !important;
        overflow-y: auto !important;
        max-height: 100vh !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-baseweb="popover"], [data-baseweb="menu"] { z-index: 999999 !important; }
    iframe { border: none; border-radius: 8px; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

dashboard_html = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ font-family: 'Inter', sans-serif; box-sizing: border-box; }}
        html, body {{ background-color: #F0F4F8; margin: 0; padding: 0 0 40px 0; width: 100%; max-width: 100%; overflow-x: hidden; }}
        .top-banner {{
            background: linear-gradient(rgba(15, 50, 85, 0.88), rgba(15, 50, 85, 0.78)), 
                        url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2000&auto=format&fit=crop') center/cover;
            padding: 12px 18px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); width: 100%;
        }}
        .logo-area {{ display: flex; align-items: center; gap: 14px; }}
        .title-area h1 {{ font-size: 16px; font-weight: 800; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; color: #FFD700; }}
        .title-area p {{ font-size: 10.5px; font-weight: 600; margin: 2px 0 0 0; color: #E0E0E0; }}
        .stats-group {{ display: flex; gap: 8px; }}
        .stat-item {{ background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.35); padding: 5px 10px; border-radius: 6px; text-align: center; }}
        .stat-item span {{ display: block; font-size: 8px; font-weight: 700; color: #FFD700; text-transform: uppercase; }}
        .stat-item strong {{ font-size: 12px; font-weight: 800; color: white; }}
        .three-column-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-bottom: 10px; width: 100%; }}
        .column-box {{ display: flex; flex-direction: column; gap: 10px; width: 100%; min-width: 0; }}
        .card-box {{ background: white; border-radius: 8px; padding: 10px 12px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); width: 100%; overflow: hidden; }}
        canvas {{ max-width: 100% !important; }}
        .col-header {{ padding: 8px 12px; border-radius: 6px; font-weight: 800; color: white; font-size: 11px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; }}
        .bg-green {{ background: #2E7D32; }}
        .bg-blue {{ background: #1565C0; }}
        .bg-purple {{ background: #4A148C; }}
        .metric-subgrid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; }}
        .m-card {{ background: #FAFAFA; border-radius: 6px; padding: 6px 4px; border: 1px solid #EAEAEA; text-align: center; height: 80px; display: flex; flex-direction: column; justify-content: center; align-items: center; min-width: 0; }}
        .m-icon {{ font-size: 11px; margin-bottom: 3px; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
        .m-title {{ font-size: 7.5px; font-weight: 800; color: #555; text-transform: uppercase; line-height: 1.2; width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        .m-value {{ font-size: 12px; font-weight: 800; color: #111; margin: 2px 0; }}
        .m-sub {{ font-size: 7px; font-weight: 700; color: #777; }}
        .section-title {{ font-size: 10.5px; font-weight: 800; color: #333; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; text-transform: uppercase; border-bottom: 2px solid #F0F0F0; padding-bottom: 4px; }}
        .proportion-container {{ margin-top: 6px; }}
        .proportion-bar-wrapper {{ display: flex; height: 18px; border-radius: 6px; overflow: hidden; background: #eee; margin: 6px 0; }}
        .prop-segment-1 {{ background: #2E7D32; width: {lampung_prop}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 9px; font-weight: 800; }}
        .prop-segment-2 {{ background: #1565C0; width: {luar_prop}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 9px; font-weight: 800; }}
        .prop-legend {{ display: flex; justify-content: space-between; font-size: 9px; font-weight: 700; color: #555; }}
        .flow-container {{ display: flex; flex-direction: column; gap: 4px; align-items: center; }}
        .flow-node {{ background: #E8F5E9; border: 1px solid #2E7D32; color: #1E3A1E; padding: 6px 10px; border-radius: 4px; font-size: 9.5px; font-weight: 800; width: 100%; text-align: center; }}
        .flow-node.blue {{ background: #E3F2FD; border-color: #1565C0; color: #0D47A1; }}
        .flow-node.orange {{ background: #FFF8E1; border-color: #F57F17; color: #E65100; }}
        .flow-node.purple {{ background: #EDE7F6; border-color: #4A148C; color: #311B92; }}
        .flow-arrow {{ font-size: 9px; color: #666; margin: -2px 0; }}
        .community-box {{ display: flex; align-items: center; gap: 12px; background: #E8F5E9; padding: 8px 10px; border-radius: 6px; border: 1px solid #C8E6C9; }}
        .progress-track {{ background: #C8E6C9; height: 6px; border-radius: 3px; width: 100%; overflow: hidden; }}
        .progress-fill {{ background: #2E7D32; height: 100%; width: 78%; border-radius: 3px; }}
        .event-list {{ display: flex; flex-direction: column; gap: 4px; }}
        .event-item {{ display: flex; align-items: center; background: #FAFAFA; padding: 5px 8px; border-radius: 4px; border-left: 3px solid #1565C0; font-size: 9.5px; gap: 8px; }}
        .event-date {{ font-weight: 800; color: #1565C0; min-width: 45px; }}
        .event-name {{ font-weight: 600; color: #333; }}
        .footer-banner {{ 
            background: linear-gradient(135deg, #0B2540 0%, #0F3255 50%, #1A4975 100%); 
            border: 2px solid #FFD700; color: white; padding: 10px 18px; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; margin-top: 5px; margin-bottom: 15px; width: 100%;
        }}
        .siger-img {{ height: 48px; width: 70px; object-fit: cover; border-radius: 6px; border: 1.5px solid #FFD700; }}
        .slogan-content {{ text-align: center; flex-grow: 1; padding: 0 15px; }}
        .slogan-title {{ font-size: 12px; font-weight: 800; color: #FFD700; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 3px; }}
        .slogan-text {{ font-size: 10px; font-weight: 600; color: #F0F4F8; font-style: italic; }}
    </style>
</head>
<body>
    <div class="top-banner">
        <div class="logo-area">
            <div class="title-area">
                <h1>Smart Tourism Dashboard — Desa Badransari</h1>
                <p>Kecamatan Punggur, Kabupaten Lampung Tengah (Filter: {filter_tahun} / {filter_jenis_wisatawan})</p>
            </div>
        </div>
        <div class="stats-group">
            <div class="stat-item">
                <span>👥 Pengunjung</span>
                <strong>{total_pengunjung_val:,} Orang</strong>
            </div>
            <div class="stat-item">
                <span>💰 Pendapatan</span>
                <strong>Rp {pendapatan_total_val} Juta</strong>
            </div>
            <div class="stat-item">
                <span>⭐ Kepuasan</span>
                <strong>88% Baik</strong>
            </div>
        </div>
    </div>
    
    <div class="three-column-grid">
        <!-- KOLOM 1: LAYANAN PARIWISATA -->
        <div class="column-box">
            <div class="card-box">
                <div class="col-header bg-green"><i class="fa-solid fa-umbrella-beach"></i> 1. Layanan Pariwisata</div>
                <div class="metric-subgrid">
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-users"></i></div><div class="m-title">Pengunjung</div><div class="m-value">{total_pengunjung_val:,}</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-person-walking"></i></div><div class="m-title">Hari Ini</div><div class="m-value">{pengunjung_hari_ini_val}</div><div class="m-sub">Orang</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-ticket"></i></div><div class="m-title">Tiket</div><div class="m-value">{tiket_val}</div><div class="m-sub">Juta Rp</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-star"></i></div><div class="m-title">Kepuasan</div><div class="m-value">88%</div><div class="m-sub">Sangat Baik</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-store"></i></div><div class="m-title">UMKM</div><div class="m-value">{umkm_aktif_val}</div><div class="m-sub">Unit</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-house"></i></div><div class="m-title">Homestay</div><div class="m-value">15</div><div class="m-sub">Unit</div></div>
                </div>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #2E7D32;"></i> Tren Kunjungan Wisatawan</div>
                <canvas id="trendChart" height="115"></canvas>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-umbrella" style="color: #2E7D32;"></i> Fasilitas Wisata (Jumlah Unit)</div>
                <canvas id="facilityChart" height="115"></canvas>
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
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.6!2d105.2!3d-5.1!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNcKwMDYnMDAnUzEwNcKwMTInMDAuMCJF!5e0!3m2!1sid!2sid!4v1650000000000!5m2!1sid!2sid" 
                    width="100%" height="120" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-triangle-exclamation" style="color: #2E7D32;"></i> Keluhan Wisatawan</div>
                <canvas id="complaintChart" height="115"></canvas>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-images" style="color: #2E7D32;"></i> Keindahan Semenanjung Badran</div>
                <div style="position: relative; overflow: hidden; border-radius: 6px; height: 160px;">
                    <div id="carouselSlides" style="display: flex; transition: transform 0.4s ease-in-out; height: 100%;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzLiEBWTG_wG6AKrTAWj86DqjfI5IvUm8BD0Ji5mhclWEC8uguyFfGCQfF&s=10" style="width: 100%; height: 100%; object-fit: cover; flex-shrink: 0;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnqCV6hftdg7YMrMpsJI0N_3VaX0mI1sIDuX-gIi82LkSvks9RTyA7gJg&s=10" style="width: 100%; height: 100%; object-fit: cover; flex-shrink: 0;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8weTv8xm9MnaCyFb6x05l11VxYjj8kKBmpCvEO7J7dC6w8KVGspk9XiI&s=10" style="width: 100%; height: 100%; object-fit: cover; flex-shrink: 0;">
                    </div>
                    <button onclick="prevSlide()" style="position: absolute; top: 50%; left: 6px; transform: translateY(-50%); background: rgba(15,50,85,0.7); color: white; border: none; width: 26px; height: 26px; border-radius: 50%; cursor: pointer; font-weight: bold; font-size: 12px; z-index: 10;">❮</button>
                    <button onclick="nextSlide()" style="position: absolute; top: 50%; right: 6px; transform: translateY(-50%); background: rgba(15,50,85,0.7); color: white; border: none; width: 26px; height: 26px; border-radius: 50%; cursor: pointer; font-weight: bold; font-size: 12px; z-index: 10;">❯</button>
                </div>
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
                <div class="section-title"><i class="fa-solid fa-calendar-days" style="color: #1565C0;"></i> Jadwal Event Desa (Dari Spreadsheet)</div>
                <div class="event-list">
                    {event_html_items}
                </div>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-money-bill-trend-up" style="color: #1565C0;"></i> Pendapatan Pariwisata (Juta Rp)</div>
                <canvas id="revenueChart" height="115"></canvas>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-wallet" style="color: #1565C0;"></i> Pengeluaran Pariwisata</div>
                <canvas id="expenseChart" height="115"></canvas>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-people-group" style="color: #1565C0;"></i> Tingkat Keterlibatan Masyarakat</div>
                <div class="community-box">
                    <div style="flex-grow: 1;">
                        <h4 style="margin: 0; font-size: 11.5px; color: #1E3A1E; font-weight: 800;">78% Partisipasi Aktif</h4>
                        <p style="margin: 2px 0 4px 0; font-size: 9px; color: #388E3C; font-weight: 600;">Masyarakat terlibat dalam homestay, event, kuliner & sadar wisata.</p>
                        <div class="progress-track"><div class="progress-fill"></div></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- KOLOM 3: PEMASARAN PARIWISATA (LENGKAP DENGAN KEPUASAN & PROMOSI) -->
        <div class="column-box">
            <div class="card-box">
                <div class="col-header bg-purple"><i class="fa-solid fa-bullhorn"></i> 3. Pemasaran & Promosi</div>
                <div class="metric-subgrid">
                    <div class="m-card"><div class="m-icon" style="color: #E1306C; background: #FCE4EC;"><i class="fa-brands fa-instagram"></i></div><div class="m-title">IG Followers</div><div class="m-value">{ig_followers_val}</div><div class="m-sub">Akun</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #000; background: #F5F5F5;"><i class="fa-brands fa-tiktok"></i></div><div class="m-title">TikTok</div><div class="m-value">{tiktok_val}</div><div class="m-sub">Akun</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-brands fa-facebook"></i></div><div class="m-title">FB Reach</div><div class="m-value">{fb_reach_val}</div><div class="m-sub">Jangkauan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #4A148C; background: #EDE7F6;"><i class="fa-solid fa-globe"></i></div><div class="m-title">Website</div><div class="m-value">{website_val}</div><div class="m-sub">Kunjungan</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-face-smile"></i></div><div class="m-title">Kepuasan</div><div class="m-value">88%</div><div class="m-sub">Sangat Baik</div></div>
                    <div class="m-card"><div class="m-icon" style="color: #F57F17; background: #FFF8E1;"><i class="fa-solid fa-bullhorn"></i></div><div class="m-title">Promo Efektif</div><div class="m-value">92%</div><div class="m-sub">Target Jangkau</div></div>
                </div>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #4A148C;"></i> Asal Wisatawan</div>
                <canvas id="originChart" height="115"></canvas>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-share-nodes" style="color: #4A148C;"></i> Media Promosi (Kontribusi %)</div>
                <canvas id="promoChart" height="115"></canvas>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #4A148C;"></i> Engagement Media Sosial</div>
                <canvas id="engagementChart" height="115"></canvas>
            </div>
            <div class="card-box">
                <div class="section-title"><i class="fa-solid fa-circle-info" style="color: #4A148C;"></i> Sumber Informasi Wisatawan</div>
                <canvas id="sourceChart" height="115"></canvas>
            </div>
        </div>
    </div>

    <!-- FOOTER SLOGAN -->
    <div class="footer-banner">
        <div class="siger-img-box"><img class="siger-img" src="https://traverse.id/wp-content/uploads/2018/03/Mahkota-Siger-Simbol-Kebanggaan-Lampung.jpg" alt="Siger"></div>
        <div class="slogan-content">
            <div class="slogan-title">Desa Wisata Semenanjung Badran</div>
            <div class="slogan-text">“Bersama Membangun Pariwisata Desa Badransari yang Berkelanjutan, Berdaya Saing, dan Berbasis Masyarakat”</div>
        </div>
        <div class="siger-img-box"><img class="siger-img" src="https://traverse.id/wp-content/uploads/2018/03/Mahkota-Siger-Simbol-Kebanggaan-Lampung.jpg" alt="Siger"></div>
    </div>

    <script>
        let currentSlideIdx = 0;
        function showSlide(idx) {{
            const slides = document.getElementById('carouselSlides');
            currentSlideIdx = (idx + 3) % 3;
            if(slides) slides.style.transform = `translateX(-${{currentSlideIdx * 100}}%)`;
        }}
        function nextSlide() {{ showSlide(currentSlideIdx + 1); }}
        function prevSlide() {{ showSlide(currentSlideIdx - 1); }}
        setInterval(nextSlide, 3500);

        const trendValues = {trend_data};
        const facilityValues = {facility_data};
        const revenueValues = {revenue_data};
        const originValues = {origin_data};
        const promoValues = {promo_data};

        new Chart(document.getElementById('trendChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
                datasets: [{{ data: trendValues, borderColor: '#2E7D32', borderWidth: 2, fill: true, tension: 0.35, pointRadius: 2.5, backgroundColor: 'rgba(46,125,50,0.2)' }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        new Chart(document.getElementById('facilityChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Parkir', 'Toilet', 'Mushola', 'Gazebo', 'Spot Foto', 'Warung'],
                datasets: [{{ data: facilityValues, backgroundColor: '#2E7D32', borderRadius: 4 }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        new Chart(document.getElementById('complaintChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Kebersihan', 'Jalan', 'Toilet', 'Parkir', 'Informasi'],
                datasets: [{{ data: [28, 22, 20, 15, 9], backgroundColor: '#388E3C', borderRadius: 4 }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});

        new Chart(document.getElementById('revenueChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Tiket', 'Parkir', 'Sewa', 'Camping', 'UMKM'],
                datasets: [{{ data: revenueValues, backgroundColor: '#1565C0', borderRadius: 4 }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        new Chart(document.getElementById('expenseChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Kebersihan (30%)', 'Perawatan (25%)', 'Promosi (15%)', 'SDM (15%)', 'Infrastruktur (15%)'],
                datasets: [{{ data: [30, 25, 15, 15, 15], backgroundColor: ['#1565C0', '#42A5F5', '#90CAF9', '#BBDEFB', '#E3F2FD'] }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 8, font: {{ size: 8 }} }} }} }} }}
        }});

        new Chart(document.getElementById('originChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Lampung', 'Sumsel', 'DKI', 'Banten', 'Jabar'],
                datasets: [{{ data: originValues, backgroundColor: '#4A148C', borderRadius: 4 }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        new Chart(document.getElementById('promoChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Instagram', 'TikTok', 'Facebook', 'Website', 'YouTube'],
                datasets: [{{ data: promoValues, backgroundColor: '#7B1FA2', borderRadius: 4 }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        new Chart(document.getElementById('engagementChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [
                    {{ label: 'Likes', data: [1200, 1500, 2100, 2800, 3200, 3900], borderColor: '#4A148C', tension: 0.3, pointRadius: 2 }},
                    {{ label: 'Comments', data: [300, 450, 600, 800, 950, 1100], borderColor: '#7B1FA2', tension: 0.3, pointRadius: 2 }},
                    {{ label: 'Shares', data: [150, 220, 340, 450, 520, 680], borderColor: '#BA68C8', tension: 0.3, pointRadius: 2 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 6, font: {{ size: 8 }} }} }} }} }}
        }});

        new Chart(document.getElementById('sourceChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Sosmed', 'Teman', 'Berita', 'Event', 'Lainnya'],
                datasets: [{{ data: [45, 25, 15, 10, 5], backgroundColor: '#9C27B0', borderRadius: 4 }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=1550, scrolling=True)