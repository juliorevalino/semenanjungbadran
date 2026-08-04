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

# 2. Styling CSS untuk Menghilangkan Ruang Kosong & Memperindah Tampilan
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0F3255 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
    }
    .stSelectbox div[data-baseweb="select"] span {
        color: #333 !important;
    }
    .sidebar-title {
        text-align: center; 
        padding: 5px 0 15px 0; 
        border-bottom: 1px solid rgba(255,255,255,0.2); 
        margin-bottom: 15px;
    }
    .sidebar-title h3 {
        color: #FFD700 !important; 
        font-size: 14px; 
        font-weight: 800; 
        margin: 0; 
        line-height: 1.4; 
        text-transform: uppercase;
    }
    .sidebar-title p { 
        color: #E0E0E0 !important; 
        font-size: 10px; 
        margin: 4px 0 0 0; 
    }
    iframe { border: none; border-radius: 8px; }
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
filter_tahun = st.sidebar.selectbox("📅 Tahun", ["2024", "2025", "2026"])
filter_bulan = st.sidebar.selectbox("🕒 Bulan", ["Semua", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
filter_jenis_wisatawan = st.sidebar.selectbox("👥 Jenis Wisatawan", ["Semua", "Lampung", "Luar Lampung"])
filter_asal = st.sidebar.selectbox("📍 Asal Daerah", ["Semua", "Lampung Tengah", "Bandar Lampung", "Luar Lampung"])
filter_jenis = st.sidebar.selectbox("⛰️ Jenis Wisata", ["Semua", "Wisata Alam", "Wisata Edukasi", "Kuliner & Outbound"])

# ==========================================
# LOGIKA FILTER (Dinamis)
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

# 4. Konten HTML/CSS Dashboard (F-String untuk Integrasi Python & Chart.js)
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
        
        /* Banner Atas dengan Foto Semenanjung Badran */
        .top-banner {{
            background: linear-gradient(rgba(15, 50, 85, 0.85), rgba(15, 50, 85, 0.7)), 
                        url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2000&auto=format&fit=crop') center/cover;
            padding: 18px 25px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; color: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .title-area h1 {{ font-size: 18px; font-weight: 800; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; color: #FFD700; }}
        .title-area p {{ font-size: 11px; font-weight: 600; margin: 3px 0 0 0; color: #E0E0E0; }}
        
        .stats-group {{ display: flex; gap: 10px; }}
        .stat-item {{ background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.3); padding: 6px 12px; border-radius: 8px; text-align: center; }}
        .stat-item span {{ display: block; font-size: 8px; font-weight: 700; color: #FFD700; text-transform: uppercase; }}
        .stat-item strong {{ font-size: 13px; font-weight: 800; color: white; }}

        /* Grid 3 Kolom Utama */
        .main-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 12px; }}
        .col-card {{ background: white; border-radius: 10px; padding: 12px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
        
        .col-header {{ padding: 8px 10px; border-radius: 6px; font-weight: 800; color: white; font-size: 11px; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; }}
        .bg-green {{ background: #2E7D32; }}
        .bg-blue {{ background: #1565C0; }}
        .bg-purple {{ background: #4A148C; }}

        .metric-subgrid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }}
        .m-card {{ background: #FAFAFA; border-radius: 6px; padding: 6px 4px; border: 1px solid #EAEAEA; text-align: center; height: 80px; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
        .m-icon {{ font-size: 10px; margin-bottom: 2px; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
        .m-title {{ font-size: 7px; font-weight: 800; color: #555; text-transform: uppercase; line-height: 1.1; width: 100%; }}
        .m-value {{ font-size: 12px; font-weight: 800; color: #111; margin: 1px 0; }}
        .m-sub {{ font-size: 7px; font-weight: 700; color: #777; }}

        /* Baris Grid Dashboard */
        .dashboard-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }}
        .dashboard-row-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px; }}
        
        .card-box {{ background: white; border-radius: 10px; padding: 12px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
        .section-title {{ font-size: 10px; font-weight: 800; color: #333; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; text-transform: uppercase; border-bottom: 2px solid #F0F0F0; padding-bottom: 5px; }}

        /* Struktur Organisasi & Pengelolaan */
        .flow-container {{ display: flex; flex-direction: column; gap: 6px; align-items: center; padding: 2px 0; }}
        .flow-node {{ background: #E8F5E9; border: 1px solid #2E7D32; color: #1E3A1E; padding: 6px 12px; border-radius: 6px; font-size: 9px; font-weight: 800; width: 100%; text-align: center; }}
        .flow-node.blue {{ background: #E3F2FD; border-color: #1565C0; color: #0D47A1; }}
        .flow-node.orange {{ background: #FFF8E1; border-color: #F57F17; color: #E65100; }}
        .flow-node.purple {{ background: #EDE7F6; border-color: #4A148C; color: #311B92; }}
        .flow-arrow {{ font-size: 10px; color: #666; margin: -3px 0; }}

        /* Keterlibatan Masyarakat Card dengan Ilustrasi Orang */
        .community-box {{ display: flex; align-items: center; gap: 15px; background: #E8F5E9; padding: 12px; border-radius: 8px; border: 1px solid #C8E6C9; margin-top: 8px; }}
        .community-icon {{ font-size: 28px; color: #2E7D32; background: white; padding: 12px; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .community-info h4 {{ margin: 0; font-size: 13px; color: #1E3A1E; font-weight: 800; }}
        .community-info p {{ margin: 3px 0 0 0; font-size: 10px; color: #388E3C; font-weight: 600; }}

        /* Event List */
        .event-list {{ display: flex; flex-direction: column; gap: 5px; }}
        .event-item {{ display: flex; align-items: center; background: #FAFAFA; padding: 5px 8px; border-radius: 6px; border-left: 3px solid #2E7D32; font-size: 9px; gap: 8px; }}
        .event-date {{ font-weight: 800; color: #2E7D32; min-width: 50px; }}
        .event-name {{ font-weight: 600; color: #333; }}
    </style>
</head>
<body>

    <!-- Banner Utama -->
    <div class="top-banner">
        <div class="title-area">
            <h1>🌿 Smart Tourism Dashboard — Desa Badransari</h1>
            <p>Kecamatan Punggur, Kabupaten Lampung Tengah • Program Hibah BIMA ITERA</p>
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

    <!-- 3 Kolom Utama -->
    <div class="main-grid">
        <!-- KOLOM 1 -->
        <div class="col-card">
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

        <!-- KOLOM 2 -->
        <div class="col-card">
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

        <!-- KOLOM 3 -->
        <div class="col-card">
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
    </div>

    <!-- ROW 1: Tren Kunjungan & Google Maps Interaktif -->
    <div class="dashboard-row">
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #2E7D32;"></i> Grafik Tren Kunjungan Wisatawan</div>
            <canvas id="trendChart" height="135"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #1565C0;"></i> Lokasi Semenanjung Badran (Peta Interaktif)</div>
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.6!2d105.2!3d-5.1!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNcKwMDYnMDAnUzEwNcKwMTInMDAuMCJF!5e0!3m2!1sid!2sid!4v1650000000000!5m2!1sid!2sid" 
                    width="100%" height="150" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
        </div>
    </div>

    <!-- ROW 2: Struktur Pengelolaan, Keterlibatan Masyarakat & Media Promosi -->
    <div class="dashboard-row-3">
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
            <div class="section-title"><i class="fa-solid fa-people-group" style="color: #2E7D32;"></i> Keterlibatan Masyarakat</div>
            <div class="community-box">
                <div class="community-icon"><i class="fa-solid fa-users-viewfinder"></i></div>
                <div class="community-info">
                    <h4>78% Partisipasi Aktif</h4>
                    <p>Masyarakat terlibat langsung dalam pengelolaan homestay, event desa, kuliner, dan sadar wisata.</p>
                </div>
            </div>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-bullhorn" style="color: #4A148C;"></i> Media Promosi (Kontribusi)</div>
            <canvas id="promoChart" height="145"></canvas>
        </div>
    </div>

    <!-- ROW 3: Fasilitas Wisata (Jumlah Absolut) & Jenis Wisatawan (2 Kategori) & Jadwal Event -->
    <div class="dashboard-row-3">
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-umbrella" style="color: #2E7D32;"></i> Fasilitas Wisata (Jumlah Unit)</div>
            <canvas id="facilityChart" height="150"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-users-rectangle" style="color: #1565C0;"></i> Jenis Wisatawan</div>
            <canvas id="visitorTypeChart" height="150"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-calendar-days" style="color: #4A148C;"></i> Jadwal Event Desa</div>
            <div class="event-list">
                <div class="event-item"><span class="event-date">14 Jan</span><span class="event-name">Festival Desa Badransari</span></div>
                <div class="event-item"><span class="event-date">18 Feb</span><span class="event-name">Pasar UMKM Kreatif</span></div>
                <div class="event-item"><span class="event-date">24 Mar</span><span class="event-name">Lomba Perahu Tradisional</span></div>
                <div class="event-item"><span class="event-date">12 Mei</span><span class="event-name">Camping & Outbound</span></div>
                <div class="event-item"><span class="event-date">20 Jul</span><span class="event-name">Festival Kuliner Desa</span></div>
            </div>
        </div>
    </div>

    <script>
        // 1. Trend Chart
        new Chart(document.getElementById('trendChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
                datasets: [{{
                    label: 'Pengunjung',
                    data: [240, 280, 310, 520, 610, 720, 480, 510, 420, 400, 440, 680],
                    borderColor: '#2E7D32',
                    backgroundColor: 'rgba(46, 125, 50, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        // 2. Media Promosi (Horizontal Bar Chart)
        new Chart(document.getElementById('promoChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Instagram', 'TikTok', 'Facebook', 'Website', 'Word of Mouth'],
                datasets: [{{
                    label: 'Kontribusi (%)',
                    data: [35, 25, 15, 10, 15],
                    backgroundColor: '#4A148C'
                }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ beginAtZero: true, max: 40 }} }} }}
        }});

        // 3. Facility Chart (Jumlah Absolut / Unit)
        new Chart(document.getElementById('facilityChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Parkir', 'Toilet', 'Mushola', 'Gazebo', 'Spot Foto', 'Warung'],
                datasets: [{{
                    label: 'Jumlah Unit',
                    data: [2, 4, 2, 6, 8, 12],
                    backgroundColor: '#2E7D32'
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        // 4. Visitor Type Chart (Hanya 2 Kategori: Lampung & Luar Lampung)
        new Chart(document.getElementById('visitorTypeChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Lampung (75%)', 'Luar Lampung (25%)'],
                datasets: [{{
                    data: [75, 25],
                    backgroundColor: ['#2E7D32', '#1565C0']
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 9 }} }} }} }} }}
        }});
    </script>
</body>
</html>
"""

# Render ke dalam Streamlit Component
import streamlit.components.v1 as components
components.html(dashboard_html, height=1350, scrolling=True)