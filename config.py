# Configuration file for the Loan Approval Dashboard
# Modify these settings to customize the application

# ============= APPLICATION SETTINGS =============
APP_TITLE = "Loan Approval Prediction & Analytics Dashboard"
APP_ICON = "💰"
APP_LAYOUT = "wide"  # "wide" or "centered"
THEME = "light"  # "light" or "dark"

# ============= MODEL SETTINGS =============
# Random Forest Parameters
RF_N_ESTIMATORS = 100  # Number of trees
RF_MAX_DEPTH = 15  # Maximum tree depth
RF_RANDOM_STATE = 42  # For reproducibility
RF_TEST_SIZE = 0.2  # Test set proportion

# ============= PREDICTION SETTINGS =============
# Interest Rate Calculation
CREDIT_SCORE_THRESHOLDS = {
    'poor': 580,      # Credit score < 580
    'fair': 670,      # 580-670
    'good': 740,      # 670-740
    'excellent': 850  # 740+
}

BASE_INTEREST_RATES = {
    'poor': 20.0,
    'fair': 15.0,
    'good': 10.0,
    'excellent': 7.0
}

INCOME_ADJUSTMENT_RATE = -0.05  # Percentage point reduction per $100k income

# ============= DATA SETTINGS =============
DATA_FILE = "loan_data_new.csv"

# Column names mapping (if you have different column names)
COLUMN_MAPPING = {
    'age': 'Age',
    'gender': 'Gender',
    'education': 'Education',
    'income': 'Person Income',
    'experience': 'Employee Experience',
    'home_ownership': 'Home Onwership',  # Note: This is the actual column name in the dataset
    'loan_amount': 'Loan Amount',
    'loan_intent': 'Loan Intent',
    'interest_rate': 'Loan interest Rate',
    'loan_percentage': 'Loan percentage',
    'credit_history': 'Credit History',
    'credit_score': 'Credit Score',
    'previous_loan': 'Previous Loan',
    'loan_status': 'Loan Status'
}

# ============= UI CUSTOMIZATION =============
# Color scheme
COLOR_APPROVED = "#28a745"  # Green
COLOR_REJECTED = "#dc3545"  # Red
COLOR_PRIMARY = "#3498db"   # Blue
COLOR_SECONDARY = "#9b59b6" # Purple

# ============= FEATURE SETTINGS =============
NUMERIC_FEATURES = [
    'Age',
    'Person Income',
    'Employee Experience',
    'Loan Amount',
    'Loan interest Rate',
    'Loan percentage',
    'Credit History',
    'Credit Score'
]

CATEGORICAL_FEATURES = [
    'Gender',
    'Education',
    'Home Onwership',
    'Loan Intent',
    'Previous Loan'
]

# Education levels
EDUCATION_LEVELS = [
    'High School',
    'Bachelor',
    'Master',
    'Associate'
]

# Home ownership types
HOME_OWNERSHIP_TYPES = [
    'RENT',
    'OWN',
    'MORTGAGE',
    'OTHER'
]

# Loan intents
LOAN_INTENTS = [
    'PERSONAL',
    'EDUCATION',
    'MEDICAL',
    'VENTURE',
    'HOMEIMPROVEMENT',
    'DEBTCONSOLIDATION'
]

# ============= PAGE SETTINGS =============
# Navigation pages
PAGES = {
    '🏠 Home': 'home',
    '📊 Analytics Dashboard': 'analytics',
    '🔮 Loan Prediction': 'prediction',
    '📈 Model Performance': 'performance'
}

# ============= SLIDER DEFAULTS =============
# Default values for prediction form sliders
SLIDER_DEFAULTS = {
    'age': 30,
    'experience': 5,
    'credit_score': 650,
    'loan_amount': 10000,
    'income': 50000
}

# ============= ANALYTICS SETTINGS =============
# Number of top items to display
TOP_N_ITEMS = 10

# Chart heights
CHART_HEIGHT = 400
CHART_HEIGHT_LARGE = 500

# ============= MODEL PERFORMANCE SETTINGS =============
# Number of top features to display
TOP_FEATURES = 15

# ============= RECOMMENDATIONS LOGIC =============
RECOMMENDATION_THRESHOLDS = {
    'poor_credit_score': 650,
    'high_debt_to_income': 0.5,  # 50%
    'low_experience': 2,  # years
    'low_income': 30000
}

# ============= CACHING SETTINGS =============
# Cache data for X seconds
CACHE_DURATION = 3600  # 1 hour

# ============= LOG SETTINGS =============
LOG_LEVEL = "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR"

# ============= ADVANCED SETTINGS =============
# Show advanced metrics on model performance page
SHOW_ADVANCED_METRICS = True

# Show raw data tables
SHOW_RAW_DATA = True

# Maximum rows to display in tables
MAX_TABLE_ROWS = 100
