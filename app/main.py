import pandas as pd
import os
from .validation import validate_data
from .anomaly_detector import detect_anomalies
from .graph_analysis import build_graph, get_suspicious_nodes
from .decision_engine import process_decisions

def run_pipeline(df, output_dir="outputs"):
    # Create output dir if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Validate Data
    df = validate_data(df)
    
    # 3. Detect Anomalies
    df = detect_anomalies(df)
    
    # 4. Graph Analysis
    G = build_graph(df)
    suspicious_nodes = get_suspicious_nodes(G)
    
    # 5. Decisions
    df = process_decisions(df)
    
    # 6. Save Outputs
    flagged_logs = df[df['Decision'] != 'Allow']
    flagged_logs.to_csv(f"{output_dir}/flagged_logs.csv", index=False)
    
    df_suspicious = pd.DataFrame(suspicious_nodes)
    if not df_suspicious.empty:
        df_suspicious.to_csv(f"{output_dir}/suspicious_nodes.csv", index=False)
    
    return df, G, df_suspicious
