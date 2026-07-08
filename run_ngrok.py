"""
Jalankan file ini untuk membuat link publik dashboard.
Pastikan Streamlit sudah berjalan terlebih dahulu di terminal lain:
    streamlit run dashboard_sungai.py

Kemudian jalankan file ini di terminal terpisah:
    python run_ngrok.py
"""

from pyngrok import ngrok

# Ganti dengan auth token kamu dari https://dashboard.ngrok.com/get-started/your-authtoken
# Daftar gratis di ngrok.com untuk mendapatkan token
NGROK_AUTH_TOKEN = "ISI_TOKEN_KAMU_DI_SINI"

ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Buat tunnel ke port Streamlit (default: 8501)
public_url = ngrok.connect(8501)

print("=" * 50)
print("  Dashboard kamu bisa diakses di:")
print(f"  {public_url}")
print("=" * 50)
print("  Tekan Ctrl+C untuk menghentikan sharing.")
print("=" * 50)

try:
    input()
except KeyboardInterrupt:
    print("\nSharing dihentikan.")
    ngrok.kill()
