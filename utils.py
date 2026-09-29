import pandas as pd
import numpy as np

def load_data(file):
    """Loads CSV data into a Pandas DataFrame."""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        return pd.DataFrame()

def preprocess_data(df):
    """Handles missing values and basic preprocessing."""
    if df.empty:
        return df
        
    df = df.copy()
    
    # Fill numeric columns with median, categorical with mode
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
            
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
            
    return df
    
def get_insights(df):
    """Generates automated insights based on real data columns."""
    insights = []
    
    if df.empty:
        return ["No data available to generate insights."]
        
    if 'Class' in df.columns:
        most_common_class = df['Class'].mode()[0]
        class_pct = (df['Class'] == most_common_class).mean() * 100
        insights.append(f"Most common travel class is **{most_common_class}** ({class_pct:.1f}% of passengers).")
        
    if 'Customer Type' in df.columns:
        most_common_cust = df['Customer Type'].mode()[0]
        cust_pct = (df['Customer Type'] == most_common_cust).mean() * 100
        insights.append(f"Majority customer type is **{most_common_cust}** ({cust_pct:.1f}%).")
        
    if 'Flight Distance' in df.columns:
        avg_distance = df['Flight Distance'].mean()
        insights.append(f"Average flight distance is **{avg_distance:.0f} miles**.")
        
    if 'Satisfaction' in df.columns:
        satisfied_pct = (df['Satisfaction'] == 'Satisfied').mean() * 100
        insights.append(f"**{satisfied_pct:.1f}%** of passengers are Satisfied.")
        
    return insights
