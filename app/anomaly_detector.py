def detect_anomalies(df, max_attempts=5):
    """
    Detects behavioral anomalies.
    Flags entries where attempts exceed the maximum threshold.
    """
    df = df.copy()
    
    # Threshold check
    df['is_anomaly'] = df['Attempts'] > max_attempts
    
    return df
