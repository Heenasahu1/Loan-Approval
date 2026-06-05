"""
Utility functions for the Loan Approval Dashboard
This module contains helper functions used across the application
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Dict, List

def load_and_preprocess_data(filepath: str) -> pd.DataFrame:
    """
    Load and perform initial preprocessing on the loan data
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        Preprocessed DataFrame
    """
    df = pd.read_csv(filepath)
    
    # Handle missing values
    df = df.fillna(df.median(numeric_only=True))
    
    # Fix any typos in column names
    if 'Home Onwership' in df.columns:
        # Keep as is, dataset has this typo
        pass
    
    return df

def encode_categorical_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Encode categorical features in the dataset
    
    Args:
        df: Input DataFrame
        
    Returns:
        Tuple of (encoded DataFrame, dictionary of LabelEncoders)
    """
    data = df.copy()
    label_encoders = {}
    
    categorical_columns = ['Gender', 'Education', 'Home Onwership', 'Loan Intent', 'Previous Loan']
    
    for col in categorical_columns:
        if col in data.columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col].astype(str))
            label_encoders[col] = le
    
    return data, label_encoders

def calculate_approval_rate(df: pd.DataFrame, group_by: str = None) -> Dict:
    """
    Calculate approval rates
    
    Args:
        df: Input DataFrame
        group_by: Column to group by (optional)
        
    Returns:
        Dictionary with approval rate statistics
    """
    if group_by is None:
        total = len(df)
        approved = (df['Loan Status'] == 1).sum()
        return {
            'total': total,
            'approved': approved,
            'rejected': total - approved,
            'approval_rate': approved / total * 100
        }
    else:
        rates = {}
        for group in df[group_by].unique():
            group_df = df[df[group_by] == group]
            total = len(group_df)
            approved = (group_df['Loan Status'] == 1).sum()
            rates[group] = {
                'total': total,
                'approved': approved,
                'approval_rate': approved / total * 100 if total > 0 else 0
            }
        return rates

def calculate_debt_to_income_ratio(income: float, loan_amount: float) -> float:
    """
    Calculate debt-to-income ratio
    
    Args:
        income: Annual income
        loan_amount: Loan amount
        
    Returns:
        Debt-to-income ratio as percentage
    """
    if income == 0:
        return 0
    return (loan_amount / income) * 100

def estimate_interest_rate(credit_score: int, annual_income: float) -> float:
    """
    Estimate loan interest rate based on credit score and income
    
    Args:
        credit_score: Applicant's credit score
        annual_income: Annual income
        
    Returns:
        Estimated interest rate percentage
    """
    # Base rate by credit score
    if credit_score < 580:
        base_rate = 20.0
    elif credit_score < 670:
        base_rate = 15.0
    elif credit_score < 740:
        base_rate = 10.0
    else:
        base_rate = 7.0
    
    # Adjust based on income (higher income = lower rate)
    income_adjustment = -0.05 * (annual_income / 100000) if annual_income > 0 else 0
    
    final_rate = max(base_rate + income_adjustment, 5.0)
    
    return round(final_rate, 2)

def get_credit_rating(credit_score: int) -> str:
    """
    Get credit rating based on credit score
    
    Args:
        credit_score: Applicant's credit score
        
    Returns:
        Credit rating string
    """
    if credit_score < 580:
        return "Poor"
    elif credit_score < 670:
        return "Fair"
    elif credit_score < 740:
        return "Good"
    elif credit_score < 800:
        return "Very Good"
    else:
        return "Excellent"

def get_income_category(income: float) -> str:
    """
    Categorize income level
    
    Args:
        income: Annual income
        
    Returns:
        Income category string
    """
    if income < 25000:
        return "Low Income"
    elif income < 50000:
        return "Lower-Middle Income"
    elif income < 75000:
        return "Middle Income"
    elif income < 100000:
        return "Upper-Middle Income"
    else:
        return "High Income"

