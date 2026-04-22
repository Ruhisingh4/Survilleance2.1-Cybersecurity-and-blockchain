import pandas as pd

def validate_data(df):
    """
    Validates input data for the surveillance system.
    Handles missing values and basic ID formatting.
    """
    df = df.copy()
    
    # Drop rows with missing ID
    df = df.dropna(subset=['ID_Code'])
    
    # Ensure ID starts with 'ID' (basic sanitization)
    df['ID_Code'] = df['ID_Code'].astype(str).str.strip().str.upper()
    df['valid_format'] = df['ID_Code'].str.startswith('ID')
    
    # Fill missing Attempts with 0
    df['Attempts'] = df['Attempts'].fillna(0).astype(int)
    
    return df
