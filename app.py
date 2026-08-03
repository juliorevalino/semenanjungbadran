import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Smart Tourism Dashboard Desa Badransari", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# 2. Styling CSS untuk Sidebar & Tema Dashboard
st.markdown("""
    <style>
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
        letter-spacing: 0.5px;
    }
    .sidebar-title p {
        color: #E0E0E0 !important;
        font-size: 10px;
        margin: 4px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Filter Data dengan Judul Hibah BIMA Semenanjung Badran ITERA
st.sidebar.markdown("""
    <div class="sidebar-title">
        <h3>Hibah BIMA Semenanjung Badran ITERA</h3>
        <p>Program Pengabdian Kepada Masyarakat</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown('### <i class="fa-solid fa-filter"></i> FILTER DATA', unsafe_allow_html=True)
st.sidebar.selectbox("📅 Tahun", ["2024", "2025", "2026"])
st.sidebar.selectbox("🕒 Bulan", ["Semua", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
st.sidebar.selectbox("👥 Jenis Wisatawan", ["Semua", "Lokal", "Kabupaten", "Provinsi", "Nasional"])
st.sidebar.selectbox("📍 Asal Daerah", ["Semua", "Lampung Tengah", "Bandar Lampung", "Luar Lampung"])
st.sidebar.selectbox("⛰️ Jenis Wisata", ["Semua", "Wisata Alam", "Wisata Edukasi", "Kuliner & Outbound"])
st.sidebar.selectbox("🎉 Event", ["Semua", "Festival Desa", "Pasar UMKM", "Lomba Perahu"])
st.sidebar.selectbox("👤 Kelompok Usia", ["Semua", "Remaja (15-25)", "Dewasa (26-45)", "Senior (>45)"])

# 4. Konten Dashboard Lengkap
dashboard_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        body { background-color: #F0F4F8; margin: 0; padding: 10px; }
        
        /* Header Utama */
        .top-header { background: white; padding: 15px 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-left: 6px solid #2E7D32; }
        .title-area h1 { font-size: 17px; font-weight: 800; color: #1E3A1E; margin: 0; }
        .title-area p { font-size: 11px; color: #555; font-weight: 600; margin: 3px 0 0 0; }
        
        .stats-group { display: flex; gap: 12px; }
        .stat-item { background: #FAFAFA; border: 1px solid #E0E0E0; padding: 6px 10px; border-radius: 8px; text-align: center; }
        .stat-item span { display: block; font-size: 7px; font-weight: 700; color: #666; text-transform: uppercase; }
        .stat-item strong { font-size: 13px; font-weight: 800; color: #222; }

        /* Grid 3 Kolom Utama (UTUH TIDAK DIUBAH) */
        .main-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px; }
        .col-card { background: white; border-radius: 10px; padding: 12px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
        
        .col-header { padding: 10px; border-radius: 6px; font-weight: 800; color: white; font-size: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; }
        .bg-green { background: #2E7D32; }
        .bg-blue { background: #1565C0; }
        .bg-purple { background: #4A148C; }

        .metric-subgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .m-card { background: #FAFAFA; border-radius: 6px; padding: 8px 4px; border: 1px solid #EAEAEA; text-align: center; height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .m-icon { font-size: 11px; margin-bottom: 3px; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
        .m-title { font-size: 7px; font-weight: 800; color: #555; text-transform: uppercase; line-height: 1.1; width: 100%; }
        .m-value { font-size: 13px; font-weight: 800; color: #111; margin: 2px 0; }
        .m-sub { font-size: 7px; font-weight: 700; color: #777; }

        /* Grid Tambahan Grafik & Informasi */
        .dashboard-row { display: grid; grid-template-columns: 2fr 1fr; gap: 15px; margin-bottom: 15px; }
        .dashboard-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px; }
        .dashboard-row-equal { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }
        
        .card-box { background: white; border-radius: 10px; padding: 15px; border: 1px solid #E0E0E0; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
        .section-title { font-size: 11px; font-weight: 800; color: #333; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; border-bottom: 2px solid #F0F0F0; padding-bottom: 6px; }

        /* Struktur Pengelolaan */
        .flow-container { display: flex; flex-direction: column; gap: 8px; align-items: center; padding: 5px 0; }
        .flow-node { background: #E8F5E9; border: 1px solid #2E7D32; color: #1E3A1E; padding: 8px 15px; border-radius: 6px; font-size: 10px; font-weight: 800; width: 100%; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .flow-node.blue { background: #E3F2FD; border-color: #1565C0; color: #0D47A1; }
        .flow-node.orange { background: #FFF8E1; border-color: #F57F17; color: #E65100; }
        .flow-node.purple { background: #EDE7F6; border-color: #4A148C; color: #311B92; }
        .flow-arrow { font-size: 12px; color: #666; margin: -2px 0; }

        /* Jadwal Event */
        .event-list { display: flex; flex-direction: column; gap: 6px; }
        .event-item { display: flex; align-items: center; background: #FAFAFA; padding: 6px 10px; border-radius: 6px; border-left: 3px solid #2E7D32; font-size: 10px; gap: 10px; }
        .event-date { font-weight: 800; color: #2E7D32; min-width: 60px; }
        .event-name { font-weight: 600; color: #333; }

        /* Progress Bars */
        .progress-box { margin-top: 10px; }
        .progress-label { display: flex; justify-content: space-between; font-size: 10px; font-weight: 800; margin-bottom: 4px; color: #333; }
        .progress-bar-bg { background: #E0E0E0; border-radius: 10px; height: 10px; width: 100%; overflow: hidden; }
        .progress-bar-fill { background: #2E7D32; height: 100%; border-radius: 10px; }
    </style>
</head>
<body>

    <!-- Header Atas -->
    <div class="top-header">
        <div class="title-area">
            <h1>🌿 SMART TOURISM DASHBOARD — DESA BADRANSARI</h1>
            <p>Kecamatan Punggur, Kabupaten Lampung Tengah • Program Hibah BIMA ITERA</p>
        </div>
        <div class="stats-group">
            <div class="stat-item">
                <span>👥 Total Pengunjung</span>
                <strong style="color: #2E7D32;">4.280 Orang</strong>
            </div>
            <div class="stat-item">
                <span>💰 Pendapatan</span>
                <strong style="color: #1565C0;">Rp 152,7 Juta</strong>
            </div>
            <div class="stat-item">
                <span>⭐ Kepuasan</span>
                <strong style="color: #F57F17;">88% Sangat Baik</strong>
            </div>
        </div>
    </div>

    <!-- 3 Kolom Utama (DIJAGA UTUH TANPA PERUBAHAN) -->
    <div class="main-grid">
        <!-- KOLOM 1: LAYANAN PARIWISATA -->
        <div class="col-card">
            <div class="col-header bg-green"><i class="fa-solid fa-umbrella-beach"></i> 1. Layanan Pariwisata</div>
            <div class="metric-subgrid">
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-users"></i></div><div class="m-title">Wisatawan 2024</div><div class="m-value">4.280</div><div class="m-sub">Orang</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-person-walking"></i></div><div class="m-title">Hari Ini</div><div class="m-value">156</div><div class="m-sub">Orang</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-ticket"></i></div><div class="m-title">Pendapatan Tiket</div><div class="m-value">68,2</div><div class="m-sub">Juta Rp</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-star"></i></div><div class="m-title">Kepuasan</div><div class="m-value">88%</div><div class="m-sub">Sangat Baik</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-store"></i></div><div class="m-title">Jumlah UMKM</div><div class="m-value">42</div><div class="m-sub">Unit</div></div>
                <div class="m-card"><div class="m-icon" style="color: #2E7D32; background: #E8F5E9;"><i class="fa-solid fa-house"></i></div><div class="m-title">Homestay</div><div class="m-value">15</div><div class="m-sub">Unit</div></div>
            </div>
        </div>

        <!-- KOLOM 2: MANAJEMEN PARIWISATA -->
        <div class="col-card">
            <div class="col-header bg-blue"><i class="fa-solid fa-gear"></i> 2. Manajemen Pariwisata</div>
            <div class="metric-subgrid">
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-users-gear"></i></div><div class="m-title">Pokdarwis</div><div class="m-value">3</div><div class="m-sub">Kelompok</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-user-tie"></i></div><div class="m-title">Pengelola</div><div class="m-value">27</div><div class="m-sub">Orang</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-shop"></i></div><div class="m-title">UMKM Aktif</div><div class="m-value">42</div><div class="m-sub">Unit</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-calendar"></i></div><div class="m-title">Event Tahun Ini</div><div class="m-value">8</div><div class="m-sub">Kegiatan</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-handshake"></i></div><div class="m-title">Mitra</div><div class="m-value">12</div><div class="m-sub">Instansi</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-solid fa-hands-holding-child"></i></div><div class="m-title">Relawan</div><div class="m-value">36</div><div class="m-sub">Orang</div></div>
            </div>
        </div>

        <!-- KOLOM 3: PEMASARAN PARIWISATA -->
        <div class="col-card">
            <div class="col-header bg-purple"><i class="fa-solid fa-bullhorn"></i> 3. Pemasaran Pariwisata</div>
            <div class="metric-subgrid">
                <div class="m-card"><div class="m-icon" style="color: #E1306C; background: #FCE4EC;"><i class="fa-brands fa-instagram"></i></div><div class="m-title">IG Followers</div><div class="m-value">3.842</div><div class="m-sub">Akun</div></div>
                <div class="m-card"><div class="m-icon" style="color: #000; background: #F5F5F5;"><i class="fa-brands fa-tiktok"></i></div><div class="m-title">TikTok Followers</div><div class="m-value">2.156</div><div class="m-sub">Akun</div></div>
                <div class="m-card"><div class="m-icon" style="color: #1565C0; background: #E3F2FD;"><i class="fa-brands fa-facebook"></i></div><div class="m-title">FB Reach</div><div class="m-value">8.745</div><div class="m-sub">Jangkauan</div></div>
                <div class="m-card"><div class="m-icon" style="color: #4A148C; background: #EDE7F6;"><i class="fa-solid fa-globe"></i></div><div class="m-title">Website Visitor</div><div class="m-value">5.231</div><div class="m-sub">Kunjungan</div></div>
                <div class="m-card"><div class="m-icon" style="color: #4A148C; background: #EDE7F6;"><i class="fa-solid fa-comments"></i></div><div class="m-title">Google Review</div><div class="m-value">157</div><div class="m-sub">Ulasan</div></div>
                <div class="m-card"><div class="m-icon" style="color: #F57F17; background: #FFF8E1;"><i class="fa-solid fa-star"></i></div><div class="m-title">Rating Google</div><div class="m-value">4,6</div><div class="m-sub">Sangat Baik</div></div>
            </div>
        </div>
    </div>

    <!-- ROW 1 TAMBAHAN: Grafik Tren & Struktur Pengelolaan -->
    <div class="dashboard-row">
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-chart-line" style="color: #2E7D32;"></i> Grafik Tren Kunjungan Wisatawan (2024)</div>
            <canvas id="trendChart" height="120"></canvas>
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
                <div class="flow-arrow">↓</div>
                <div class="flow-node" style="background: #E0F2F1; border-color: #00796B; color: #004D40;">🧑‍🤝‍🧑 Wisatawan / Pengunjung</div>
            </div>
        </div>
    </div>

    <!-- ROW 2 TAMBAHAN: Fasilitas, Jenis Wisatawan, Jadwal Event -->
    <div class="dashboard-row-3">
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-umbrella" style="color: #2E7D32;"></i> Fasilitas Wisata</div>
            <canvas id="facilityChart" height="180"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-users-rectangle" style="color: #1565C0;"></i> Jenis Wisatawan</div>
            <canvas id="visitorTypeChart" height="180"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-calendar-days" style="color: #4A148C;"></i> Jadwal Event 2024</div>
            <div class="event-list">
                <div class="event-item"><span class="event-date">14 Jan</span><span class="event-name">Festival Desa Badransari</span></div>
                <div class="event-item"><span class="event-date">18 Feb</span><span class="event-name">Pasar UMKM Kreatif</span></div>
                <div class="event-item"><span class="event-date">24 Mar</span><span class="event-name">Lomba Perahu Tradisional</span></div>
                <div class="event-item"><span class="event-date">21 Apr</span><span class="event-name">Senam Minggu Sehat</span></div>
                <div class="event-item"><span class="event-date">12 Mei</span><span class="event-name">Camping & Outbound</span></div>
                <div class="event-item"><span class="event-date">20 Jul</span><span class="event-name">Festival Kuliner Desa</span></div>
                <div class="event-item"><span class="event-date">17 Agu</span><span class="event-name">Lomba Mancing Mania</span></div>
                <div class="event-item"><span class="event-date">29 Des</span><span class="event-name">Pergantian Tahun Baru</span></div>
            </div>
        </div>
    </div>

    <!-- ROW 3 TAMBAHAN: Pendapatan, Pengeluaran, Asal Wisatawan -->
    <div class="dashboard-row-3">
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-wallet" style="color: #2E7D32;"></i> Pendapatan Pariwisata (Juta Rp)</div>
            <canvas id="revenueChart" height="180"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-receipt" style="color: #D32F2F;"></i> Pengeluaran Operasional</div>
            <canvas id="expenseChart" height="180"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-map-location-dot" style="color: #1565C0;"></i> Asal Daerah Wisatawan</div>
            <canvas id="originChart" height="180"></canvas>
        </div>
    </div>

    <!-- ROW 4 TAMBAHAN: Media Sosial, Keluhan, Konten Terpopuler & Keterlibatan -->
    <div class="dashboard-row">
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-chart-area" style="color: #4A148C;"></i> Engagement Media Sosial (Like, Comment, Share)</div>
            <canvas id="socialChart" height="130"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-triangle-exclamation" style="color: #C62828;"></i> Keluhan Wisatawan</div>
            <canvas id="complaintChart" height="130"></canvas>
        </div>
    </div>

    <div class="dashboard-row-equal">
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-fire" style="color: #E65100;"></i> Konten Terpopuler</div>
            <canvas id="contentChart" height="130"></canvas>
        </div>
        <div class="card-box">
            <div class="section-title"><i class="fa-solid fa-circle-check" style="color: #2E7D32;"></i> Indikator Kinerja Program Hibah BIMA</div>
            <div style="padding: 10px 0;">
                <div class="progress-box">
                    <div class="progress-label"><span>Tingkat Keterlibatan Masyarakat (Community Engagement)</span><span>78%</span></div>
                    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 78%;"></div></div>
                </div>
                <div class="progress-box" style="margin-top: 15px;">
                    <div class="progress-label"><span>Tingkat Kepuasan Promosi & Digital Marketing</span><span>85% Sangat Baik</span></div>
                    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 85%; background: #1565C0;"></div></div>
                </div>
                <div class="progress-box" style="margin-top: 15px;">
                    <div class="progress-label"><span>Peningkatan Pendapatan UMKM Lokal YoY</span><span>64%</span></div>
                    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 64%; background: #F57F17;"></div></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 1. Trend Chart
        new Chart(document.getElementById('trendChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'],
                datasets: [{
                    label: 'Pengunjung',
                    data: [240, 280, 310, 520, 610, 720, 480, 510, 420, 400, 440, 680],
                    borderColor: '#2E7D32',
                    backgroundColor: 'rgba(46, 125, 50, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
        });

        // 2. Facility Chart (Doughnut)
        new Chart(document.getElementById('facilityChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Parkir (18%)', 'Toilet (15%)', 'Mushola (12%)', 'Gazebo (17%)', 'Spot Foto (20%)', 'Warung (10%)', 'Camping (8%)'],
                datasets: [{
                    data: [18, 15, 12, 17, 20, 10, 8],
                    backgroundColor: ['#2E7D32', '#1565C0', '#F57F17', '#4A148C', '#00796B', '#D32F2F', '#795548']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 9 } } } } }
        });

        // 3. Visitor Type Chart (Pie)
        new Chart(document.getElementById('visitorTypeChart').getContext('2d'), {
            type: 'pie',
            data: {
                labels: ['Lokal (52%)', 'Kabupaten (23%)', 'Provinsi (15%)', 'Nasional (10%)'],
                datasets: [{
                    data: [52, 23, 15, 10],
                    backgroundColor: ['#2E7D32', '#1565C0', '#F57F17', '#4A148C']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 9 } } } } }
        });

        // 4. Revenue Bar Chart
        new Chart(document.getElementById('revenueChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Tiket', 'Parkir', 'Sewa Gazebo', 'Camping', 'UMKM'],
                datasets: [{
                    label: 'Juta Rp',
                    data: [68.2, 22.1, 16.7, 15.6, 28.1],
                    backgroundColor: '#2E7D32'
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
        });

        // 5. Expense Chart (Doughnut)
        new Chart(document.getElementById('expenseChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Kebersihan (30%)', 'Perawatan (25%)', 'Promosi (15%)', 'SDM (15%)', 'Infrastruktur (15%)'],
                datasets: [{
                    data: [30, 25, 15, 15, 15],
                    backgroundColor: ['#D32F2F', '#F57F17', '#1565C0', '#4A148C', '#2E7D32']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 9 } } } } }
        });

        // 6. Origin Chart (Doughnut)
        new Chart(document.getElementById('originChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Lampung Tengah (55%)', 'Sumatera Sel. (17%)', 'DKI Jakarta (10%)', 'Banten (7%)', 'Jawa Barat (6%)', 'Lainnya (5%)'],
                datasets: [{
                    data: [55, 17, 10, 7, 6, 5],
                    backgroundColor: ['#2E7D32', '#1565C0', '#F57F17', '#4A148C', '#00796B', '#D32F2F']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 8 } } } } }
        });

        // 7. Social Line Chart
        new Chart(document.getElementById('socialChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                datasets: [
                    { label: 'Likes', data: [1200, 1900, 2400, 3100, 4200, 5100], borderColor: '#E1306C', backgroundColor: 'transparent', borderWidth: 2 },
                    { label: 'Comments', data: [300, 450, 600, 850, 1100, 1400], borderColor: '#1565C0', backgroundColor: 'transparent', borderWidth: 2 },
                    { label: 'Shares', data: [150, 220, 340, 480, 650, 890], borderColor: '#2E7D32', backgroundColor: 'transparent', borderWidth: 2 }
                ]
            },
            options: { responsive: true, plugins: { legend: { position: 'top', labels: { boxWidth: 10, font: { size: 9 } } } }, scales: { y: { beginAtZero: true } } }
        });

        // 8. Complaint Bar Chart
        new Chart(document.getElementById('complaintChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Kebersihan', 'Jalan', 'Toilet', 'Parkir', 'Informasi', 'Harga'],
                datasets: [{
                    label: 'Persentase (%)',
                    data: [28, 22, 20, 15, 9, 6],
                    backgroundColor: '#D32F2F'
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 35 } } }
        });

        // 9. Content Horizontal Bar Chart
        new Chart(document.getElementById('contentChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Spot Foto & Panorama', 'Sunset & Pemandangan', 'Festival & Event', 'Camping & Outbound', 'Kuliner Khas'],
                datasets: [{
                    label: 'Popularitas (%)',
                    data: [35, 25, 20, 10, 10],
                    backgroundColor: '#F57F17'
                }]
            },
            options: { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, max: 40 } } }
        });
    </script>
</body>
</html>
"""

import streamlit.components.v1 as components
components.html(dashboard_html, height=1850, scrolling=True)