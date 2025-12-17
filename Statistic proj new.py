# =====================================================
# STREAMLIT SURVEY ANALYSIS WEB APP (FINAL – COMPLETE)
# Descriptive Statistics, Frequency Tables, Composite Scores,
# Association Analysis, and Pearson Assumptions
# Languages: English & Indonesian
# Group Members: Juna, Giev, Riski, and Lena
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# Language Dictionary
# ===============================
TEXT = {
    "EN": {
        "title": "Survey Data Analysis Web App",
        "upload": "Upload Survey Dataset (CSV or Excel)",
        "desc": "Descriptive Statistics",
        "freq": "Frequency & Percentage Table",
        "assoc": "Association Analysis (X and Y)",
        "select_x": "Select Variable X",
        "select_y": "Select Variable Y",
        "method": "Choose Association Method",
        "pearson": "Pearson Correlation",
        "spearman": "Spearman Correlation",
        "members": "Group Members: Juna, Giev, Riski, and Lena",
        "interp": "Interpretation",
        "assump": "Pearson Correlation Assumptions",
        "composite": "Composite Scores"
    },
    "ID": {
        "title": "Aplikasi Analisis Data Survei",
        "upload": "Unggah Dataset Survei (CSV atau Excel)",
        "desc": "Statistik Deskriptif",
        "freq": "Tabel Frekuensi & Persentase",
        "assoc": "Analisis Asosiasi (X dan Y)",
        "select_x": "Pilih Variabel X",
        "select_y": "Pilih Variabel Y",
        "method": "Pilih Metode Asosiasi",
        "pearson": "Korelasi Pearson",
        "spearman": "Korelasi Spearman",
        "members": "Anggota Kelompok: Juna, Giev, Riski, and Lena",
        "interp": "Interpretasi",
        "assump": "Asumsi Korelasi Pearson",
        "composite": "Skor Komposit"
    }
}

# ===============================
# Functions
# ===============================

def descriptive_stats(series):
    return {
        "Mean": series.mean(),
        "Median": series.median(),
        "Mode": series.mode().iloc[0] if not series.mode().empty else np.nan,
        "Min": series.min(),
        "Max": series.max(),
        "Std": series.std()
    }


def correlation_value(df, x, y, method):
    return df[[x, y]].corr(method=method).iloc[0, 1]


def interpret_corr(r, lang):
    if abs(r) < 0.3:
        strength = "Weak" if lang == "EN" else "Lemah"
    elif abs(r) < 0.6:
        strength = "Moderate" if lang == "EN" else "Sedang"
    else:
        strength = "Strong" if lang == "EN" else "Kuat"

    direction = "Positive" if r > 0 else "Negative"
    if lang == "ID":
        direction = "Positif" if r > 0 else "Negatif"

    return f"{direction}, {strength}"

# ===============================
# Streamlit UI
# ===============================
st.set_page_config(page_title="Survey Analysis", layout="wide")

lang = st.sidebar.selectbox("Language / Bahasa", ["EN", "ID"])

st.title(TEXT[lang]["title"])
st.write(TEXT[lang]["members"])

file = st.file_uploader(TEXT[lang]["upload"], type=["csv", "xlsx"])

if file is not None:

    # ---------- Read Data ----------
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # Force numeric conversion (important for Excel Likert data)
    df_num = df.apply(pd.to_numeric, errors="coerce")
    numeric_cols = df_num.columns[df_num.notna().any()].tolist()

    if len(numeric_cols) == 0:
        st.error("No numeric variables detected. Please check your data format.")
        st.stop()

    # ===============================
    # Descriptive Statistics
    # ===============================
    st.subheader(TEXT[lang]["desc"])

    desc_rows = []
    for col in numeric_cols:
        stats = descriptive_stats(df_num[col].dropna())
        row = {"Variable": col}
        row.update(stats)
        desc_rows.append(row)

    desc_df = pd.DataFrame(desc_rows).set_index("Variable")
    st.dataframe(desc_df.round(3))

    # ===============================
    # Frequency & Percentage Tables
    # ===============================
    st.subheader(TEXT[lang]["freq"])
    freq_var = st.selectbox("Variable", numeric_cols)

    freq_table = df_num[freq_var].value_counts().sort_index()
    perc_table = (freq_table / freq_table.sum()) * 100

    freq_df = pd.DataFrame({
        "Frequency": freq_table,
        "Percentage (%)": perc_table.round(2)
    })

    st.dataframe(freq_df)

    # ===============================
    # Composite Scores (X_total, Y_total)
    # ===============================
    st.subheader(TEXT[lang]["composite"])

    x_items = st.multiselect("Items for X_total", numeric_cols)
    y_items = st.multiselect("Items for Y_total", numeric_cols)

    if x_items:
        df_num["X_total"] = df_num[x_items].mean(axis=1)
        st.write("X_total created")

    if y_items:
        df_num["Y_total"] = df_num[y_items].mean(axis=1)
        st.write("Y_total created")

    # ===============================
    # Association Analysis
    # ===============================
    st.subheader(TEXT[lang]["assoc"])

    assoc_cols = df_num.columns.tolist()

    x_var = st.selectbox(TEXT[lang]["select_x"], assoc_cols)
    y_var = st.selectbox(TEXT[lang]["select_y"], assoc_cols)

    method = st.selectbox(
        TEXT[lang]["method"],
        ["pearson", "spearman"],
        format_func=lambda x: TEXT[lang][x]
    )

    r = correlation_value(df_num, x_var, y_var, method)

    st.write(f"r = {r:.3f}")
    st.write(f"{TEXT[lang]['interp']}: {interpret_corr(r, lang)}")

    fig, ax = plt.subplots()
    ax.scatter(df_num[x_var], df_num[y_var])
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    st.pyplot(fig)

    # ===============================
    # Pearson Assumptions (Narrative)
    # ===============================
    st.subheader(TEXT[lang]["assump"])

    if lang == "EN":
        st.markdown("""
        **1. Normality**: Variables should be approximately normally distributed.  
        **2. Linearity**: The relationship between X and Y should be linear.  
        **3. Homoscedasticity**: Variance of Y should be constant across X.  
        **4. No Extreme Outliers**: Outliers can distort the correlation coefficient.  
        **5. Scale of Measurement**: Variables should be measured on an interval or ratio scale.
        """)
    else:
        st.markdown("""
        **1. Normalitas**: Variabel X dan Y harus berdistribusi mendekati normal.  
        **2. Linearitas**: Hubungan antara X dan Y harus linear.  
        **3. Homoskedastisitas**: Variansi Y relatif konstan pada setiap nilai X.  
        **4. Tidak Ada Outlier Ekstrem**: Outlier dapat memengaruhi nilai korelasi.  
        **5. Skala Pengukuran**: Variabel harus berskala interval atau rasio.
        """)
