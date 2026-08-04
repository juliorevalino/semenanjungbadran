import streamlit as st
import pandas as pd
import random
import warnings
warnings.filterwarnings('ignore')

# 1. Konfigurasi Halaman (Wide Layout)
st.set_page_config(page_title="Smart Tourism Dashboard", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# 2. Styling CSS untuk menghilangkan ruang kosong (margin/padding) Streamlit
st.markdown("""
    <style>
    /* Menghilangkan padding default Streamlit agar full screen */
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
# Jika filter diubah, angka akan dikalikan dengan faktor tertentu agar terlihat berfungsi
multiplier = 1.0
if filter_tahun == "2025": multiplier = 1.15
elif filter_tahun == "2026": multiplier = 1.35

if filter_bulan != "Semua": 
    multiplier = multiplier * 0.1 # Jika pilih 1 bulan, data drop ke rata-rata bulanan

# Menghitung data dinamis berdasarkan filter
total_pengunjung = int(4280 * multiplier)
pendapatan = round(152.7 * multiplier, 1)
kepuasan = random.randint(82, 95)
tiket_rp = round(68.2 * multiplier, 1)
pengunjung_hari_ini = int(156 * multiplier * (random.uniform(0.8, 1.2)))

# 4. Konten HTML/CSS Dashboard
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
            padding: 20px 30px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; color: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .title-area h1 {{ font-size: 20px; font-weight: 800; margin: 0; text-transform: uppercase; letter-spacing: 1px; color: #FFD700; }}
        .title-area p {{ font-size: 12px; font-weight: 600; margin: 5px 0 0 0; color: #E0E0E0; }}
        
        .stats-group {{ display: flex; gap: 15px; }}
        .stat-item {{ background: rgba(255,255,255,0.1); backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 10px; text-align: center; }}
        .stat-item span {{ display: block; font-size: 9px; font-weight: 700; color: #FFF; text-transform: uppercase; letter-spacing: 0.5px; }}
        .stat-item strong {{ font-size: 18px; font-weight: 800; color: #69F0AE; }}

        /* 3 KOLOM UTAMA */
        .main-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px; }}
        .col-card {{ background: white; border-radius: 10px; padding: 15px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 15px; }}
        
        .col-header {{ padding: 12px; border-radius: 6px; font-weight: 800; color: white; font-size: 13px; display: flex; align-items: center; gap: 10px; text-transform: uppercase; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .bg-green {{ background: linear-gradient(135deg, #2E7D32, #1B5E20); }}
        .bg-blue {{ background: linear-gradient(135deg, #1565C0, #0D47A1); }}
        .bg-purple {{ background: linear-gradient(135deg, #4A148C, #311B92); }}

        /* KARTU METRIK KECIL */
        .metric-subgrid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
        .m-card {{ background: #FAFAFA; border-radius: 8px; padding: 10px 5px; border: 1px solid #EAEAEA; text-align: center; }}
        .m-icon {{ font-size: 14px; margin: 0 auto 5px auto; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
        .m-title {{ font-size: 8px; font-weight: 800; color: #555; text-transform: uppercase; }}
        .m-value {{ font-size: 15px; font-weight: 800; color: #111; margin: 3px 0; }}
        
        /* ELEMEN DESAIN SPESIFIK */
        .section-title {{ font-size: 12px; font-weight: 800; color: #333; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; border-bottom: 2px solid #F0F0F0; padding-bottom: 6px; }}
        
        .chart-container {{ background: white; padding: 10px; border-radius: 8px; border: 1px solid #f0f0f0; margin-bottom: 10px; }}
        
        /* Flowchart */
        .flow-node {{ background: #E8F5E9; border: 1px solid #2E7D32; color: #1E3A1E; padding: 8px; border-radius: 6px; font-size: 10px; font-weight: 800; text-align: center; margin-bottom: 5px; }}
        .flow-arrow {{ text-align: center; font-size: 12px; color: #666; margin-bottom: 5px; line-height: 1; }}

        /* Map Container */
        .map-container {{ border-radius: 8px; overflow: hidden; border: 1px solid #E0E0E0; height: 180px; width: 100%; }}
        
        /* Event List */
        .event-item {{ display: flex; align-items: center; background: #FAFAFA; padding: 6px 10px; border-radius: 6px; border-left: 4px solid #1565C0; font-size: 10px; gap: 10px; margin-bottom: 6px; }}
        .event-date {{ font-weight: 800; color: #1565C0; min-width: 50px; }}
        
        /* People Icons Keterlibatan */
        .people-icons {{ display: flex; gap: 5px; color: #2E7D32; font-size: 16px; align-items: center; justify-content: center; margin-bottom: 10px; }}
        .people-icons .inactive {{ color: #E0E0E0; }}
    </style>
</head>
<body>

    <!-- BANNER ATAS -->
    <div class="top-banner">
        <div class="title-area">
            <h1><i class="fa-solid fa-leaf"></i> Dashboard Pariwisata Semenanjung Badran</h1>
            <p>Desa Badransari, Kec. Punggur, Lampung Tengah • Data Filter: {filter_bulan} {filter_tahun}</p>
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
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-users"></i></div><div class="m-title">Total Wisatawan</div><div class="m-value">{total_pengunjung}</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-person-walking"></i></div><div class="m-title">Hari Ini</div><div class="m-value">{pengunjung_hari_ini}</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-ticket"></i></div><div class="m-title">Penjualan Tiket</div><div class="m-value">{tiket_rp} Jt</div></div>
            </div>

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #2E7D32;"></i> 1. Tren Kunjungan Wisatawan</div>
                <canvas id="trendChart" height="150"></canvas>
            </div>

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-umbrella" style="color: #2E7D32;"></i> 2. Fasilitas Wisata (Unit)</div>
                <canvas id="facilityChart" height="180"></canvas>
            </div>

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-people-group" style="color: #2E7D32;"></i> 3. Jenis Wisatawan</div>
                <canvas id="jenisWisatawanChart" height="180"></canvas>
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

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-money-bill-trend-up" style="color: #1565C0;"></i> 4. Pendapatan Pariwisata (Juta Rp)</div>
                <canvas id="pendapatanChart" height="150"></canvas>
            </div>

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-wallet" style="color: #1565C0;"></i> 5. Pengeluaran Operasional</div>
                <canvas id="pengeluaranChart" height="180"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-clipboard-question" style="color: #1565C0;"></i> 6. Keluhan Wisatawan</div>
                <canvas id="keluhanChart" height="150"></canvas>
            </div>

            <div style="background: #F9F9F9; padding: 10px; border-radius: 8px; border: 1px solid #EEE;">
                <div class="section-title" style="border:none; margin-bottom:5px;"><i class="fa-solid fa-users-rays" style="color: #1565C0;"></i> Keterlibatan Masyarakat (78%)</div>
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

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-map-pin" style="color: #4A148C;"></i> 7. Asal Daerah Wisatawan</div>
                <canvas id="asalWisatawanChart" height="180"></canvas>
            </div>

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-thumbs-up" style="color: #4A148C;"></i> 8. Engagement Media Sosial</div>
                <canvas id="engagementChart" height="150"></canvas>
            </div>

            <div class="chart-container">
                <div class="section-title"><i class="fa-solid fa-fire" style="color: #4A148C;"></i> 9. Konten Terpopuler (Likes/Views)</div>
                <canvas id="kontenChart" height="150"></canvas>
            </div>

            <div>
                <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #4A148C;"></i> Lokasi Semenanjung Badran</div>
                <div class="map-container">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d127183.0560935575!2d105.197365!3d-5.0069507!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e40b7987817ebbf%3A0x4039d80b220cc30!2sPunggur%2C%20Kabupaten%20Lampung%20Tengah%2C%20Lampung!5e0!3m2!1sid!2sid!4v1700000000000!5m2!1sid!2sid" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                </div>
            </div>
        </div>
    </div>

    <!-- KONFIGURASI JAVASCRIPT CHART.JS -->
    <script>
        // Data Universal Modifier dari Python Filter
        const mod = {multiplier};

        // Konfigurasi umum untuk Legend Chart
        const legendOption = {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 10 }} }} }};

        // 1. Line Chart: Tren Kunjungan
        new Chart(document.getElementById('trendChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [{{
                    label: 'Pengunjung',
                    data: [240*mod, 280*mod, 520*mod, 610*mod, 480*mod, 510*mod],
                    borderColor: '#2E7D32', backgroundColor: 'rgba(46, 125, 50, 0.15)', borderWidth: 2, fill: true, tension: 0.4
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
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
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: legendOption }} }}
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
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: legendOption }} }}
        }});

        // 4. Bar Chart: Pendapatan Pariwisata
        new Chart(document.getElementById('pendapatanChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Tiket', 'Parkir', 'Kuliner', 'Souvenir', 'Sewa'],
                datasets: [{{
                    label: 'Pendapatan (Juta Rp)',
                    data: [45*mod, 15*mod, 60*mod, 20*mod, 35*mod],
                    backgroundColor: '#1976D2', borderRadius: 4
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});

        // 5. Doughnut Chart: Pengeluaran Operasional
        new Chart(document.getElementById('pengeluaranChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Gaji/Honor', 'Perawatan', 'Pemasaran', 'Operasional Lain'],
                datasets: [{{
                    data: [40, 25, 15, 20],
                    backgroundColor: ['#D32F2F', '#1976D2', '#388E3C', '#FBC02D']
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: legendOption }} }}
        }});

        // 6. Bar Chart: Keluhan Wisatawan
        new Chart(document.getElementById('keluhanChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Kebersihan', 'Akses Jalan', 'Fasilitas', 'Harga'],
                datasets: [{{
                    label: 'Jumlah Keluhan',
                    data: [15, 28, 10, 5],
                    backgroundColor: '#E53935', borderRadius: 4
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});

        // 7. Doughnut Chart: Asal Daerah Wisatawan
        new Chart(document.getElementById('asalWisatawanChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Lampung Tengah', 'Bandar Lampung', 'Luar Lampung', 'Lainnya'],
                datasets: [{{
                    data: [50, 25, 15, 10],
                    backgroundColor: ['#6A1B9A', '#8E24AA', '#AB47BC', '#CE93D8']
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: legendOption }} }}
        }});

        // 8. Line Chart: Engagement Media Sosial
        new Chart(document.getElementById('engagementChart').getContext('2d'), {{
            type: 'line',
            data: {{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [{{
                    label: 'Interaksi',
                    data: [1200*mod, 1500*mod, 1400*mod, 2100*mod, 1800*mod, 2500*mod],
                    borderColor: '#E1306C', backgroundColor: 'rgba(225, 48, 108, 0.1)', borderWidth: 2, fill: true, tension: 0.3
                }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});

        // 9. Horizontal Bar Chart: Konten Terpopuler
        new Chart(document.getElementById('kontenChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: ['Video Drone', 'Review Makanan', 'Event Budaya', 'Spot Foto'],
                datasets: [{{
                    label: 'Engagement',
                    data: [8500, 6200, 4800, 3100],
                    backgroundColor: ['#E1306C', '#1DA1F2', '#4267B2', '#FF0000'],
                    borderRadius: 4
                }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }} }} }}
        }});
    </script>
</body>
</html>
"""

# Render HTML ke Streamlit (Height disesuaikan jadi 1600 agar semua chart muat dan tidak terpotong)
st.components.v1.html(dashboard_html, height=1700, scrolling=True)