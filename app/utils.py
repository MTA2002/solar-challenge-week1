# app/utils.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

DATA_PATHS = {
    'Benin': 'data/benin_clean.csv',
    'Sierra Leone': 'data/sierraleone-bumbuna.csv',
    'Togo': 'data/togo-dapaong_qc.csv'
}

def load_all_data():
    data = {}
    for country, path in DATA_PATHS.items():
        if Path(path).exists():
            df = pd.read_csv(path)
            df['Country'] = country
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            data[country] = df
    return data

def get_top_regions(df, metric='GHI', n=3):
    """Return top N countries by mean metric (only numeric columns)."""
    if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
        return pd.DataFrame(columns=['Country', 'mean'])
    
    return (
        df.groupby('Country')[metric]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .round(1)
        .reset_index()
        .rename(columns={metric: 'mean'})  # ← ENSURE COLUMN IS 'mean'
    )

def create_boxplot(df, metric):
    if metric not in df.columns:
        return go.Figure().add_annotation(text=f"Metric {metric} not found", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    fig = px.box(df, x='Country', y=metric, color='Country', color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(showlegend=False, height=500, title=f"{metric} Distribution by Country")
    return fig

def create_trend_line(df):
    daily = df.copy()
    daily['Date'] = daily['Timestamp'].dt.date
    daily = daily.groupby(['Country', 'Date']).mean(numeric_only=True).reset_index()

    fig = go.Figure()
    colors = {'Benin': '#10B981', 'Sierra Leone': '#F59E0B', 'Togo': '#3B82F6'}

    for country in df['Country'].unique():
        subset = daily[daily['Country'] == country]
        if 'GHI' not in subset.columns:
            continue
        fig.add_trace(go.Scatter(
            x=subset['Date'], y=subset['GHI'],
            mode='lines', name=country,
            line=dict(color=colors.get(country, '#888'), width=3)
        ))

        if 'Cleaning' in df.columns:
            clean = df[(df['Country'] == country) & (df['Cleaning'] == 1)]
            if not clean.empty:
                clean_dates = clean['Timestamp'].dt.date.unique()
                max_ghi = subset['GHI'].max() if not subset.empty else 0
                fig.add_trace(go.Scatter(
                    x=list(clean_dates),
                    y=[max_ghi * 1.1] * len(clean_dates),
                    mode='markers', name=f"{country} Cleaning",
                    marker=dict(symbol='star', size=12, color=colors.get(country), line=dict(width=2, color='red'))
                ))

    fig.update_layout(title="Daily GHI Trends", xaxis_title="Date", yaxis_title="GHI (W/m²)", height=500)
    return fig