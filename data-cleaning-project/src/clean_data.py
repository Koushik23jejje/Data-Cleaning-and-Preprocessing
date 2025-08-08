import pandas as pd
import os

def clean_dataset(
    input_path='data/raw_dataset.csv',
    output_path='output/cleaned_dataset.csv',
    handle_missing='drop'
):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        print(f"📂 Loading dataset from: {input_path}")
        df = pd.read_csv(input_path)
        print(f"📊 Original dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        
        if df.empty:
            print("⚠️  Warning: Dataset is empty")
            return
        
        missing_info = df.isnull().sum()
        total_missing = missing_info.sum()
        if total_missing > 0:
            print(f"\n🔍 Missing values found:")
            for col, count in missing_info[missing_info > 0].items():
                print(f"   {col}: {count} missing values")
            print(f"   Total missing values: {total_missing}")
        else:
            print("✅ No missing values found")
        
        if handle_missing == 'drop':
            df_cleaned = df.dropna()
            if df_cleaned.empty:
                print("❌ Error: All rows removed due to missing values when dropping rows.")
                print("💡 Suggestion: Try 'impute' option for handling missing values.")
                return
        elif handle_missing == 'impute':
            df_cleaned = df.copy()
            numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                mean_val = df_cleaned[col].mean()
                df_cleaned.loc[:, col] = df_cleaned[col].fillna(mean_val)
            
            categorical_cols = df_cleaned.select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols:
                mode = df_cleaned[col].mode()
                if not mode.empty:
                    df_cleaned.loc[:, col] = df_cleaned[col].fillna(mode[0])
                else:
                    df_cleaned.loc[:, col] = df_cleaned[col].fillna('Unknown')
        else:
            print(f"⚠️  Warning: Unknown handle_missing option '{handle_missing}'. Using default 'drop'.")
            df_cleaned = df.dropna()
            if df_cleaned.empty:
                print("❌ Error: All rows removed due to missing values when dropping rows.")
                print("💡 Suggestion: Try 'impute' option for handling missing values.")
                return
        
        print(f"\n📊 Cleaned dataset: {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} columns")
        
        df_cleaned.to_csv(output_path, index=False)
        print(f"💾 Cleaned dataset saved to: {output_path}")

    except FileNotFoundError as e:
        print(f"🛑 {e}")
    except pd.errors.EmptyDataError:
        print("🛑 Error: Input CSV is empty or invalid.")
    except PermissionError as e:
        print(f"🛑 Permission error: {e}")
    except Exception as e:
        print(f"🛑 Unexpected error occurred: {e}")
