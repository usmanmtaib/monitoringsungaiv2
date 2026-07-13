from datetime import datetime

import streamlit as st


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


def klasifikasi_ec(ec):
    if ec < 750:
        return "Baik", "kualitas-baik"
    if ec <= 1500:
        return "Sedang", "kualitas-sedang"
    return "Buruk", "kualitas-buruk"


st.set_page_config(page_title="Monitoring Air", page_icon=":droplet:", layout="wide")

st.title("Monitoring Air")
st.caption(
    "Versi Streamlit dari dashboard sederhana untuk pemantauan kualitas air."
)

with st.sidebar:
    st.header("Input")
    suhu = st.number_input(
        "Suhu Air (C)", min_value=10.0, max_value=45.0, value=26.0, step=0.1
    )
    tds = st.number_input("TDS (ppm)", min_value=0, max_value=5000, value=200)
    ec = st.number_input(
        "Elektro Konduktivitas (µS/cm)", min_value=0, max_value=10000, value=400
    )
    st.caption(f"Update: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")


stat_suhu, css_suhu = klasifikasi_suhu(suhu)
stat_tds, css_tds = klasifikasi_tds(tds)
stat_ec, css_ec = klasifikasi_ec(ec)

col1, col2, col3 = st.columns(3)
col1.metric("Suhu Air", f"{suhu:.1f} °C", f"Status: {stat_suhu}")
col2.metric("Total Dissolved Solids (TDS)", f"{tds} ppm", f"Status: {stat_tds}")
col3.metric("Elektro Konduktivitas", f"{ec} µS/cm", f"Status: {stat_ec}")

st.markdown("---")
left, right = st.columns(2)

with left:
    st.subheader("Ringkasan Status")
    st.markdown(f"- Suhu: `{suhu:.1f} °C` ({stat_suhu})")
    st.markdown(f"- TDS: `{tds} ppm` ({stat_tds})")
    st.markdown(f"- Elektro Konduktivitas: `{ec} µS/cm` ({stat_ec})")

with right:
    st.subheader("Keterangan Kualitas Air")
    st.success(f"Status Suhu: {stat_suhu} (Kode: {css_suhu})")
    st.warning(f"Status TDS: {stat_tds} (Kode: {css_tds})")
    st.info(f"Status Elektro Konduktivitas: {stat_ec} (Kode: {css_ec})")
