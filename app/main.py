# app/main.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_all_data, get_top_regions, create_boxplot, create_trend_line

st.set_page_config(
    page_title="Solar Investment Dashboard",
    page_icon="solar_panel",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CSS ===
st.markdown("""
<style>
    .main > div {padding-top: 2rem;}
    .metric-card {background: #f8f9fa; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .header {font-size: 2.8rem; font-weight: bold; color: #1E3A8A; text-align: center;}
    .subheader {font-size: 1.6rem; color: #1E40AF; text-align: center;}
</style>
""", unsafe_allow_html=True)

# === Title ===
st.markdown("<div class='header'>Solar Farm Investment Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>MoonLight Energy Solutions</div>", unsafe_allow_html=True)
st.markdown("---")

# === Load Data ===
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()
if not data:
    st.error("No data found in `data/` folder. Run Task 2 first.")
    st.stop()

countries = list(data.keys())

# === Sidebar Widgets ===
with st.sidebar:
    st.image("https://img.icons8.com/fluency/48/solar-panel.png")
    st.title("Controls")
    
    selected_countries = st.multiselect(
        "Select Countries", countries, default=countries
    )
    
    metric = st.selectbox(
        "Primary Metric", ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
    )
    
    st.markdown("---")
    st.markdown("### Filters")
    show_cleaning = st.checkbox("Show Cleaning Events", value=True)
    top_n = st.slider("Top Regions to Display", 1, 3, 3)

# === Combine Data ===
df_list = [data[c] for c in selected_countries]
df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()

if df.empty:
    st.warning("No countries selected.")
    st.stop()

# === KPI Cards ===
col1, col2, col3 = st.columns(3)
mean_ghi = df['GHI'].mean()
top_country = df.groupby('Country')['GHI'].mean().idxmax()
clean_gain = (df[df['Cleaning']==1]['ModA'].mean() - df[df['Cleaning']==0]['ModA'].mean()) if 'Cleaning' in df.columns else 0

with col1:
    st.markdown(f"<div class='metric-card'><h3>{mean_ghi:.1f}</h3><p>Avg GHI (W/m²)</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>{top_country}</h3><p>Top Country</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>+{clean_gain:.1f}</h3><p>Cleaning Gain</p></div>", unsafe_allow_html=True)

st.markdown("---")

# === 1. Boxplot ===
st.subheader(f"{metric} Distribution")
fig_box = create_boxplot(df, metric)
st.plotly_chart(fig_box, use_container_width=True)

# === 2. Time Series ===
st.subheader("Daily GHI Trends")
fig_trend = create_trend_line(df)
st.plotly_chart(fig_trend, use_container_width=True)

# === 3. Top Regions Table ===
st.subheader(f"Top {top_n} Regions by {metric}")
top_df = get_top_regions(df, metric, top_n)
st.table(top_df.style.format({"mean": "{:.1f}"}))

# === 4. Recommendation ===
st.success(f"""
**Recommendation**: **{top_country}** is the best location for solar investment:
- Highest average **{metric}**: {top_df.iloc[0]['mean']:.1f}
- Strong cleaning response
- Ideal for scalable solar farms
""")

# === Footer ===
st.markdown("---")
st.caption("10 Academy | Solar Data Discovery | Mahfouz Teyib | Local: http://localhost:8501")