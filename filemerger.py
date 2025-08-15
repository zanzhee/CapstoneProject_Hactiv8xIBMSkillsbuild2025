import os
import json
import re

# ==== KONFIGURASI ====
BATCH_FOLDER = "output_batches"  # Folder hasil batch
OUTPUT_FILE = "final_output.json"  # File gabungan
# =====================

all_data = []

# Regex untuk ambil nomor batch dari nama file
batch_pattern = re.compile(r"batch_(\d+)\.json")

# Ambil semua file di folder dan urutkan berdasarkan nomor batch
batch_files = sorted(
    [f for f in os.listdir(BATCH_FOLDER) if f.endswith(".json")],
    key=lambda x: int(batch_pattern.search(x).group(1)) if batch_pattern.search(x) else float('inf')
)

print(f"🔍 Ditemukan {len(batch_files)} file batch untuk digabungkan.")

# Loop setiap file batch
for file_name in batch_files:
    file_path = os.path.join(BATCH_FOLDER, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                all_data.extend(data)
            else:
                print(f"⚠️ {file_name} tidak berisi list JSON, dilewati.")
        print(f"✅ Gabung {file_name} ({len(data)} record)")
    except Exception as e:
        print(f"⚠️ Gagal membaca {file_name}: {e}")

# Simpan hasil gabungan
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"🎯 Semua batch berhasil digabung! Hasil tersimpan di {OUTPUT_FILE}")
