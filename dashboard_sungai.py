from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def hitung_luas_penampang(lebar, kedalaman):
    return lebar * kedalaman


def hitung_debit(luas, kecepatan):
    return luas * kecepatan


def hitung_daya(luas, kecepatan, efisiensi=0.35, rho=1000):
    return 0.5 * rho * luas * (kecepatan**3) * efisiensi


def klasifikasi_arus(kecepatan):
    if kecepatan < 0.5:
        return "RENDAH", "status-rendah", "Tidak potensial untuk pembangkit listrik"
    if kecepatan <= 1.5:
        return "SEDANG", "status-sedang", "Cukup potensial (Pico-Hydro)"
    return "TINGGI", "status-tinggi", "Sangat potensial (Micro-Hydro)"


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


def buat_grafik_daya(v_saat_ini):
    v_range = np.linspace(0, 3, 100)
    luas_referensi = 1.0
    daya_range = [hitung_daya(luas_referensi, v) for v in v_range]

    fig = go.Figure()
    fig.add_vrect(x0=0, x1=0.5, fillcolor="#fde8e8", opacity=0.3, line_width=0)
    fig.add_vrect(x0=0.5, x1=1.5, fillcolor="#fef9e7", opacity=0.3, line_width=0)
    fig.add_vrect(x0=1.5, x1=3.0, fillcolor="#e8f8f5", opacity=0.3, line_width=0)
    fig.add_trace(
        go.Scatter(
            x=v_range,
            y=daya_range,
            mode="lines",
            line=dict(color="#1a6fa8", width=3),
            name="Potensi Daya (W)",
        )
    )
    daya_saat_ini = hitung_daya(luas_referensi, v_saat_ini)
    fig.add_trace(
        go.Scatter(
            x=[v_saat_ini],
            y=[daya_saat_ini],
            mode="markers",
            marker=dict(size=14, color="red", symbol="circle"),
            name=f"Sensor: {v_saat_ini} m/s",
        )
    )
    fig.update_layout(
        title="Grafik Potensi Daya vs Kecepatan Arus",
        xaxis_title="Kecepatan Arus (m/s)",
        yaxis_title="Potensi Daya (Watt)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=380,
    )
    fig.update_xaxes(showgrid=True, gridcolor="#ececec")
    fig.update_yaxes(showgrid=True, gridcolor="#ececec")
    return fig


def buat_grafik_simulasi(jumlah_data=30):
    waktu = pd.date_range(end=datetime.now(), periods=jumlah_data, freq="1min")
    return pd.DataFrame(
        {
            "Waktu": waktu,
            "Arus": np.random.uniform(0.3, 2.5, jumlah_data).round(2),
            "Suhu": np.random.uniform(22, 32, jumlah_data).round(1),
            "TDS": np.random.randint(100, 900, jumlah_data).astype(float),
        }
    )


def buat_gauge(nilai, judul, satuan, min_val, max_val, batas_rendah, batas_tinggi):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=nilai,
            title={"text": f"{judul} ({satuan})", "font": {"size": 14}},
            gauge={
                "axis": {"range": [min_val, max_val]},
                "bar": {"color": "#1a6fa8"},
                "steps": [
                    {"range": [min_val, batas_rendah], "color": "#fde8e8"},
                    {"range": [batas_rendah, batas_tinggi], "color": "#fef9e7"},
                    {"range": [batas_tinggi, max_val], "color": "#e8f8f5"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": nilai,
                },
            },
        )
    )
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig


