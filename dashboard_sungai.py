from datetime import datetime

import streamlit as st


# ─── Klasifikasi ───────────────────────────────────────────────
def klasifikasi_suhu(suhu):
    if 20 <= suhu <= 30:
        return "Normal", "kualitas-baik"
    if suhu < 20:
        return "Terlalu Dingin", "kualitas-sedang"
    return "Terlalu Panas", "kualitas-buruk"


def klasifikasi_tds(tds):
    if tds < 500:
        return "Bersih", "kualitas-baik"
    if tds <= 1000:
        return "Perlu Filter", "kualitas-sedang"
    return "Tercemar", "kualitas-buruk"


# ─── Rekomendasi ───────────────────────────────────────────────
def buat_rekomendasi(stat_suhu, stat_tds):
    rekomendasi = []

    if stat_suhu == "Terlalu Panas":
        rekomendasi.append("🌡️ Suhu air terlalu tinggi. Periksa sumber panas di sekitar aliran sungai dan pantau lebih sering.")
    elif stat_suhu == "Terlalu Dingin":
        rekomendasi.append("❄️ Suhu air terlalu rendah. Waspadai dampak terhadap ekosistem air.")
    else:
        rekomendasi.append("✅ Suhu air dalam batas normal. Tidak diperlukan tindakan khusus.")

    if stat_tds == "Tercemar":
        rekomendasi.append("🚫 TDS sangat tinggi — air tercemar. Hentikan penggunaan air dan laporkan ke dinas terkait.")
    elif stat_tds == "Perlu Filter":
        rekomendasi.append("⚠️ TDS melebihi batas aman. Gunakan filter air sebelum digunakan untuk konsumsi.")
    else:
        rekomendasi.append("✅ TDS dalam batas aman. Air layak digunakan dengan pengolahan standar.")

    return rekomendasi


# ─── Konfigurasi Halaman ───────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Kualitas Air Sungai",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .main-title {
            font-size: 2.2rem; font-weight: 700;
            color: #1a6fa8; text-align: center; margin-bottom: 4px;
        }
        .sub-title {
            font-size: 1rem; color: #888;
            text-align: center; margin-bottom: 24px;
        }

        /* Status card */
        .kualitas-baik   { background:#e8f8f5; color:#1e8449; border-radius:12px; padding:18px 20px; border-left:5px solid #1e8449; }
        .kualitas-sedang { background:#fef9e7; color:#b7950b; border-radius:12px; padding:18px 20px; border-left:5px solid #d4ac0d; }
        .kualitas-buruk  { background:#fde8e8; color:#c0392b; border-radius:12px; padding:18px 20px; border-left:5px solid #c0392b; }

        /* Rekomendasi box */
        .rekomendasi-box {
            background: #f4f8ff;
            border: 1px solid #cce0ff;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 10px;
            font-size: 0.97rem;
            line-height: 1.7;
        }
        .rekomendasi-judul {
            font-weight: 700; font-size: 1.05rem;
            color: #1a6fa8; margin-bottom: 8px;
        }
        .badge-baik   { display:inline-block; background:#1e8449; color:#fff; border-radius:20px; padding:2px 14px; font-size:0.85rem; font-weight:600; }
        .badge-sedang { display:inline-block; background:#d4ac0d; color:#fff; border-radius:20px; padding:2px 14px; font-size:0.85rem; font-weight:600; }
        .badge-buruk  { display:inline-block; background:#c0392b; color:#fff; border-radius:20px; padding:2px 14px; font-size:0.85rem; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/river.png", width=80)
    st.markdown("## 💧 Input Sensor")
    st.markdown("---")
    suhu_sensor = st.slider(
        "🌡️ Suhu Air (°C)", min_value=10.0, max_value=45.0, value=26.0, step=0.1
    )
    tds_sensor = st.number_input(
        "🧪 Nilai TDS (ppm)", min_value=0, max_value=5000, value=200, step=10
    )
    st.markdown("---")
    st.caption(f"⏱️ Update: {datetime.now().strftime('%H:%M:%S')}")

# ─── Logika Status ─────────────────────────────────────────────
stat_suhu, css_suhu = klasifikasi_suhu(suhu_sensor)
stat_tds, css_tds = klasifikasi_tds(tds_sensor)

if stat_suhu == "Normal" and stat_tds == "Bersih":
    status_keseluruhan = "BAIK"
    css_keseluruhan = "kualitas-baik"
    badge_keseluruhan = "badge-baik"
    deskripsi_keseluruhan = "Air aman dan berada dalam batas normal."
elif stat_suhu == "Terlalu Panas" or stat_suhu == "Terlalu Dingin" or stat_tds == "Tercemar":
    status_keseluruhan = "BURUK"
    css_keseluruhan = "kualitas-buruk"
    badge_keseluruhan = "badge-buruk"
    deskripsi_keseluruhan = "Air tidak aman / tercemar. Diperlukan tindakan segera."
else:
    status_keseluruhan = "SEDANG"
    css_keseluruhan = "kualitas-sedang"
    badge_keseluruhan = "badge-sedang"
    deskripsi_keseluruhan = "Air cukup baik namun memerlukan pemantauan atau filtrasi."

rekomendasi_list = buat_rekomendasi(stat_suhu, stat_tds)

# ─── Header ────────────────────────────────────────────────────
st.markdown(
    '<p class="main-title">💧 Dashboard Monitoring Kualitas Air Sungai</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">Sistem IoT — Pemantauan Suhu & TDS secara Real-time</p>',
    unsafe_allow_html=True,
)

# ─── Metrik Ringkasan ──────────────────────────────────────────
st.markdown("### 📊 Ringkasan Sensor")
m1, m2, m3 = st.columns(3)
m1.metric("🌡️ Suhu Air", f"{suhu_sensor:.1f} °C", stat_suhu)
m2.metric("🧪 TDS", f"{tds_sensor} ppm", stat_tds)
m3.metric("🏞️ Status Kualitas Air", status_keseluruhan, deskripsi_keseluruhan)

st.markdown("---")

# ─── Kartu Status Detail ───────────────────────────────────────
st.markdown("### 🔍 Detail Status Kualitas Air")
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(
        f"""
        <div class="{css_suhu}">
            <b>🌡️ Suhu Air</b><br>
            Nilai: <b>{suhu_sensor:.1f} °C</b><br>
            Status: <b>{stat_suhu}</b><br>
            <small>Standar: 20°C – 30°C</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="{css_tds}">
            <b>🧪 TDS (Total Dissolved Solids)</b><br>
            Nilai: <b>{tds_sensor} ppm</b><br>
            Status: <b>{stat_tds}</b><br>
            <small>Standar: &lt; 500 ppm (Air Bersih)</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class="{css_keseluruhan}">
            <b>🏞️ Indeks Kualitas Air</b><br>
            Kondisi: <b>{status_keseluruhan}</b><br>
            <small>{deskripsi_keseluruhan}</small><br>
            <small>Update: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ─── Rekomendasi ───────────────────────────────────────────────
st.markdown("### 💡 Rekomendasi Tindakan")

badge_html = f'<span class="{badge_keseluruhan}">{status_keseluruhan}</span>'
rek_items = "".join(f"<li>{r}</li>" for r in rekomendasi_list)

st.markdown(
    f"""
    <div class="rekomendasi-box">
        <div class="rekomendasi-judul">Status Saat Ini: {badge_html}</div>
        <ul style="margin:0; padding-left:18px;">
            {rek_items}
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.caption("💧 Dashboard IoT Monitoring Kualitas Air Sungai | Python & Streamlit")
