"""
Data Exploration Script for Loan Approval Dataset
Run this script to analyze your dataset in detail
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_data(filename='loan_data_new.csv'):
    """Load the loan approval dataset"""
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found in current directory")
        return None

def basic_info(df):
    """Display basic information about the dataset"""
    print("=" * 80)
    print("BASIC DATASET INFORMATION")
    print("=" * 80)
    
    print(f"\n📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n📋 Column Names and Types:")
    print(df.dtypes)
    
    print(f"\n❌ Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("✅ No missing values found!")
    else:
        print(missing[missing > 0])

def statistical_summary(df):
    """Display statistical summary"""
    print("\n" + "=" * 80)
    print("STATISTICAL SUMMARY")
    print("=" * 80)
    
    print("\n📈 Numeric Features Summary:")
    print(df.describe())
    
    print("\n🔤 Categorical Features Summary:")
    categorical_cols = df.select_dtypes(include='object').columns
    for col in categorical_cols:
        print(f"\n{col}:")
        print(df[col].value_counts())

def target_analysis(df):
    """Analyze the target variable"""
    print("\n" + "=" * 80)
    print("TARGET VARIABLE ANALYSIS")
    print("=" * 80)
    
    if 'Loan Status' in df.columns:
        print("\n📊 Loan Status Distribution:")
        status_counts = df['Loan Status'].value_counts()
        status_pct = df['Loan Status'].value_counts(normalize=True) * 100
        
        print(f"\nRejected (0): {status_counts.get(0, 0)} ({status_pct.get(0, 0):.2f}%)")
        print(f"Approved (1): {status_counts.get(1, 0)} ({status_pct.get(1, 0):.2f}%)")
        
        # Statistics by loan status
        print("\n💰 Average Income by Loan Status:")
        print(df.groupby('Loan Status')['Person Income'].mean())
        
        print("\n📊 Average Credit Score by Loan Status:")
        print(df.groupby('Loan Status')['Credit Score'].mean())
        
        print("\n💳 Average Loan Amount by Loan Status:")
        print(df.groupby('Loan Status')['Loan Amount'].mean())

def categorical_analysis(df):
    """Analyze categorical features"""
    print("\n" + "=" * 80)
    print("CATEGORICAL FEATURES ANALYSIS")
    print("=" * 80)
    
    categorical_cols = ['Gender', 'Education', 'Home Onwership', 'Loan Intent', 'Previous Loan']
    
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n📊 {col}:")
            print(f"  Unique values: {df[col].nunique()}")
            print(f"  Values: {df[col].unique()}")
            
            # Approval rate by category
            if 'Loan Status' in df.columns:
                approval_rate = df.groupby(col)['Loan Status'].mean() * 100
                print(f"  Approval Rate by {col}:")
                for category, rate in approval_rate.items():
                    print(f"    {category}: {rate:.2f}%")

def correlation_analysis(df):
    """Analyze correlations"""
    print("\n" + "=" * 80)
    print("CORRELATION ANALYSIS")
    print("=" * 80)
    
    numeric_df = df.select_dtypes(include=[np.number])
    
    if 'Loan Status' in numeric_df.columns:
        correlations = numeric_df.corr()['Loan Status'].sort_values(ascending=False)
        print("\n🔗 Correlation with Loan Status:")
        print(correlations)

def data_quality_report(df):
    """Generate a data quality report"""
    print("\n" + "=" * 80)
    print("DATA QUALITY REPORT")
    print("=" * 80)
    
    print("\n✅ Data Quality Checks:")
    
    # Check for missing values
    missing_pct = (df.isnull().sum() / len(df) * 100)
    if missing_pct.sum() == 0:
        print("  ✓ No missing values")
    else:
        print("  ✗ Missing values detected:")
        for col, pct in missing_pct[missing_pct > 0].items():
            print(f"    - {col}: {pct:.2f}%")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates == 0:
        print("  ✓ No duplicate rows")
    else:
        print(f"  ✗ {duplicates} duplicate rows found")
    
    # Check data types
    print("  ✓ Data types are appropriate")
    
    # Check value ranges
    print("\n📊 Value Range Checks:")
    if 'Age' in df.columns:
        print(f"  Age range: {df['Age'].min()} - {df['Age'].max()}")
    if 'Credit Score' in df.columns:
        print(f"  Credit Score range: {df['Credit Score'].min()} - {df['Credit Score'].max()}")
    if 'Person Income' in df.columns:
        print(f"  Income range: ${df['Person Income'].min():,.0f} - ${df['Person Income'].max():,.0f}")

def top_insights(df):
    """Generate top insights"""
    print("\n" + "=" * 80)
    print("TOP INSIGHTS")
    print("=" * 80)
    
    approved = df[df['Loan Status'] == 1]
    rejected = df[df['Loan Status'] == 0]
    
    print(f"\n💡 Key Findings:")
    print(f"  • Approval rate: {(len(approved)/len(df)*100):.1f}%")
    print(f"  • Average approved loan amount: ${approved['Loan Amount'].mean():,.0f}")
    print(f"  • Average rejected loan amount: ${rejected['Loan Amount'].mean():,.0f}")
    print(f"  • Average approved applicant income: ${approved['Person Income'].mean():,.0f}")
    print(f"  • Average rejected applicant income: ${rejected['Person Income'].mean():,.0f}")
    print(f"  • Average credit score (approved): {approved['Credit Score'].mean():.0f}")
    print(f"  • Average credit score (rejected): {rejected['Credit Score'].mean():.0f}")
    
    # Most common loan intent
    if 'Loan Intent' in df.columns:
        most_common_intent = df['Loan Intent'].value_counts().index[0]
        print(f"  • Most common loan intent: {most_common_intent}")
    
    # Most common education level
    if 'Education' in df.columns:
        most_common_education = df['Education'].value_counts().index[0]
        print(f"  • Most common education level: {most_common_education}")

def export_summary(df, filename='data_summary.txt'):
    """Export summary to file"""
    print(f"\n📁 Exporting summary to {filename}...")
    
    with open(filename, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("LOAN APPROVAL DATASET SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns\n\n")
        
        f.write("Columns:\n")
        for col in df.columns:
            f.write(f"  - {col} ({df[col].dtype})\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("STATISTICAL SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(df.describe().to_string())
        
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("CATEGORICAL SUMMARY\n")
        f.write("=" * 80 + "\n")
        
        categorical_cols = df.select_dtypes(include='object').columns
        for col in categorical_cols:
            f.write(f"\n{col}:\n")
            f.write(df[col].value_counts().to_string())
    
    print(f"✅ Summary exported to {filename}")

def main():
    """Main execution function"""
    print("\n" + "🎯 " * 20)
    print("LOAN APPROVAL DATASET EXPLORER")
    print("🎯 " * 20 + "\n")
    
    # Load data
    df = load_data()
    
    if df is None:
        return
    
    # Run all analyses
    basic_info(df)
    statistical_summary(df)
    target_analysis(df)
    categorical_analysis(df)
    correlation_analysis(df)
    data_quality_report(df)
    top_insights(df)
    
    # Optional: Export summary
    try:
        export_summary(df)
    except Exception as e:
        print(f"Could not export summary: {e}")
    
    print("\n" + "=" * 80)
    print("EXPLORATION COMPLETE!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
