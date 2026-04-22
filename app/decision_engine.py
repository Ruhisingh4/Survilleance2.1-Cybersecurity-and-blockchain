def assign_risk_score(row):
    """
    Assigns Risk Score based on behavior.
    """
    if row['is_anomaly']:
        if row['Attempts'] > 8:
            return 'High', 'Block'
        return 'Medium', 'Flag'
    
    return 'Low', 'Allow'

def process_decisions(df):
    """
    Applies the decision engine logic to the dataframe.
    """
    df = df.copy()
    
    risks = []
    decisions = []
    reasons = []
    
    for _, row in df.iterrows():
        risk, decision = assign_risk_score(row)
        
        reason = "Normal activity"
        if risk == 'High':
            reason = f"Extreme attempts ({row['Attempts']})"
        elif risk == 'Medium':
            reason = f"Suspicious attempts ({row['Attempts']})"
            
        risks.append(risk)
        decisions.append(decision)
        reasons.append(reason)
        
    df['Risk_Level'] = risks
    df['Decision'] = decisions
    df['Reason'] = reasons
    
    return df
