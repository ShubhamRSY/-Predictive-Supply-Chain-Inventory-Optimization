# 📦 Predictive Supply Chain & Inventory Optimization Tool

## 🚀 Overview
This project is a complete end-to-end **Predictive Supply Chain & Inventory Optimization Tool** for the beauty industry. It forecasts product demand by region, reduces stockouts, avoids overstocking, and minimizes total supply chain costs.

The system integrates:
- **Machine Learning Models (Random Forest, XGBoost)**
- **Optimization with Linear Programming (PuLP)**
- **Streamlit Interactive Dashboard**
- **Automated PDF Reporting**

## 🛠️ Tech Stack
- Python (Pandas, NumPy, Scikit-Learn, XGBoost)
- Streamlit (Dashboard)
- Matplotlib & Seaborn (EDA Visualizations)
- ReportLab (PDF Generation)
- PuLP (Optimization Solver)
- Google Colab (initial prototyping)

## 🎯 Problem Statement
The goal is to predict product demand and optimize inventory levels across regions to:
- Minimize stockouts
- Avoid overstocking
- Reduce total supply chain costs

## 📊 Features
- 📁 **Data Upload & EDA**: Upload CSV, view dataset statistics, heatmaps, and Pareto analysis
- 🔍 **ML Forecasting**: Predict demand using advanced feature engineering + XGBoost model
- 🎯 **Inventory Optimization**: Linear programming to optimize reorder quantities
- 📝 **Auto PDF Reporting**: Generate PDF reports with data tables, KPIs & visual charts
- 🌐 **Streamlit Dashboard**: Fully interactive supply chain app

## 📂 Directory Structure
```text
├── app.py                         # Streamlit Dashboard (full pipeline)
├── beauty_supply_chain.py         # Jupyter Notebook (EDA + ML + Insights)
├── Beauty_supply_chain.ipynb.pdf  # Notebook Report PDF
├── requirements.txt               # Python dependencies
└── README.md
```

## 📈 Key Insights
- **Pareto Rule**: ~20% of SKUs contribute to 80%+ of total supply chain costs
- **Supplier Risk Matrix**: Supplier 5 flagged as high-risk (longest shipping + highest defect rates)
- **Region-wise Inventory Imbalance**: Excess stock in Kolkata
- **Transport Cost Drivers**: Air freight is the most expensive mode, recommendation to shift to sea/rail

## 🧠 Machine Learning Pipeline
1. **EDA & Cleaning**
   - Null checks, duplicates, standardization
   - Categorical encoding, feature scaling (StandardScaler)

2. **Feature Engineering**
   - Shipping cost per unit
   - Revenue per product
   - Stock cover ratio
   - Lead time pressure
   - Cost efficiency

3. **ML Model**
   - Random Forest baseline (R² ~86%)
   - XGBoost (hyperparameter-tuned, R² ~87%)
   
4. **Optimization**
   - Linear programming to optimize reorder quantities
   - Objective: Minimize holding & stockout costs

## 🖥️ Streamlit App Workflow
1. **Upload CSV** via Streamlit sidebar
2. **EDA & Pareto Dashboard** (Heatmaps, Sales Analysis, Cost Drivers)
3. **ML Demand Forecasting** (Train XGBoost model)
4. **Optimization & Reporting**
   - Generate optimal reorder recommendations
   - Download PDF report with charts & tables

## 📊 Sample Visualizations
- Product sales distribution
- Revenue vs supply chain costs (by product type)
- Supplier defect rates
- Supplier risk heatmap
- Pareto chart (SKU cost analysis)
- Supplier KPI radar chart

## ⚙️ Installation
```bash
# Clone the repository
git clone https://github.com/your-username/predictive-supply-chain-tool.git
cd predictive-supply-chain-tool

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## ✅ Requirements
```
streamlit
pandas
numpy
scikit-learn
xgboost
seaborn
matplotlib
pulp
reportlab
```

## 📄 Output Example (PDF Report)
- Region & product type filters
- Pre vs Post-Optimization stockout comparison
- Optimal reorder quantity recommendations
- Charts embedded (stockouts, Pareto analysis)

## 🤝 Contribution
Feel free to fork this project, open issues, or submit PRs. Let’s improve supply chain analytics together!


---

**Crafted with ❤️ for supply chain professionals and data scientists.**
