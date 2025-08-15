import pandas as pd

# Baca CSV
df = pd.read_csv("MetroPT3(AirCompressor).csv", parse_dates=['timestamp'])

# Jadikan timestamp sebagai index
df.set_index('timestamp', inplace=True)

# Ambil setiap 60 menit (pakai rata-rata)
df_60min = df.resample('60T').mean()

# Reset index biar timestamp balik jadi kolom
df_60min = df_60min.reset_index()

# Simpan hasil
df_60min.to_csv("PT3_60min.csv", index=False)

print("Data asli:", len(df))
print("Data 60 menit:", len(df_60min))
