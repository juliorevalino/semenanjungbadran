import streamlit as st
import pandas as pd
import random
import warnings
warnings.filterwarnings('ignore')

# 1. Konfigurasi Halaman (Wide Layout)
st.set_page_config(page_title="Smart Tourism Dashboard", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# 2. Styling CSS Streamlit
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
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
        text-align: center; padding: 5px 0 15px 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px;
    }
    .sidebar-title h3 {
        color: #FFD700 !important; font-size: 14px; font-weight: 800; margin: 0; line-height: 1.4; text-transform: uppercase;
    }
    .sidebar-title p { color: #E0E0E0 !important; font-size: 10px; margin: 4px 0 0 0; }
    iframe { border: none; }
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
st.sidebar.selectbox("📍 Asal Daerah", ["Semua", "Lampung Tengah", "Bandar Lampung", "Luar Lampung"])
st.sidebar.selectbox("⛰️ Jenis Wisata", ["Semua", "Wisata Alam", "Wisata Edukasi", "Kuliner & Outbound"])

# ==========================================
# LOGIKA FILTER (Simulasi Data Dinamis)
# ==========================================
multiplier = 1.0
if filter_tahun == "2025": multiplier = 1.15
elif filter_tahun == "2026": multiplier = 1.35

if filter_bulan != "Semua": 
    multiplier = multiplier * 0.1 

total_pengunjung = int(4280 * multiplier)
pendapatan = round(152.7 * multiplier, 1)
kepuasan = random.randint(82, 95)
tiket_rp = round(68.2 * multiplier, 1)
pengunjung_hari_ini = int(156 * multiplier * (random.uniform(0.8, 1.2)))

# 4. Konten HTML/CSS Dashboard (Dengan Fixed Container Height untuk Mencegah Blank/Putih)
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
        
        /* BANNER ATAS */
        .top-banner {{
            background: linear-gradient(rgba(15, 50, 85, 0.85), rgba(15, 50, 85, 0.7)), 
                        url('https://images.unsplash.com/photo-1542361345-89e58247f2d5?q=80&w=2070&auto=format&fit=crop') center/cover;
            padding: 18px 25px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; color: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .title-area h1 {{ font-size: 18px; font-weight: 800; margin: 0; text-transform: uppercase; letter-spacing: 1px; color: #FFD700; }}
        .title-area p {{ font-size: 11px; font-weight: 600; margin: 4px 0 0 0; color: #E0E0E0; }}
        
        .stats-group {{ display: flex; gap: 12px; }}
        .stat-item {{ background: rgba(255,255,255,0.1); backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.2); padding: 8px 15px; border-radius: 8px; text-align: center; }}
        .stat-item span {{ display: block; font-size: 8px; font-weight: 700; color: #FFF; text-transform: uppercase; letter-spacing: 0.5px; }}
        .stat-item strong {{ font-size: 16px; font-weight: 800; color: #69F0AE; }}

        /* 3 KOLOM UTAMA */
        .main-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px; }}
        .col-card {{ background: white; border-radius: 10px; padding: 15px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 12px; }}
        
        .col-header {{ padding: 10px 12px; border-radius: 6px; font-weight: 800; color: white; font-size: 12px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .bg-green {{ background: linear-gradient(135deg, #2E7D32, #1B5E20); }}
        .bg-blue {{ background: linear-gradient(135deg, #1565C0, #0D47A1); }}
        .bg-purple {{ background: linear-gradient(135deg, #4A148C, #311B92); }}

        /* KARTU METRIK KECIL */
        .metric-subgrid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }}
        .m-card {{ background: #FAFAFA; border-radius: 6px; padding: 8px 4px; border: 1px solid #EAEAEA; text-align: center; }}
        .m-icon {{ font-size: 12px; margin: 0 auto 4px auto; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
        .m-title {{ font-size: 7px; font-weight: 800; color: #555; text-transform: uppercase; }}
        .m-value {{ font-size: 13px; font-weight: 800; color: #111; margin: 2px 0; }}
        
        .section-title {{ font-size: 11px; font-weight: 800; color: #333; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; text-transform: uppercase; border-bottom: 2px solid #F0F0F0; padding-bottom: 4px; }}
        
        /* PENTING: Kontainer Chart Diberi Tinggi Tetap & Relative agar tidak Blank/Putih */
        .chart-container {{ 
            background: white; 
            padding: 8px; 
            border-radius: 6px; 
            border: 1px solid #f0f0f0; 
            position: relative; 
            height: 165px; 
            width: 100%;
        }}
        
        .map-container {{ border-radius: 6px; overflow: hidden; border: 1px solid #E0E0E0; height: 165px; width: 100%; }}
        
        .people-icons {{ display: flex; gap: 5px; color: #2E7D32; font-size: 16px; align-items: center; justify-content: center; margin-bottom: 5px; }}
        .people-icons .inactive {{ color: #E0E0E0; }}
    </style>
</head>
<body>

    <!-- BANNER ATAS -->
    <div class="top-banner">
        <div class="title-area">
            <h1><i class="fa-solid fa-leaf"></i> Dashboard Pariwisata Semenanjung Badran</h1>
            <p>Desa Badransari, Kec. Punggur, Lampung Tengah • Filter: {filter_bulan} {filter_tahun}</p>
        </div>
        <div class="stats-group">
            <div class="stat-item">
                <span>Total Pengunjung</span>
                <strong>{total_pengunjung:,} Org</strong>
            </div>
            <div class="stat-item">
                <span>Pendapatan</span>
                <strong style="color: #64B5F6;">Rp {pendapatan:,.1f} Jt</strong>
            </div>
            <div class="stat-item">
                <span>Kepuasan</span>
                <strong style="color: #FFD54F;">{kepuasan}% Baik</strong>
            </div>
        </div>
    </div>

    <!-- 3 KOLOM GRID UTAMA -->
    <div class="main-grid">
        
        <!-- ==================== KOLOM 1: LAYANAN PARIWISATA ==================== -->
        <div class="col-card">
            <div class="col-header bg-green"><i class="fa-solid fa-umbrella-beach"></i> 1. Layanan Pariwisata</div>
            
            <div class="metric-subgrid">
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-users"></i></div><div class="m-title">Wisatawan</div><div class="m-value">{total_pengunjung}</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-person-walking"></i></div><div class="m-title">Hari Ini</div><div class="m-value">{pengunjung_hari_ini}</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-ticket"></i></div><div class="m-title">Tiket</div><div class="m-value">{tiket_rp} Jt</div></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #2E7D32;"></i> 1. Tren Kunjungan</div>
                <div class="chart-container"><canvas id="trendChart"></canvas></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-umbrella" style="color: #2E7D32;"></i> 2. Fasilitas Wisata</div>
                <div class="chart-container"><canvas id="facilityChart"></canvas></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-people-group" style="color: #2E7D32;"></i> 3. Jenis Wisatawan</div>
                <div class="chart-container"><canvas id="jenisWisatawanChart"></canvas></div>
            </div>
        </div>

        <!-- ==================== KOLOM 2: MANAJEMEN USAHA ==================== -->
        <div class="col-card">
            <div class="col-header bg-blue"><i class="fa-solid fa-gear"></i> 2. Manajemen Usaha & Operasional</div>
            
            <div class="metric-subgrid">
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-shop"></i></div><div class="m-title">UMKM Aktif</div><div class="m-value">42</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-bed"></i></div><div class="m-title">Homestay</div><div class="m-value">15</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-handshake"></i></div><div class="m-title">Mitra Kerja</div><div class="m-value">12</div></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-money-bill-trend-up" style="color: #1565C0;"></i> 4. Pendapatan (Juta Rp)</div>
                <div class="chart-container"><canvas id="pendapatanChart"></canvas></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-wallet" style="color: #1565C0;"></i> 5. Pengeluaran</div>
                <div class="chart-container"><canvas id="pengeluaranChart"></canvas></div>
            </div>
            
            <div>
                <div class="section-title"><i class="fa-solid fa-clipboard-question" style="color: #1565C0;"></i> 6. Keluhan Wisatawan</div>
                <div class="chart-container"><canvas id="keluhanChart"></canvas></div>
            </div>

            <div style="background: #F9F9F9; padding: 8px; border-radius: 6px; border: 1px solid #EEE;">
                <div class="section-title" style="border:none; margin-bottom:4px;"><i class="fa-solid fa-users-rays" style="color: #1565C0;"></i> Keterlibatan Masyarakat (78%)</div>
                <div class="people-icons">
                    <i class="fa-solid fa-child-reaching"></i><i class="fa-solid fa-person"></i><i class="fa-solid fa-person-dress"></i>
                    <i class="fa-solid fa-person-walking"></i><i class="fa-solid fa-child"></i><i class="fa-solid fa-person"></i>
                    <i class="fa-solid fa-person-dress"></i><i class="fa-solid fa-person inactive"></i><i class="fa-solid fa-person inactive"></i>
                </div>
            </div>
        </div>

        <!-- ==================== KOLOM 3: PEMASARAN PARIWISATA ==================== -->
        <div class="col-card">
            <div class="col-header bg-purple"><i class="fa-solid fa-bullhorn"></i> 3. Pemasaran Pariwisata</div>
            
            <div class="metric-subgrid">
                <div class="m-card"><div class="m-icon" style="color: #E1306C; background: #FCE4EC;"><i class="fa-brands fa-instagram"></i></div><div class="m-title">IG Followers</div><div class="m-value">3.8K</div></div>
                <div class="m-card"><div class="m-icon" style="color: #000; background: #F5F5F5;"><i class="fa-brands fa-tiktok"></i></div><div class="m-title">TikTok</div><div class="m-value">2.1K</div></div>
                <div class="m-card"><div class="m-icon" style="color: #F57F17; background: #FFF8E1;"><i class="fa-solid fa-star"></i></div><div class="m-title">Google Rate</div><div class="m-value">4.6</div></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-map-pin" style="color: #4A148C;"></i> 7. Asal Daerah Wisatawan</div>
                <div class="chart-container"><canvas id="asalWisatawanChart"></canvas></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-thumbs-up" style="color: #4A148C;"></i> 8. Engagement Medsos</div>
                <div class="chart-container"><canvas id="engagementChart"></canvas></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-fire" style="color: #4A148C;"></i> 9. Konten Terpopuler</div>
                <div class="chart-container"><canvas id="kontenChart"></canvas></div>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #4A148C;"></i> Lokasi Semenanjung Badran</div>
                <div class="map-container">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d127183.0560935575!2d105.197365!3d-5.0069507!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e40b7987817ebbf%3A0x4039d80b220cc30!2sPunggur%2C%20Kabupaten%20Lampung%20Tengah%2C%20Lampung!5e0!3m2!1sid!2sid!4v1700000000000!5m2!1sid!2sid" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                </div>
            </div>
        </div>
    </div>

    <!-- KONFIGURASI JAVASCRIPT CHART.JS (DENGAN maintainAspectRatio: false) -->
    <script>
        const mod = {multiplier};
        const commonOptions = {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }}
        }};
        const legendOption = {{ 
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 9 }} }} }} }} 
        }};

        // 1. Line Chart: Tren Kunjungan
        new Chart(document.getElementById('trendChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [{{
                    data: [240*mod, 280*mod, 520*mod, 610*mod, 480*mod, 510*mod],
                    borderColor: '#2E7D32', backgroundColor: 'rgba(46, 125, 50, 0.15)', borderWidth: 2, fill: true, tension: 0.4
                }}]
            }},
            options: commonOptions
        }});

        // 2. Doughnut Chart: Fasilitas Wisata
        new Chart(document.getElementById('facilityChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Spot Foto', 'Gazebo', 'Toilet', 'Mushola', 'Warung', 'Tenda'],
                datasets: [{{
                    data: [12, 8, 6, 2, 15, 20],
                    backgroundColor: ['#2E7D32', '#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9', '#FBC02D']
                }}]
            }},
            options: legendOption
        }});

        // 3. Pie Chart: Jenis Wisatawan
        new Chart(document.getElementById('jenisWisatawanChart').getContext('2d'), {{
            type: 'pie',
            data: {{
                labels: ['Keluarga', 'Rombongan', 'Pasangan', 'Individu'],
                datasets: [{{
                    data: [45, 25, 20, 10],
                    backgroundColor: ['#1E88E5', '#43A047', '#E53935', '#FDD835']
                }}]
            }},
            options: legendOption
        }});

        // 4. Bar Chart: Pendapatan Pariwisata
        new Chart(document.getElementById('pendapatanChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Tiket', 'Parkir', 'Kuliner', 'Souvenir', 'Sewa'],
                datasets: [{{
                    data: [45*mod, 15*mod, 60*mod, 20*mod, 35*mod],
                    backgroundColor: '#1976D2', borderRadius: 4
                }}]
            }},
            options: commonOptions
        }});

        // 5. Doughnut Chart: Pengeluaran Operasional
        new Chart(document.getElementById('pengeluaranChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Gaji/Honor', 'Perawatan', 'Pemasaran', 'Lainnya'],
                datasets: [{{
                    data: [40, 25, 15, 20],
                    backgroundColor: ['#D32F2F', '#1976D2', '#388E3C', '#FBC02D']
                }}]
            }},
            options: legendOption
        }});

        // 6. Bar Chart: Keluhan Wisatawan
        new Chart(document.getElementById('keluhanChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Kebersihan', 'Akses', 'Fasilitas', 'Harga'],
                datasets: [{{
                    data: [15, 28, 10, 5],
                    backgroundColor: '#E53935', borderRadius: 4
                }}]
            }},
            options: commonOptions
        }});

        // 7. Doughnut Chart: Asal Daerah Wisatawan
        new Chart(document.getElementById('asalWisatawanChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Lampung Tengah', 'Bandar Lampung', 'Luar', 'Lainnya'],
                datasets: [{{
                    data: [50, 25, 15, 10],
                    backgroundColor: ['#6A1B9A', '#8E24AA', '#AB47BC', '#CE93D8']
                }}]
            }},
            options: legendOption
        }});

        // 8. Line Chart: Engagement Media Sosial
        new Chart(document.getElementById('engagementChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [{{
                    data: [1200*mod, 1500*mod, 1400*mod, 2100*mod, 1800*mod, 2500*mod],
                    borderColor: '#E1306C', backgroundColor: 'rgba(225, 48, 108, 0.1)', borderWidth: 2, fill: true, tension: 0.3
                }}]
            }},
            options: commonOptions
        }});

        // 9. Horizontal Bar Chart: Konten Terpopuler
        newChart(document.getElementById('kontenChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Drone', 'Kuliner', 'Budaya', 'Spot Foto'],
                datasets: [{{
                    data: [8500, 6200, 4800, 3100],
                    backgroundColor: ['#E1306C', '#1DA1F2', '#4267B2', '#FF0000'],
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});
    </script>
</body>
</html>
"""

# Render ke Streamlit dengan tinggi komponen yang pas
st.components.v1.html(dashboard_html, height=1650, scrolling=True)