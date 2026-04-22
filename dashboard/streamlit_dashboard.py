import streamlit as st
import pandas as pd
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import json
import pdfplumber

# Ensure app package is accessible
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)
from app.main import run_pipeline

st.set_page_config(page_title="CyberSec Surveillance", page_icon="🛡️", layout="wide")

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stMetric {
        background-color: #1e212b;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #333;
    }
    h1, h2, h3 {
        color: #4da6ff !important;
    }
    .upload-box {
        border: 2px dashed #4da6ff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        background-color: #1a1c23;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Digital Cybersecurity Surveillance System")
st.markdown("**Real-time monitoring of ID code usage, anomaly detection, and graph-based suspicious relationship analysis.**")

st.sidebar.header("📁 Data Input")
st.sidebar.markdown("Upload your access logs here. Supported formats: CSV, JSON, PDF")

uploaded_file = st.sidebar.file_uploader("Upload Data File", type=['csv', 'json', 'pdf'])

def parse_uploaded_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.json'):
        return pd.read_json(file)
    elif file.name.endswith('.pdf'):
        # Attempt to extract table from PDF
        try:
            with pdfplumber.open(file) as pdf:
                all_data = []
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        all_data.extend(table[1:]) # skip headers of subsequent pages maybe, but let's assume one table
                        if not all_data:
                            all_data = table # first page
                if all_data:
                    # Assume first row is header
                    df = pd.DataFrame(all_data[1:], columns=all_data[0])
                    return df
        except Exception as e:
            st.error(f"Error parsing PDF: {e}")
            return None
    return None

df_input = None

if uploaded_file is not None:
    df_input = parse_uploaded_file(uploaded_file)
    if df_input is not None:
        st.sidebar.success("File uploaded successfully!")
else:
    # Use default sample data if no file uploaded
    st.sidebar.info("Using default sample dataset.")
    csv_path = os.path.join(base_dir, "data", "access_logs.csv")
    if os.path.exists(csv_path):
        df_input = pd.read_csv(csv_path)

if df_input is not None:
    outputs_dir = os.path.join(base_dir, "outputs")
    
    with st.spinner('Analyzing Surveillance Data...'):
        df, G, df_suspicious = run_pipeline(df_input, outputs_dir)
    
    # Top Metrics
    total_logs = len(df)
    flagged = len(df[df['Decision'] == 'Flag'])
    blocked = len(df[df['Decision'] == 'Block'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Logs", total_logs)
    col2.metric("Flagged Entries", flagged, delta_color="inverse")
    col3.metric("Blocked Entries", blocked, delta_color="inverse")
    col4.metric("Suspicious Nodes", len(df_suspicious), delta_color="inverse")
    
    st.divider()
    
    # Layout
    tab1, tab2, tab3 = st.tabs(["📋 Detailed Logs", "🕸️ Behavior Graph", "🚨 Alerts & Suspicious Nodes"])
    
    with tab1:
        st.subheader("Comprehensive Surveillance Results")
        st.dataframe(
            df[['ID_Code', 'User', 'Time', 'Attempts', 'Risk_Level', 'Decision', 'Reason']], 
            use_container_width=True,
            height=400
        )
        
    with tab2:
        st.subheader("Entity Relationship Analysis")
        st.markdown("Visualizing the connections between Users, IDs, and Devices.")
        col_g1, col_g2 = st.columns([7, 3])
        with col_g1:
            fig, ax = plt.subplots(figsize=(8, 6))
            # Set background color of the plot
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')
            
            pos = nx.spring_layout(G, seed=42)
            
            # Draw nodes and edges with custom colors for dark mode
            nx.draw_networkx_nodes(G, pos, node_color='#4da6ff', node_size=1000, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='#555555', ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=9, font_color='white', font_weight='bold', ax=ax)
            
            ax.axis('off')
            st.pyplot(fig)
        with col_g2:
            st.info("Graph represents usage patterns. Nodes with excessive connections often indicate compromised credentials or shared accounts.")
        
    with tab3:
        st.subheader("High-Priority Alerts")
        st.markdown("Logs that were **Flagged** or **Blocked** by the Decision Engine.")
        flagged_df = df[df['Decision'] != 'Allow']
        
        if not flagged_df.empty:
            st.dataframe(flagged_df, use_container_width=True)
            
            # Download option
            st.download_button(
                label="📥 Download Flagged Logs (CSV)",
                data=flagged_df.to_csv(index=False).encode('utf-8'),
                file_name='flagged_logs.csv',
                mime='text/csv',
                help="Export the flagged and blocked entries for external auditing."
            )
        else:
            st.success("No anomalies detected. System is secure.")
            
        st.subheader("Suspicious Entities Detected")
        if not df_suspicious.empty:
            st.warning("The following nodes exhibit highly abnormal connection counts:")
            st.dataframe(df_suspicious, use_container_width=True)
        else:
            st.success("No suspicious cross-entity behavior found.")
else:
    st.error("No data available to analyze.")