st.set_page_config(
    page_title="Dashboard Monitoring Sungai IoT",
    page_icon=":droplet:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .main-title { font-size: 2rem; font-weight: bold; color: #1a6fa8; text-align: center; }
        .sub-title { font-size: 1rem; color: #888; text-align: center; margin-bottom: 20px; }
        .status-box { padding: 15px; border-radius: 10px; text-align: center; font-size: 1.1rem; font-weight: bold; }
        .status-rendah  { background-color: #fde8e8; color: #c0392b; }
        .status-sedang  { background-color: #fef9e7; color: #d4ac0d; }
        .status-tinggi  { background-color: #e8f8f5; color: #1e8449; }
        .kualitas-baik  { background-color: #e8f8f5; color: #1e8449; border-radius:8px; padding:10px; }
        .kualitas-sedang{ background-color: #fef9e7; color: #d4ac0d; border-radius:8px; padding:10px; }
        .kualitas-buruk { background-color: #fde8e8; color: #c0392b; border-radius:8px; padding:10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/river.png", width=80)
    st.markdown("## Input Sensor IoT")
    st.markdown("---")
    st.markdown("### Dimensi Sungai")
    lebar = st.number_input(
        "Lebar Sungai (m)", min_value=0.1, max_value=100.0, value=2.0, step=0.1
    )
    kedalaman = st.number_input(
        "Kedalaman Air (m)", min_value=0.1, max_value=50.0, value=1.0, step=0.1
    )
    st.markdown("### Data Sensor Aliran")
    v_sensor = st.slider(
        "Kecepatan Arus (m/s)", min_value=0.0, max_value=3.0, value=1.2, step=0.01
    )
    st.markdown("### Kualitas Air")
    suhu_sensor = st.slider(
        "Suhu Air (C)", min_value=10.0, max_value=45.0, value=26.0, step=0.1
    )
    tds_sensor = st.number_input(
        "Nilai TDS (ppm)", min_value=0, max_value=5000, value=200
    )
    st.markdown("---")
    st.caption(f"Update: {datetime.now().strftime('%H:%M:%S')}")


luas = hitung_luas_penampang(lebar, kedalaman)
debit = hitung_debit(luas, v_sensor)
daya = hitung_daya(luas, v_sensor)
kat_arus, css_arus, saran_arus = klasifikasi_arus(v_sensor)
stat_suhu, css_suhu = klasifikasi_suhu(suhu_sensor)
stat_tds, css_tds = klasifikasi_tds(tds_sensor)
lampu = int(daya / 10)

st.markdown(
    '<p class="main-title">Dashboard Monitoring Potensi Energi Sungai</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">Sistem IoT Pemantauan Kecepatan Arus, Daya Listrik, dan Kualitas Air</p>',
    unsafe_allow_html=True,
)

st.markdown("### Ringkasan Data Sensor")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Luas Penampang", f"{luas:.2f} m2", f"L:{lebar}m x D:{kedalaman}m")
m2.metric("Debit Air", f"{debit:.3f} m3/s", "A x v")
m3.metric("Potensi Daya", f"{daya:.1f} W", "Efisiensi 35%")
m4.metric("Kecepatan Arus", f"{v_sensor:.2f} m/s", kat_arus)
m5.metric("Estimasi Lampu LED", f"{lampu} unit", "@10W per lampu")

st.markdown("---")
col_kiri, col_kanan = st.columns([1, 2])

with col_kiri:
    st.markdown("### Status Klasifikasi Arus")
    st.markdown(
        f"""
        <div class="status-box {css_arus}">
            KATEGORI ARUS: {kat_arus}<br>
            <small>{saran_arus}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Tabel Standar Kecepatan")
    df_standar = pd.DataFrame(
        {
            "Kategori": ["Rendah", "Sedang", "Tinggi"],
            "Kecepatan": ["< 0.5 m/s", "0.5 - 1.5 m/s", "> 1.5 m/s"],
            "Potensi": ["Tidak Potensial", "Pico-Hydro", "Micro-Hydro"],
        }
    )
    st.dataframe(df_standar, hide_index=True, use_container_width=True)

with col_kanan:
    st.markdown("### Kurva Potensi Daya vs Kecepatan Arus")
    st.plotly_chart(buat_grafik_daya(v_sensor), use_container_width=True)

st.markdown("---")
st.markdown("### Gauge Sensor Real-time")
g1, g2, g3 = st.columns(3)
with g1:
    st.plotly_chart(
        buat_gauge(v_sensor, "Kecepatan Arus", "m/s", 0, 3, 0.5, 1.5),
        use_container_width=True,
    )
with g2:
    st.plotly_chart(
        buat_gauge(suhu_sensor, "Suhu Air", "C", 10, 45, 20, 30),
        use_container_width=True,
    )
with g3:
    st.plotly_chart(
        buat_gauge(tds_sensor, "TDS", "ppm", 0, 2000, 500, 1000),
        use_container_width=True,
    )

st.markdown("---")
st.markdown("### Status Kualitas Air")
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(
        f"""
        <div class="{css_suhu}">
            <b>Suhu Air</b><br>
            Nilai: <b>{suhu_sensor} C</b><br>
            Status: <b>{stat_suhu}</b><br>
            Standar: 20C - 30C
        </div>
        """,
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f"""
        <div class="{css_tds}">
            <b>TDS (Total Dissolved Solids)</b><br>
            Nilai: <b>{tds_sensor} ppm</b><br>
            Status: <b>{stat_tds}</b><br>
            Standar: < 500 ppm (Air Bersih)
        </div>
        """,
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f"""
        <div class="kualitas-baik" style="background:#eaf3fb; color:#1a6fa8;">
            <b>Estimasi Daya Listrik</b><br>
            Total Daya: <b>{daya:.2f} W</b><br>
            Lampu LED 10W: <b>{lampu} unit</b><br>
            Debit: <b>{debit:.3f} m3/s</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("### Grafik Historis Sensor (Simulasi 30 Menit Terakhir)")
df_hist = buat_grafik_simulasi(30)

tab1, tab2, tab3 = st.tabs(["Kecepatan Arus", "Suhu Air", "TDS"])
with tab1:
    fig_arus = px.line(
        df_hist,
        x="Waktu",
        y="Arus",
        title="Kecepatan Arus (m/s) - 30 Menit Terakhir",
        color_discrete_sequence=["#1a6fa8"],
    )
    fig_arus.add_hline(
        y=0.5, line_dash="dash", line_color="#f39c12", annotation_text="Batas Rendah"
    )
    fig_arus.add_hline(
        y=1.5, line_dash="dash", line_color="#1e8449", annotation_text="Batas Tinggi"
    )
    fig_arus.update_layout(plot_bgcolor="white", height=350)
    st.plotly_chart(fig_arus, use_container_width=True)
with tab2:
    fig_suhu = px.line(
        df_hist,
        x="Waktu",
        y="Suhu",
        title="Suhu Air (C) - 30 Menit Terakhir",
        color_discrete_sequence=["#e74c3c"],
    )
    fig_suhu.add_hline(
        y=20, line_dash="dash", line_color="#f39c12", annotation_text="Batas Bawah"
    )
    fig_suhu.add_hline(
        y=30, line_dash="dash", line_color="#c0392b", annotation_text="Batas Atas"
    )
    fig_suhu.update_layout(plot_bgcolor="white", height=350)
    st.plotly_chart(fig_suhu, use_container_width=True)
with tab3:
    fig_tds = px.bar(
        df_hist,
        x="Waktu",
        y="TDS",
        title="Nilai TDS (ppm) - 30 Menit Terakhir",
        color_discrete_sequence=["#8e44ad"],
    )
    fig_tds.add_hline(
        y=500, line_dash="dash", line_color="#f39c12", annotation_text="Batas Baik"
    )
    fig_tds.add_hline(
        y=1000, line_dash="dash", line_color="#c0392b", annotation_text="Batas Buruk"
    )
    fig_tds.update_layout(plot_bgcolor="white", height=350)
    st.plotly_chart(fig_tds, use_container_width=True)

st.markdown("---")
st.caption("Dashboard IoT Monitoring Sungai | Dibuat dengan Python dan Streamlit")
