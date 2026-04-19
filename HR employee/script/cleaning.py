import pandas as pd
import numpy as np

# 1. LOAD DATA
df = pd.read_csv(r"C:\Users\LENOVO\Documents\DATA ANALYST\HR employee\HR_employee_data.csv")

# 2. DATA CLEANING
# Menghapus kolom yang tidak memberikan informasi (konstan)
# StandardHours biasanya 80 dan Over18 biasanya 'Y', tidak perlu dianalisis
cols_to_drop = ['EmployeeCount', 'StandardHours', 'Over18']
df = df.drop(columns=cols_to_drop)

# Cek duplikat
df = df.drop_duplicates()

# 3. DATA ENGINEERING: TRANSFORMASI ATTRITION
# Mengubah Attrition (Yes/No) menjadi angka agar bisa dihitung rata-ratanya (Rate) di Power BI
df['Attrition_Num'] = df['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)

# 4. DATA ENGINEERING: PENGELOMPOKAN (BINNING)
# Membuat kelompok usia (Age Group) agar visualisasi lebih rapi
bins = [18, 30, 40, 50, 60]
labels = ['18-29', '30-39', '40-49', '50-60']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

# 5. DATA ENGINEERING: TOTAL SATISFACTION SCORE
# Menggabungkan kepuasan lingkungan, pekerjaan, dan hubungan untuk skor total (Max 12)
df['Total_Satisfaction'] = df['EnvironmentSatisfaction'] + df['JobSatisfaction'] + df['RelationshipSatisfaction']

# 6. DATA ENGINEERING: RISK CATEGORY (Berdasarkan Overtime & WorkLifeBalance)
# Karyawan yang lembur terus dan Work-Life Balance rendah dianggap High Risk untuk Resign
def identify_risk(row):
    if row['OverTime'] == 'Yes' and row['WorkLifeBalance'] <= 2:
        return 'High Risk'
    elif row['OverTime'] == 'Yes' or row['WorkLifeBalance'] <= 2:
        return 'Medium Risk'
    else:
        return 'Low Risk'

df['Retention_Risk'] = df.apply(identify_risk, axis=1)

# 7. LOKALISASI CURRENCY (Opsional, jika ingin dikonversi ke IDR)
# MonthlyIncome di dataset ini biasanya dalam USD, kita konversi ke IDR (asumsi kurs 15.800)
df['Monthly_Income_IDR'] = df['MonthlyIncome'] * 15800

# 8. EXPORT HASIL
df.to_csv('Cleaned_HR_Analytics_Data.csv', index=False)
print("Data Engineering Selesai! File 'Cleaned_HR_Analytics_Data.csv' siap diimpor ke Power BI.")