# 📊 Analisis Pola Kejadian Gangguan Kompresor Kereta Metro dan Rekomendasi Strategis Menggunakan Granite 3.2 8B
**Hacktiv8 x IBM SkillsBuild — Agustus 2025**  
Muhammad Fauzan Azhima  

---

## 📝 Project overview  
Proyek ini bertujuan menganalisis pola kejadian gangguan pada unit produksi udara (Air Production Unit/APU) kompresor kereta metro menggunakan dataset **MetroPT-3** agar bisa didapat saran atau rekomendasi strategis yang bisa dilakukan untuk mengatasi gangguan tersebut.  
Karena ukuran asli dataset yang terlalu besar (dataset asli direkeam dengan frekuensi 1 Hz atau setiap detik dari bulan februari 2020 - agustus 2020) dan keterbatasan perangkat, rekaman aslinya dirata-ratakan menjadi interval 60 menit dan periode analisis dibatasi (contoh: 10 Februari – 20 Maret).  

Setiap sampel per jam dilabeli menjadi salah satu kategori:  
- ✅ **Normal**  
- 🟠 **AirLeak**  
- 🔴 **HighStress**  
- 🟣 **AirLeak-HighStress**  

Untuk efisiensi token dan memori model, pelabelan dilakukan dalam batch. Hasil pelabelan digabungkan, lalu **Python** menghitung tren jam & hari rawan 📈. Ringkasan tren tersebut dikirim ke **Granite 3.2 8B** (lokal via LM Studio) agar Granite dapat fokus memberikan rekomendasi strategis  bagi perusahaan.  

---

## 🔗 Raw dataset  
MetroPT-3 (AirCompressor) — multivariate time series dari 15 sensor APU kompresor kereta metro.  
📥 [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/791/metropt%2B3%2Bdataset?utm_source=chatgpt.com)  

---

## 📌 Insight & findings (ringkasan)  
- 📉 **Tingkat anomali:** Subset data menunjukkan proporsi anomali signifikan (~18% pada periode contoh).  
- ⏰ **Jam puncak anomali:** Dini hari (01:00–04:00) dan pagi hari (sekitar 07:00) punya frekuensi gangguan tinggi.  
- 📅 **Tanggal puncak:** Konsentrasi masalah terlihat di pertengahan Maret 2020 pada subset analisis.  
- 💡 **Rekomendasi awal:**  
  - Penjadwalan inspeksi di jam rawan.  
  - Preventive maintenance rutin.  
  - Pengaturan beban operasi di jam berisiko.  
  - Implementasi sistem peringatan dini & optimasi sensor.

---

## 🤖 AI support explanation  
Seluruh proses yang melibatkan pemahaman bahasa alami (NLU), pelabelan berbasis deskripsi, dan pemberian rekomendasi strategis dilakukan oleh **Granite 3.2 8B** 🧠, dijalankan secara lokal lewat **LM Studio** 💻.  
**Python** berperan sebagai antarmuka pemrograman (*programming interface*) untuk:  
- Mengatur alur kerja.  
- Mengirim prompt & menerima respons.  
- Menggabungkan output batch.  
- Menyusun ringkasan tren efisien untuk ditinjau Granite.  

Peran AI dalam proyek ini:  
- 🏷️ Pelabelan dataset per jam (batched).  
- 📊 Interpretasi pola tren.  
- 💡 Pemberian saran operasional & strategis.

---

## 📂 File description  
| File | Deskripsi |
|------|-----------|
| **MetroPT3(AirCompressor).csv** | 📄 Dataset mentah (multivariate time series) 15 sensor APU kompresor; rekaman 1 Hz (Feb–Aug 2020). |
| **filedivider.py** | ✂️ Merata-ratakan data dari 1 detik menjadi 60 menit sekali. Output: `PT3_60min.csv`. |
| **labelingdata.py** | 🏷️ Meminta Granite memberi label kondisi per jam (Normal/AirLeak/HighStress/AirLeak-HighStress). Dibagi jadi 512 batch karena keterbatasan token/memori. Output: JSON per batch di folder `output_batches/`. |
| **filemerger.py** | 🔗 Menggabungkan semua batch JSON dari `labelingdata.py` menjadi satu dataset terlabel utuh. Output: `final_output.json`. |
| **visualization.py** | 🖼️ Membuat heatmap kalender dari data terlabel untuk melihat distribusi label per jam & hari. Output: `label_calendar.png`. |
| **trendanalysis.py** | 📊 Menghitung tren jam & hari rawan di Python, merangkumnya, lalu meminta Granite memberi rekomendasi strategis. Output: `trend_analysis.txt`. |

---
