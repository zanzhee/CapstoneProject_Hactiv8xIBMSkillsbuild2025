# 📊 Analisis Pola Kejadian Gangguan Kompresor Kereta Metro dan Rekomendasi Strategis Menggunakan Granite 3.2 8B
**Hacktiv8 x IBM SkillsBuild — Agustus 2025**  
Muhammad Fauzan Azhima  

---

## 📝 Project overview  
Unit Produksi Udara (Air Production Unit/APU) pada kompresor kereta metro adalah komponen vital yang bertugas menjaga tekanan udara untuk sistem rem, pintu, dan berbagai mekanisme pneumatik. Gangguan pada sistem ini, seperti *air leak* atau *high stress*, dapat menyebabkan penurunan kinerja hingga potensi kerusakan serius yang mengganggu operasional kereta. Oleh karena itu, pemantauan kondisi APU secara rutin menjadi kunci untuk menjaga keselamatan dan efisiensi.

Proyek ini hadir untuk menjawab permasalahan tersebut dengan memanfaatkan dataset **MetroPT-3**, yang berisi rekaman multivariate time series dari 15 sensor APU. Permasalahan utama yang dihadapi adalah ukuran dataset yang sangat besar (rekaman 1 Hz selama Februari 2020 - Agustus 2020), keterbatasan perangkat, dan tidak adanya label kondisi pada data mentah. Data mentah perlu diolah agar dapat digunakan untuk analisis pola gangguan secara efektif.

Pendekatan yang diambil dimulai dengan merata-ratakan data menjadi interval 60 menit untuk mengurangi ukuran dataset dan membatasi periode analisis 1 Februari 2020 - 28 Maret 2020. Data hasil agregasi kemudian dilabeli menjadi empat kategori kondisi operasional: **Normal**, **AirLeak**, **HighStress**, dan **AirLeak-HighStress**. Proses pelabelan dilakukan oleh **Granite 3.2 8B** yang dijalankan secara lokal melalui **LM Studio**, dengan **Python** sebagai antarmuka pemrograman untuk mengatur alur kerja dan pemrosesan hasil.

Karena keterbatasan token model, pelabelan dilakukan dalam batch dan hasilnya digabungkan kembali menjadi satu dataset terlabel lengkap. Python kemudian digunakan untuk menghitung tren jam dan hari rawan terjadinya gangguan. Ringkasan tren yang padat ini dikirim ke Granite untuk dianalisis, sehingga Granite dapat memberikan rekomendasi strategis yang langsung dapat diimplementasikan oleh perusahaan, seperti penjadwalan *preventive maintenance*, pengaturan beban operasi di jam rawan, dan penerapan sistem peringatan dini. Dengan pendekatan ini, proyek tidak hanya mengidentifikasi pola gangguan, tetapi juga mengubah data mentah menjadi wawasan operasional yang actionable bagi pengambil keputusan.

Setiap sampel per jam dilabeli menjadi salah satu kategori:  
- ✅ **Normal**  
- 🟠 **AirLeak**  
- 🔴 **HighStress**  
- 🟣 **AirLeak-HighStress**  

Untuk efisiensi token dan memori model, pelabelan dilakukan dalam batch. Hasil pelabelan digabungkan, lalu **Python** menghitung tren jam & hari rawan 📈. Ringkasan tren tersebut dikirim ke **Granite 3.2 8B** (lokal via LM Studio) agar Granite dapat fokus memberikan rekomendasi strategis  bagi perusahaan.  

---

## 🔗 Raw dataset  
MetroPT-3 (AirCompressor) — multivariate time series dari 15 sensor APU kompresor kereta metro.  
📥 [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/791/metropt%2B3%2Bdataset?utm_)  

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

### 🏷️ Pelabelan Data Operasional  
- Mengkategorikan setiap sampel per jam ke dalam label **Normal**, **AirLeak**, **HighStress**, atau **AirLeak-HighStress**.  
- Proses dilakukan dalam batch karena keterbatasan token/memori model.  

### 📊 Analisis Tren Berbasis Ringkasan  
- Menerima ringkasan tren yang dihasilkan Python (jam & hari rawan).  
- Menginterpretasi pola dari tren tersebut untuk menemukan insight tambahan.  

### 💡 Pemberian Rekomendasi Strategis  
- Mengusulkan langkah yang dapat dilakukan perusahaan untuk mengurangi risiko gangguan, seperti:  
  - Penjadwalan *preventive maintenance* di waktu optimal.  
  - Penyesuaian beban operasional di jam rawan.  
  - Implementasi sistem peringatan dini.  

### 📢 Pendukung Insight Operasional  
- Memberikan narasi penjelasan yang mudah dipahami pengambil keputusan, sehingga data teknis bisa langsung diterjemahkan menjadi kebijakan operasional.



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
