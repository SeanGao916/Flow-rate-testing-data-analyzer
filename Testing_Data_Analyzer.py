#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 00:12:09 2025

@author: seangao
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dual Analyzer", page_icon="📊", layout="wide")
st.title("📊 Testing Data Analyzer")

col1, col2 = st.columns(2)

# ---------------- Left Side: 3000 data points (CSV)
with col1:
    st.header("📁 Pressure Data Analyzer")
    st.markdown("**Read from row 12 onward | Columns: Pressure1 (col 2) & Pressure2 (col 4)**")

    csv_file = st.file_uploader("📂 Upload **Pressure Sensor** CSV file", type=["csv"], key="csv")

    if csv_file is not None:
        try:
            df_csv = pd.read_csv(csv_file, header=None, skiprows=11)
            value1 = pd.to_numeric(df_csv[1], errors='coerce').head(3000)
            value2 = pd.to_numeric(df_csv[3], errors='coerce').head(3000)

            st.subheader("✅ Average of 5 minutes Data Points (3000 data)")
            st.write(f" **Pressure 1 (col 2):** {value1.mean():.6f}")
            st.write(f" **Pressure 2 (col 4):** {value2.mean():.6f}")

            with st.expander("🔍 Preview CSV Data (first 5 rows)"):
                st.dataframe(df_csv.head())

        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")

# ---------------- Right Side: 300 data points (Excel or CSV with headers)
with col2:
    st.header("📁 DAQ Data Analyzer")
    st.markdown("**Read from row 56 onward | T_inlet (°C), Side P_1 (PSI), Side P_2 (PSI), & Main_dowmstream Flow rate (LPM)**")

    uploaded_file = st.file_uploader("📂 Upload **DAQ** CSV file", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        try:
            # Detect file type
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, header=54)  # Row 56 = index 55
            else:
                df = pd.read_excel(uploaded_file, header=54)

            # Define target columns (you can also use column letters if headers not present)
            target_columns = [
                "101 (°C)- T_inlet",
                "121 (PSI)- Side P_1",
                "122 (PSI)- Side P_2",
                "221 (LPM)- Flow rate_1"
            ]
            
                
            missing = [col for col in target_columns if col not in df.columns]
            if missing:
                st.error(f"❌ These columns are missing in your file: {missing}")
            else:
                df = df[target_columns].dropna().head(300)

                st.subheader("✅ Average of 5 minutes Data Points (300 data)")
                for col in target_columns:
                    avg = df[col].mean()
                    st.write(f"**{col}**: {avg:.6f}")
                    
            with st.expander("🔍 Preview CSV Data (first 5 rows)"):
                st.dataframe(df.head())

        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")
