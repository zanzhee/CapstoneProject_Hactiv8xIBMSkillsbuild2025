import pandas as pd
import math
import json
import time
import requests
import os

# ==== KONFIGURASI ====
CSV_FILE = "PT3_60min.csv"                # Nama file CSV
BATCH_SIZE = 10                           # Kecilkan biar aman token
OUTPUT_FOLDER = "output_batches"          # Folder untuk simpan hasil batch
MODEL_NAME = "granite-3.2-8b"             # Model Granite di LM Studio
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
# =====================

# Baca CSV
df = pd.read_csv(CSV_FILE)

# Hilangkan kolom index jika ada
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

total_rows = len(df)
total_batches = math.ceil(total_rows / BATCH_SIZE)
print(f"Total data: {total_rows} baris → {total_batches} batch")

# Buat folder output kalau belum ada
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Loop batch
for i in range(total_batches):
    start = i * BATCH_SIZE
    end = min(start + BATCH_SIZE, total_rows)
    batch_df = df.iloc[start:end]
    batch_list = batch_df.to_dict(orient='records')

    prompt = f"""
You are an expert railway maintenance assistant.
Classify the operational status of a train's air compressor based on sensor readings.

For each JSON object, return:
- timestamp (as given)
- date (YYYY-MM-DD)
- hour (0-23) extracted from timestamp
- label: one of Normal, AirLeak, HighStress, AirLeak-HighStress
- confidence (0.0 - 1.0)
- reason (short technical explanation)

Data:
{json.dumps(batch_list, ensure_ascii=False)}

Return only a JSON array.
"""

    try:
        # Kirim ke LM Studio API
        response = requests.post(
            LMSTUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            }
        )

        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code} - {response.text}")

        result_text = response.json()["choices"][0]["message"]["content"]
        parsed_result = json.loads(result_text)

        # Simpan hasil batch ke file terpisah
        batch_file = os.path.join(OUTPUT_FOLDER, f"batch_{i+1}.json")
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(parsed_result, f, ensure_ascii=False, indent=2)

        print(f"✅ Batch {i+1}/{total_batches} selesai → disimpan di {batch_file}")

    except Exception as e:
        print(f"⚠️ Error pada batch {i+1}: {e}")

    time.sleep(1)  # jeda biar server aman

print(f"🎯 Semua selesai! Hasil ada di folder '{OUTPUT_FOLDER}'")
