# Leckers Turi Project — Pizza Lecker Thury

Aplikasi web pemesanan untuk Pizza Lecker Thury (Flask + MySQL), dilengkapi dashboard admin dan autentikasi dua faktor (2FA).

## Fitur

- Katalog menu, pemesanan, dan checkout dengan QRIS.
- Registrasi, login, dan verifikasi dua faktor (`twofactor.py`).
- Profil pengguna dan riwayat pesanan.
- Dashboard admin: CRUD menu, kelola pesanan, statistik, dan kelola pengguna.
- API JSON internal (`/api/*`) untuk sisi klien.

## Struktur

- `app.py` — seluruh route web dan API.
- `templates/` — template Jinja.
- `static/` — CSS per komponen, JavaScript, dan gambar QRIS.
- `data_dummy.json` — data contoh.
- `requirements.txt` — dependensi Python (Flask).

## Menjalankan

```bash
pip install -r requirements.txt
pip install mysql-connector-python qrcode pillow
python app.py          # http://127.0.0.1:5000
```

Konfigurasi MySQL ada di `app.py` (database `db_pizza_thury`), atau lewat environment variable `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

## Deploy ke Vercel

Aplikasi ini tidak perlu dijalankan dengan `python app.py` di Vercel — sudah disiapkan sebagai serverless:

- `api/index.py` — entry point serverless (Vercel mengimpor `app` dari sini).
- `vercel.json` — routing semua request (termasuk `/static/*`) ke aplikasi Flask.

Cara deploy:

1. Push repo ini ke GitHub (sudah).
2. Di [vercel.com](https://vercel.com) → **Add New → Project** → pilih repo ini → Deploy (framework preset: **Other**, tidak perlu diubah).
3. Set **Environment Variables** di Project Settings:
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` → koneksi MySQL remote (contoh: hosting/cleardb/railway/freesqldatabase). MySQL localhost TIDAK bisa diakses dari Vercel.
4. Redeploy setelah env var diisi.

Jalankan lokal tetap seperti biasa: `python app.py`.

## Catatan

Folder `.venv/` dan `__pycache__/` tidak lagi dilacak git. Jalankan `pip install` untuk membuat lingkungan lokal sendiri.