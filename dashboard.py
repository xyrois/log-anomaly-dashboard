import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from anomaly_detector import detect_anomalies

st.set_page_config(page_title="Log Anomaly Detection", layout="wide")

st.title("🔍 Log Anomaly Detection Dashboard")

# Load data
try:
    df = pd.read_csv("parsed_logs.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Detect anomalies
    anomalies_df = detect_anomalies(df)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requests", len(df))
    with col2:
        st.metric("Unique IPs", df['ip'].nunique())
    with col3:
        st.metric("Error Responses", df['is_error'].sum())
    with col4:
        st.metric("Anomalies Detected", len(anomalies_df) if not anomalies_df.empty else 0)
    
    st.divider()
    
    # Anomalies section
    if not anomalies_df.empty:
        st.subheader("🚨 Detected Anomalies")
        
        # Color code by severity
        def highlight_severity(row):
            if row['severity'] == 'HIGH':
                return ['background-color: #ffcccc'] * len(row)
            elif row['severity'] == 'MEDIUM':
                return ['background-color: #fff4cc'] * len(row)
            return [''] * len(row)
        
        styled_df = anomalies_df.style.apply(highlight_severity, axis=1)
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("✓ No anomalies detected in the logs")
    
    st.divider()
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Status Code Distribution")
        status_counts = df['status'].value_counts().sort_index()
        fig = px.bar(x=status_counts.index, y=status_counts.values,
                     labels={'x': 'Status Code', 'y': 'Count'},
                     color=status_counts.values,
                     color_continuous_scale='reds')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Requests by IP")
        ip_counts = df['ip'].value_counts().head(10)
        fig = px.bar(x=ip_counts.values, y=ip_counts.index, orientation='h',
                     labels={'x': 'Request Count', 'y': 'IP Address'},
                     color=ip_counts.values,
                     color_continuous_scale='blues')
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.subheader("Request Timeline")
    timeline_df = df.groupby([df['timestamp'].dt.floor('1min'), 'status']).size().reset_index()
    timeline_df.columns = ['timestamp', 'status', 'count']
    timeline_df['status'] = timeline_df['status'].astype(str)
    
    fig = px.line(timeline_df, x='timestamp', y='count', color='status',
                  labels={'count': 'Request Count', 'timestamp': 'Time'},
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Raw data
    with st.expander("📊 View Raw Log Data"):
        st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ parsed_logs.csv not found. Please run parser.py first!")
    st.info("Run: `python parser.py` to generate the parsed logs")