import pandas as pd
import random
from datetime import datetime, timedelta

employees = [f"Karyawan_{i}" for i in range(1, 31)]

start_date = datetime(2026, 6, 1)

data = []

for day in range(30):
    current_date = start_date + timedelta(days=day)

    for employee in employees:
        status = random.choices(
            ["Hadir", "Terlambat", "Izin", "Sakit", "Alpha"],
            weights=[85, 7, 4, 3, 1],
            k=1
        )[0]

        data.append([
            employee,
            current_date.strftime("%Y-%m-%d"),
            status
        ])

df = pd.DataFrame(
    data,
    columns=["Nama", "Tanggal", "Status"]
)

df.to_excel(
    "data/attendance.xlsx",
    index=False
)

print("Dataset berhasil dibuat!")
print(f"Jumlah data: {len(df)}")