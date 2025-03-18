# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DdvfRPByoXTMaL2RdUjj9E9Hos4zhzIR
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
import pulp
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib import colors

# =============== STREAMLIT CONFIG ====================
st.set_page_config(page_title="Supply Chain Optimization Dashboard", layout="wide")

# =============== HEADER + BRANDING ====================
st.markdown("""
    <style>
        .big-font {font-size:30px !important; font-weight: bold;}
        .small-font {font-size:14px !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big-font'>💄 Beauty Supply Chain Dashboard</h1>", unsafe_allow_html=True)
st.caption("Optimizing inventory, demand forecasting & cost efficiency 🚚")

# =============== SIDEBAR NAV ========================
st.sidebar.title("📂 Menu")
page = st.sidebar.radio("Navigate to:", [
    "1️⃣ Upload Data",
    "2️⃣ EDA & Pareto",
    "3️⃣ ML Forecasting",
    "4️⃣ Optimization & Reporting"
])

# =============== FILE UPLOAD ========================
if page == "1️⃣ Upload Data":
    st.subheader("📁 Upload Supply Chain CSV")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())
        st.session_state.df = df

# =============== EDA + PARETO ========================
elif page == "2️⃣ EDA & Pareto":
    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload your dataset first.")
    else:
        df = st.session_state.df
        st.subheader("📊 Exploratory Data Analysis")
        st.write(df.describe())

        st.subheader("📉 Missing Data Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(df.isnull(), cbar=False, ax=ax)
        st.pyplot(fig)

        st.subheader("💡 Pareto Analysis: Top Cost Drivers")
        pareto = df.groupby('Product type')['Costs'].sum().sort_values(ascending=False)
        pareto_cumsum = pareto.cumsum() / pareto.sum()

        fig, ax = plt.subplots()
        pareto.plot(kind='bar', ax=ax, color='skyblue')
        pareto_cumsum.plot(secondary_y=True, marker="o", ax=ax, color='red')
        ax.set_ylabel('Total Costs')
        ax.right_ax.set_ylabel('% Cumulative')
        st.pyplot(fig)

# =============== ML FORECAST ========================
elif page == "3️⃣ ML Forecasting":
    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload your dataset first.")
    else:
        df = st.session_state.df.copy()
        supplier_lead_time_col = 'Supplier Lead Time' if 'Supplier Lead Time' in df.columns else 'Lead times'
        df['Shipping_Cost_per_Unit'] = df['Shipping costs'] / df['Number of products sold'].replace(0, 1)
        df['Revenue_per_Product'] = df['Revenue generated'] / df['Number of products sold'].replace(0, 1)
        df['Stock_Cover_Ratio'] = df['Stock levels'] / df['Number of products sold'].replace(0, 1)
        df['Lead_Time_Pressure'] = df[supplier_lead_time_col] * df['Order quantities']
        df['Cost_Efficiency'] = df['Costs'] / df['Revenue generated'].replace(0, 1)

        df_encoded = pd.get_dummies(df)
        target = 'Number of products sold'
        sku_cols = [col for col in df_encoded.columns if col.startswith('SKU_')]
        X = df_encoded.drop(columns=[target, 'Revenue generated'] + sku_cols)
        y = df_encoded[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = XGBRegressor(objective='reg:squarederror', n_estimators=300, max_depth=7, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        st.success(f"✅ R² Score: {r2_score(y_test, y_pred):.2%}")
        st.success(f"✅ RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

        df['Forecasted_Demand'] = model.predict(X)
        st.session_state.df_model = df

# =============== OPTIMIZATION + REPORT ===============
elif page == "4️⃣ Optimization & Reporting":
    if 'df_model' not in st.session_state:
        st.warning("⚠️ Please forecast demand first (run Step 3).")
    else:
        df = st.session_state.df_model.copy()

        # Filters
        st.subheader("🎛️ Filter your data")
        region_filter = st.multiselect("Select Region(s):", options=df['Location'].unique(), default=list(df['Location'].unique()))
        product_filter = st.multiselect("Select Product Type(s):", options=df['Product type'].unique(), default=list(df['Product type'].unique()))
        df = df[(df['Location'].isin(region_filter)) & (df['Product type'].isin(product_filter))]

        df['Stock_Surplus'] = df['Stock levels'] - df['Forecasted_Demand']
        df['Stockout_Flag'] = df['Stock_Surplus'] < 0

        prob = pulp.LpProblem("Inventory_Optimization", pulp.LpMinimize)
        reorder_vars, surplus_vars, stockout_vars = {}, {}, {}
        holding_cost_per_unit = 2.0
        stockout_cost_per_unit = 10.0

        for idx, row in df.iterrows():
            reorder_vars[idx] = pulp.LpVariable(f"reorder_{idx}", lowBound=0)
            surplus_vars[idx] = pulp.LpVariable(f"surplus_{idx}", lowBound=0)
            stockout_vars[idx] = pulp.LpVariable(f"stockout_{idx}", lowBound=0)
            demand = row['Forecasted_Demand']
            stock = row['Stock levels']
            prob += surplus_vars[idx] - stockout_vars[idx] == stock + reorder_vars[idx] - demand

        prob += pulp.lpSum([holding_cost_per_unit * surplus_vars[k] + stockout_cost_per_unit * stockout_vars[k] for k in reorder_vars])
        solver = pulp.COIN_CMD(path="/opt/homebrew/bin/cbc", msg=True)
        prob.solve(solver)

        df['Optimal_Reorder'] = [reorder_vars[idx].varValue for idx in df.index]
        df['Post_Stockout'] = df['Stock levels'] + df['Optimal_Reorder'] - df['Forecasted_Demand']
        df['Post_Stockout'] = df['Post_Stockout'] < 0

        st.metric("📉 Pre-Optimization Stockouts", int(df['Stockout_Flag'].sum()))
        st.metric("✅ Post-Optimization Stockouts", int(df['Post_Stockout'].sum()))

        st.subheader("📊 Stockouts Before vs After Optimization")
        fig, ax = plt.subplots()
        sns.barplot(x=['Pre-Optimization', 'Post-Optimization'],
                    y=[df['Stockout_Flag'].sum(), df['Post_Stockout'].sum()],
                    palette='viridis', ax=ax)
        plt.savefig("stockout_chart.png")
        st.pyplot(fig)

        # ReportLab PDF Export with chart & table
        st.subheader("📄 Export Report as PDF (ReportLab)")

        if st.button("Generate PDF Report"):
            c = canvas.Canvas("report.pdf", pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, "📦 Optimized Inventory Report")
            c.setFont("Helvetica", 12)
            c.drawString(50, 730, f"Region(s): {', '.join(region_filter)}")
            c.drawString(50, 710, f"Product Type(s): {', '.join(product_filter)}")
            c.drawString(50, 690, f"Pre-Optimization Stockouts: {int(df['Stockout_Flag'].sum())}")
            c.drawString(50, 670, f"Post-Optimization Stockouts: {int(df['Post_Stockout'].sum())}")

            # Insert chart image
            c.drawImage("stockout_chart.png", 50, 400, width=400, preserveAspectRatio=True)

            # Insert table
            table_data = [["Location", "Product", "Optimal Reorder"]]
            for i, row in df.iterrows():
                table_data.append([row['Location'], row['Product type'], f"{row['Optimal_Reorder']:.0f}"])

            t = Table(table_data, colWidths=[100, 150, 100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            t.wrapOn(c, 50, 300)
            t.drawOn(c, 50, 300)

            c.save()
            st.success("✅ PDF generated as report.pdf with chart & table!")