def validate_input(data: Dict) -> Tuple[bool, str]:
    """
    Validate user input for loan prediction
    
    Args:
        data: Dictionary of input values
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate age
    if data.get('Age', 0) < 18 or data.get('Age', 0) > 120:
        return False, "Age must be between 18 and 120"
    
    # Validate income
    if data.get('Person Income', 0) < 0:
        return False, "Income cannot be negative"
    
    # Validate loan amount
    if data.get('Loan Amount', 0) < 0:
        return False, "Loan amount cannot be negative"
    
    # Validate credit score
    credit_score = data.get('Credit Score', 0)
    if credit_score < 300 or credit_score > 850:
        return False, "Credit score must be between 300 and 850"
    
    # Validate employment experience
    experience = data.get('Employee Experience', 0)
    if experience < 0 or experience > 100:
        return False, "Employment experience must be between 0 and 100 years"
    
    return True, "Input is valid"

def get_recommendations(data: Dict, prediction: int, probability: np.ndarray) -> List[str]:
    """
    Generate personalized recommendations based on applicant data and prediction
    
    Args:
        data: Dictionary of applicant data
        prediction: Loan approval prediction (0 or 1)
        probability: Prediction probability array
        
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Credit score recommendations
    if data.get('Credit Score', 0) < 650:
        recommendations.append("⚠️ Work on improving your credit score to increase approval chances")
    
    # Debt-to-income ratio recommendations
    dti_ratio = calculate_debt_to_income_ratio(
        data.get('Person Income', 1),
        data.get('Loan Amount', 0)
    )
    if dti_ratio > 50:
        recommendations.append("⚠️ Consider reducing the loan amount relative to your income")
    
    # Employment experience recommendations
    if data.get('Employee Experience', 0) < 2:
        recommendations.append("⚠️ Building more employment history will strengthen your application")
    
    # Income recommendations
    if data.get('Person Income', 0) < 30000:
        recommendations.append("💡 Improving your income will increase approval probability")
    
    # If approved, add positive recommendations
    if prediction == 1:
        recommendations.insert(0, "✅ Your financial profile looks good for loan approval!")
    else:
        # If rejected, suggest improvements
        if len(recommendations) == 0:
            recommendations.append("💡 Try improving your credit score or reducing the loan amount")
    
    return recommendations if recommendations else ["✅ Application submitted for review"]

def format_currency(amount: float) -> str:
    """
    Format a number as currency
    
    Args:
        amount: Numeric amount
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"

def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a number as percentage
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"

def get_feature_importance_interpretation(feature_name: str, importance: float) -> str:
    """
    Get a human-readable interpretation of feature importance
    
    Args:
        feature_name: Name of the feature
        importance: Importance value
        
    Returns:
        Interpretation string
    """
    if importance > 0.15:
        impact = "Very High"
    elif importance > 0.10:
        impact = "High"
    elif importance > 0.05:
        impact = "Medium"
    else:
        impact = "Low"
    
    return f"{feature_name} has {impact} impact on approval decisions"

def create_applicant_profile(data: Dict) -> Dict:
    """
    Create a comprehensive applicant profile
    
    Args:
        data: Applicant data dictionary
        
    Returns:
        Dictionary with profile information
    """
    profile = {
        'age': data.get('Age'),
        'gender': data.get('Gender'),
        'education': data.get('Education'),
        'income': data.get('Person Income'),
        'income_category': get_income_category(data.get('Person Income', 0)),
        'experience': data.get('Employee Experience'),
        'credit_score': data.get('Credit Score'),
        'credit_rating': get_credit_rating(data.get('Credit Score', 0)),
        'loan_amount': data.get('Loan Amount'),
        'dti_ratio': calculate_debt_to_income_ratio(
            data.get('Person Income', 0),
            data.get('Loan Amount', 0)
        ),
        'estimated_rate': estimate_interest_rate(
            data.get('Credit Score', 0),
            data.get('Person Income', 0)
        ),
        'home_ownership': data.get('Home Onwership'),
        'loan_intent': data.get('Loan Intent'),
        'previous_loan': data.get('Previous Loan')
    }
    
    return profile

def compare_to_dataset(data: Dict, df: pd.DataFrame) -> Dict:
    """
    Compare applicant data to dataset averages
    
    Args:
        data: Applicant data dictionary
        df: Reference dataset
        
    Returns:
        Dictionary with comparison statistics
    """
    approved_df = df[df['Loan Status'] == 1]
    
    comparison = {
        'age': {
            'applicant': data.get('Age'),
            'avg_approved': approved_df['Age'].mean(),
            'vs_approved': 'Above' if data.get('Age', 0) > approved_df['Age'].mean() else 'Below'
        },
        'income': {
            'applicant': data.get('Person Income'),
            'avg_approved': approved_df['Person Income'].mean(),
            'vs_approved': 'Above' if data.get('Person Income', 0) > approved_df['Person Income'].mean() else 'Below'
        },
        'credit_score': {
            'applicant': data.get('Credit Score'),
            'avg_approved': approved_df['Credit Score'].mean(),
            'vs_approved': 'Above' if data.get('Credit Score', 0) > approved_df['Credit Score'].mean() else 'Below'
        },
        'loan_amount': {
            'applicant': data.get('Loan Amount'),
            'avg_approved': approved_df['Loan Amount'].mean(),
            'vs_approved': 'Below' if data.get('Loan Amount', 0) < approved_df['Loan Amount'].mean() else 'Above'
        }
    }
    
    return comparison

# Export all functions
__all__ = [
    'load_and_preprocess_data',
    'encode_categorical_features',
    'calculate_approval_rate',
    'calculate_debt_to_income_ratio',
    'estimate_interest_rate',
    'get_credit_rating',
    'get_income_category',
    'validate_input',
    'get_recommendations',
    'format_currency',
    'format_percentage',
    'get_feature_importance_interpretation',
    'create_applicant_profile',
    'compare_to_dataset'
]
