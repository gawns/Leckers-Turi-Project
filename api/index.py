# Vercel serverless entry point.
# Vercel TIDAK menjalankan `python app.py` — dia mengimpor variable `app`
# dari file ini untuk setiap request (serverless function).
import sys
import os

# Pastikan folder root proyek ada di sys.path supaya `app.py` dan `twofactor.py`
# (yang berada satu level di atas folder api/) bisa diimpor.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app  # noqa: E402  (Aplikasi Flask utama)

# Vercel (Runtime Python / WSGI) mencari variable `app` di module ini.
app.config['SERVER_NAME'] = None
