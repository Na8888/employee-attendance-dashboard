import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(
    page_title="Employee Attendance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Employee Attendance Analytics Dashboard")

# ======================
# LOAD DATA
# ======================

uploaded_file = st.sidebar.file_uploader(
    "Upload Attendance File",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_excel("data/attendance.xlsx")

# ======================
# FILTER
# ======================

def sort_employee(name):
    match = re.search(r'(\d+)$', str(name))

    if match:
        return (0, int(match.group()))

    return (1, str(name).lower())

employee_names = sorted(
    df["Nama"].unique(),
    key=sort_employee
)

employee_list = ["Semua"] + employee_names

selected_employee = st.sidebar.selectbox(
    "Pilih Karyawan",
    employee_list
)

if selected_employee != "Semua":
    df = df[df["Nama"] == selected_employee]

# ======================
# KPI
# ======================

total_records = len(df)
total_employees = df["Nama"].nunique()

hadir = len(df[df["Status"] == "Hadir"])
terlambat = len(df[df["Status"] == "Terlambat"])

attendance_rate = (hadir / total_records) * 100

late_rate = (terlambat / total_records) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Karyawan", total_employees)
col2.metric("📄 Total Record", total_records)
col3.metric("✅ Attendance Rate", f"{attendance_rate:.2f}%")
col4.metric("⏰ Late Rate", f"{late_rate:.2f}%")

st.divider()

# ======================
# CHARTS
# ======================

col_left, col_right = st.columns(2)

with col_left:

    st.subheader("Distribusi Kehadiran")

    status_counts = df["Status"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(5,5))

    ax1.pie(
        status_counts,
        labels=status_counts.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig1)

with col_right:

    st.subheader("Top Kehadiran Karyawan")

    ranking = (
        df[df["Status"] == "Hadir"]
        .groupby("Nama")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(6,5))

    ranking.plot(
        kind="bar",
        ax=ax2
    )

    ax2.set_ylabel("Jumlah Hadir")

    st.pyplot(fig2)

st.divider()

# ======================
# TOP PERFORMER
# ======================

st.subheader("🏆 Top Performer")

ranking_table = (
    df[df["Status"] == "Hadir"]
    .groupby("Nama")
    .size()
    .reset_index(name="Jumlah Hadir")
)

ranking_table = ranking_table.sort_values(
    by="Jumlah Hadir",
    ascending=False
).reset_index(drop=True)

ranking_table.index = ranking_table.index + 1

st.dataframe(
    ranking_table,
    width="stretch",
    hide_index=False
)

ranking_table.index = range(1, len(ranking_table) + 1)

best_employee = ranking_table.iloc[0]

st.success(
    f"Top Performer: {best_employee['Nama']} dengan {best_employee['Jumlah Hadir']} hari hadir."
)

st.info(
    f"Tingkat kehadiran perusahaan mencapai {attendance_rate:.2f}% dari total {total_records} data absensi."
)