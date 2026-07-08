from datetime import datetime

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


st.set_page_config(page_title="Monitoring Air", page_icon=":droplet:", layout="wide")

st.title("Monitoring Air")
st.caption(
    "Versi Streamlit dari dashboard sederhana untuk perhitungan arus dan kualitas air."
)

with st.sidebar:
    st.header("Input")
    lebar = st.number_input("Lebar Penampang (m)", min_value=0.1, value=2.0, step=0.1)
    kedalaman = st.number_input(
        "Kedalaman Air (m)", min_value=0.1, value=1.0, step=0.1
    )
    arus = st.slider(
        "Kecepatan Arus (m/s)", min_value=0.0, max_value=3.0, value=1.2, step=0.01
    )
    suhu = st.slider(
        "Suhu Air (C)", min_value=10.0, max_value=45.0, value=26.0, step=0.1
    )
    tds = st.number_input("TDS (ppm)", min_value=0, max_value=5000, value=200)
    st.caption(f"Update: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")


luas = hitung_luas_penampang(lebar, kedalaman)
debit = hitung_debit(luas, arus)
daya = hitung_daya(luas, arus)
kat_arus, css_arus, saran_arus = klasifikasi_arus(arus)
stat_suhu, css_suhu = klasifikasi_suhu(suhu)
stat_tds, css_tds = klasifikasi_tds(tds)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Luas Penampang", f"{luas:.2f} m2")
col2.metric("Debit Air", f"{debit:.3f} m3/s")
col3.metric("Daya", f"{daya:.2f} W")
col4.metric("Kategori Arus", kat_arus)

st.markdown("---")
left, right = st.columns(2)

with left:
    st.subheader("Ringkasan")
    st.markdown(f"- Luas: `{luas:.2f} m2`")
    st.markdown(f"- Debit: `{debit:.3f} m3/s`")
    st.markdown(f"- Daya: `{daya:.2f} W`")
    st.markdown(f"- Arus: `{kat_arus}`")
    st.info(saran_arus)

with right:
    st.subheader("Kualitas Air")
    st.success(f"Suhu: {stat_suhu}")
    st.warning(f"TDS: {stat_tds}")
    st.caption(f"Kode status suhu: {css_suhu}")
    st.caption(f"Kode status TDS: {css_tds}")
