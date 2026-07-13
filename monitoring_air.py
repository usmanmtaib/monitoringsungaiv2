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
    # Rentang EC perikanan air tawar yang digunakan aplikasi: 100–1.500 S/m.
    if ec < 100:
        return "Terlalu Rendah", "kualitas-sedang"
    if ec <= 1500:
        return "Sesuai", "kualitas-baik"
    return "Terlalu Tinggi", "kualitas-buruk"


def klasifikasi_kualitas_air(*kode_status):
    """Gabungkan status sensor dengan mengambil tingkat risiko tertinggi."""
    if "kualitas-buruk" in kode_status:
        return "Buruk", "error"
    if "kualitas-sedang" in kode_status:
        return "Perlu Perhatian", "warning"
    return "Baik", "success"


def tampilkan_status_sensor(label, status, kode_status):
    """Tampilkan warna pesan Streamlit sesuai tingkat kualitas sensor."""
    pesan = f"Status {label}: {status}"
    if kode_status == "kualitas-buruk":
        st.error(pesan)
    elif kode_status == "kualitas-sedang":
        st.warning(pesan)
    else:
        st.success(pesan)


st.set_page_config(page_title="Monitoring Air", page_icon=":droplet:", layout="wide")

st.title("Monitoring Air")
st.caption(
    "Versi Streamlit dari dashboard sederhana untuk pemantauan kualitas air."
)

with st.sidebar:
    st.header("Input")
    suhu = st.number_input(
        "Suhu Air (°C)", min_value=10.0, max_value=45.0, value=26.0, step=0.1
    )
    tds = st.number_input("TDS (ppm)", min_value=0, max_value=5000, value=200)
    ec = st.number_input(
        "Elektro Konduktivitas (S/m)",
        min_value=0,
        max_value=5000,
        value=400,
        step=10,
    )
    st.caption("Standar EC perikanan air tawar: 100–1.500 S/m")
    st.caption(f"Update: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")


stat_suhu, css_suhu = klasifikasi_suhu(suhu)
stat_tds, css_tds = klasifikasi_tds(tds)
stat_ec, css_ec = klasifikasi_ec(ec)
status_air, tipe_pesan = klasifikasi_kualitas_air(css_suhu, css_tds, css_ec)

col1, col2, col3 = st.columns(3)
col1.metric("Suhu Air", f"{suhu:.1f} °C", f"Status: {stat_suhu}")
col2.metric("Total Dissolved Solids (TDS)", f"{tds} ppm", f"Status: {stat_tds}")
col3.metric("Elektro Konduktivitas", f"{ec} S/m", f"Status: {stat_ec}")

pesan_status = f"Status kualitas air keseluruhan: {status_air}"
getattr(st, tipe_pesan)(pesan_status)
st.caption(
    "Status keseluruhan menggabungkan suhu, TDS, dan EC dengan mengambil "
    "tingkat risiko tertinggi. Nilai sensor tetap dihitung dalam satuannya masing-masing."
)

st.markdown("---")
left, right = st.columns(2)

with left:
    st.subheader("Ringkasan Status")
    st.markdown(f"- Suhu: `{suhu:.1f} °C` ({stat_suhu})")
    st.markdown(f"- TDS: `{tds} ppm` ({stat_tds})")
    st.markdown(f"- Elektro Konduktivitas: `{ec} S/m` ({stat_ec})")

with right:
    st.subheader("Keterangan Kualitas Air")
    tampilkan_status_sensor("Suhu", stat_suhu, css_suhu)
    tampilkan_status_sensor("TDS", stat_tds, css_tds)
    tampilkan_status_sensor("Elektro Konduktivitas", stat_ec, css_ec)
