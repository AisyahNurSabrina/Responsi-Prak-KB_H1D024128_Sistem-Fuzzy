# Sistem Fuzzy Penilaian Kesehatan Tanaman Indoor

Project ini adalah versi Python/Flask dari Sistem Fuzzy. File `script.js` sudah dihapus dan logika sistem dipindahkan ke `fuzzy/fuzzy_system.py`.

## Struktur

```text
plant-fuzzy-system/
├── app.py
├── requirements.txt
├── vercel.json
├── templates/
│   └── index.html
├── public/
│   └── style.css
└── fuzzy/
    ├── __init__.py
    └── fuzzy_system.py
```

## Menjalankan Lokal

```bash
pip install -r requirements.txt
python app.py
```

Buka:

```text
http://127.0.0.1:5000/
```
