import pandas as pd
import os

def clean_dataset(input_path='data/raw_dataset.csv', output_path='output/cleaned_dataset.csv'):
    """
    Clean dataset with comprehensive error handling and reporting.
    
    Args:
        input_path (str): Path to the raw dataset CSV file
        output_path (str): Path where cleaned dataset will be saved
    """
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Check if input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Load dataset
        print(f"📂 Loading dataset from: {input_path}")
        df = pd.read_csv(input_path)
        print(f"📊 Original dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Check if dataset is empty
        if df.empty:
            print("⚠️  Warning: Dataset is empty")
            return
        
        # Report missing values before cleaning
        missing_info = df.isnull().sum()
        total_missing = missing_info.sum()
        if total_missing > 0:
            print(f"\n🔍 Missing values found:")
            for col, count in missing_info[missing_info > 0].items():
                print(f"   {col}: {count} missing values")
            print(f"   Total missing values: {total_missing}")
        else:
            print("✅ No missing values found")
        
        # Handle missing values with validation
        initial_rows = len(df)
        
        # Option 1: Drop rows with ANY missing values (your original approach)
        df_cleaned = df.dropna()
        
        # Validate that we still have data
        if df_cleaned.empty:
            print("❌ Error: All rows removed due to missing values.")
            print("💡 Suggestion: Consider using imputation instead of removal")
            
            # Alternative: Fill missing values instead of dropping
            print("🔄 Attempting to fill missing values instead...")
            df_cleaned = df.copy()
            
            # Fill numeric columns with mean
            numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mean())
            
            # Fill categorical columns with mode
