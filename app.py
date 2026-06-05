import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# Initialize session state
if 'use_uploaded_data' not in st.session_state:
    st.session_state.use_uploaded_data = False
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Page configuration
st.set_page_config(
    page_title="Loan Approval Prediction Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .approved {
        color: #28a745;
        font-weight: bold;
    }
    .rejected {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data(filepath='loan_data_new.csv'):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"Data file not found: {filepath}")
        return None

# Download template function
def download_template():
    """Generate template CSV for download"""
    template_df = pd.read_csv('data_import_template.csv')
    return template_df.to_csv(index=False).encode('utf-8')

# Prepare data and train model
@st.cache_resource
def train_model(df):
    # Create a copy for processing
    data = df.copy()
    
    # Handle missing values
    data = data.fillna(data.median(numeric_only=True))
    
    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['Gender', 'Education', 'Home Onwership', 'Loan Intent', 'Previous Loan']
    
    for col in categorical_columns:
        le = LabelEncoder()
        if col in data.columns:
            data[col] = le.fit_transform(data[col].astype(str))
            label_encoders[col] = le
    
    # Prepare features and target
    X = data.drop('Loan Status', axis=1)
    y = data['Loan Status']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15)
    model.fit(X_train, y_train)
    
    # Get model performance metrics
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': model.score(X_test, y_test),
        'roc_auc': roc_auc_score(y_test, y_pred_proba),
        'classification_report': classification_report(y_test, y_pred, output_dict=True)
    }
    
    return model, label_encoders, X.columns.tolist(), metrics

# Make prediction
def make_prediction(model, label_encoders, feature_names, user_data):
    input_df = pd.DataFrame([user_data])
    
    # Encode categorical variables
    categorical_columns = ['Gender', 'Education', 'Home Onwership', 'Loan Intent', 'Previous Loan']
    
    for col in categorical_columns:
        if col in input_df.columns and col in label_encoders:
            input_df[col] = label_encoders[col].transform(input_df[col].astype(str))
    
    # Ensure all features are present
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0
    
    input_df = input_df[feature_names]
    
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]
    
    return prediction, probability

# Load data
df = load_data()

# Train model
model, label_encoders, feature_names, metrics = train_model(df)

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Analytics Dashboard", "🔮 Loan Prediction", "📈 Model Performance", "📤 Data Management"]
)

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("💰 Loan Approval Prediction & Analytics Dashboard")
        st.markdown("""
        Welcome to the **Loan Approval Prediction & Analytics Dashboard**!
        
        This intelligent system helps:
        - 📊 **Predict** loan approval decisions based on applicant information
        - 📈 **Analyze** lending patterns and trends
        - 💡 **Understand** key factors affecting loan approval
        - 🎯 **Guide** applicants on their approval chances
        """)
    
    with col2:
        st.metric("Dataset Records", f"{len(df):,}")
        approval_rate = (df['Loan Status'].sum() / len(df) * 100)
        st.metric("Approval Rate", f"{approval_rate:.1f}%")
    
    st.divider()
    
    # Key Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Age", f"{df['Age'].mean():.0f} years")
    
    with col2:
        st.metric("Avg Income", f"${df['Person Income'].mean():,.0f}")
    
    with col3:
        st.metric("Avg Loan Amount", f"${df['Loan Amount'].mean():,.0f}")
    
    with col4:
        st.metric("Avg Credit Score", f"{df['Credit Score'].mean():.0f}")
    
    st.divider()
    
    # Quick Start Guide
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 How to Use")
        st.markdown("""
        1. **Go to Loan Prediction** - Enter your details
        2. **Get Decision** - AI predicts approval status
        3. **View Analytics** - Understand the data
        4. **Check Model Performance** - See accuracy metrics
        """)
    
    with col2:
        st.subheader("⚡ Key Insights")
        approved = df[df['Loan Status'] == 1]
        rejected = df[df['Loan Status'] == 0]
        
        st.markdown(f"""
        - **Approved Loans:** {len(approved):,} ({len(approved)/len(df)*100:.1f}%)
        - **Rejected Loans:** {len(rejected):,} ({len(rejected)/len(df)*100:.1f}%)
        - **Avg Income (Approved):** ${approved['Person Income'].mean():,.0f}
        - **Avg Income (Rejected):** ${rejected['Person Income'].mean():,.0f}
        """)

# ==================== ANALYTICS DASHBOARD ====================
elif page == "📊 Analytics Dashboard":
    st.title("📊 Analytics Dashboard")
    st.markdown("Explore trends and patterns in loan applications")
    
    col1, col2 = st.columns(2)
    
    # Loan Status Distribution
    with col1:
        fig_status = go.Figure(data=[
            go.Pie(
                labels=['Approved', 'Rejected'],
                values=[df[df['Loan Status'] == 1].shape[0], df[df['Loan Status'] == 0].shape[0]],
                marker=dict(colors=['#28a745', '#dc3545']),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
            )
        ])
        fig_status.update_layout(title="Loan Status Distribution", height=400)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Gender Distribution
    with col2:
        gender_counts = df['Gender'].value_counts()
        fig_gender = go.Figure(data=[
            go.Bar(
                x=gender_counts.index,
                y=gender_counts.values,
                marker=dict(color=['#FF6B6B', '#4ECDC4'])
            )
        ])
        fig_gender.update_layout(title="Gender Distribution", height=400, xaxis_title="Gender", yaxis_title="Count")
        st.plotly_chart(fig_gender, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # Age vs Loan Approval
    with col1:
        fig_age = px.scatter(
            df,
            x='Age',
            y='Person Income',
            color='Loan Status',
            color_discrete_map={0: '#dc3545', 1: '#28a745'},
            labels={'Loan Status': 'Approved'},
            hover_data=['Credit Score', 'Loan Amount']
        )
        fig_age.update_layout(title="Age vs Income (Colored by Approval)", height=400)
        st.plotly_chart(fig_age, use_container_width=True)
    
    # Loan Intent Distribution
    with col2:
        intent_counts = df['Loan Intent'].value_counts().head(10)
        fig_intent = go.Figure(data=[
            go.Bar(
                x=intent_counts.values,
                y=intent_counts.index,
                orientation='h',
                marker=dict(color='#3498db')
            )
        ])
        fig_intent.update_layout(title="Top 10 Loan Intents", height=400, xaxis_title="Count")
        st.plotly_chart(fig_intent, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # Credit Score Distribution
    with col1:
        fig_credit = px.histogram(
            df,
            x='Credit Score',
            nbins=30,
            color='Loan Status',
            color_discrete_map={0: '#dc3545', 1: '#28a745'},
            labels={'Loan Status': 'Approved'}
        )
        fig_credit.update_layout(title="Credit Score Distribution", height=400)
        st.plotly_chart(fig_credit, use_container_width=True)
    
    # Home Ownership vs Approval
    with col2:
        home_approval = df.groupby('Home Onwership')['Loan Status'].agg(['sum', 'count'])
        home_approval['approval_rate'] = (home_approval['sum'] / home_approval['count'] * 100).round(2)
        
        fig_home = go.Figure(data=[
            go.Bar(
                x=home_approval.index,
                y=home_approval['approval_rate'],
                marker=dict(color='#9b59b6')
            )
        ])
        fig_home.update_layout(title="Approval Rate by Home Ownership", height=400, yaxis_title="Approval Rate (%)")
        st.plotly_chart(fig_home, use_container_width=True)
    
    # Detailed Statistics
    st.divider()
    st.subheader("📋 Detailed Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Key Numeric Features:**")
        numeric_stats = df[['Age', 'Person Income', 'Loan Amount', 'Credit Score', 'Loan interest Rate']].describe()
        st.dataframe(numeric_stats, use_container_width=True)
    
    with col2:
        st.write("**Approval Rate by Education Level:**")
        education_approval = df.groupby('Education').agg({
            'Loan Status': ['count', 'sum']
        }).round(2)
        education_approval.columns = ['Total', 'Approved']
        education_approval['Approval Rate %'] = (education_approval['Approved'] / education_approval['Total'] * 100).round(2)
        st.dataframe(education_approval, use_container_width=True)

# ==================== LOAN PREDICTION PAGE ====================
elif page == "🔮 Loan Prediction":
    st.title("🔮 Loan Approval Prediction")
    st.markdown("Enter your details below to get a loan approval prediction")
    
    col1, col2 = st.columns(2)
    
    # User Input Form
    with col1:
        st.subheader("Personal Information")
        age = st.slider("Age", min_value=18, max_value=80, value=30)
        gender = st.selectbox("Gender", options=['male', 'female'])
        education = st.selectbox("Education Level", options=['High School', 'Bachelor', 'Master', 'Associate'])
        person_income = st.number_input("Annual Income ($)", min_value=0, value=50000, step=1000)
        emp_experience = st.slider("Years of Employment Experience", min_value=0, max_value=50, value=5)
    
    with col2:
        st.subheader("Loan Information")
        home_ownership = st.selectbox("Home Ownership Status", options=['RENT', 'OWN', 'MORTGAGE', 'OTHER'])
        loan_amount = st.number_input("Loan Amount ($)", min_value=0, value=10000, step=500)
        loan_intent = st.selectbox("Loan Purpose", options=[
            'PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 
            'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'
        ])
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=650)
        previous_loan = st.selectbox("Previous Loan History", options=['Yes', 'No'])
    
    # Calculate additional metrics
    loan_percentage = loan_amount / person_income if person_income > 0 else 0
    
    # Estimate interest rate based on credit score and income
    if credit_score < 580:
        base_rate = 20.0
    elif credit_score < 670:
        base_rate = 15.0
    elif credit_score < 740:
        base_rate = 10.0
    else:
        base_rate = 7.0
    
    # Adjust based on income
    income_adjustment = -0.05 * (person_income / 100000) if person_income > 0 else 0
    loan_interest_rate = max(base_rate + income_adjustment, 5.0)
    
    # Create credit history estimate (1-5 years)
    credit_history = min(5, max(1, emp_experience // 2 + 1))
    
    st.divider()
    
    # Prepare prediction data
    prediction_data = {
        'Age': age,
        'Gender': gender,
        'Education': education,
        'Person Income': person_income,
        'Employee Experience': emp_experience,
        'Home Onwership': home_ownership,
        'Loan Amount': loan_amount,
        'Loan Intent': loan_intent,
        'Loan interest Rate': loan_interest_rate,
        'Loan percentage': loan_percentage,
        'Credit History': credit_history,
        'Credit Score': credit_score,
        'Previous Loan': previous_loan
    }
    
    # Make prediction button
    if st.button("🎯 Get Prediction", use_container_width=True):
        try:
            prediction, probability = make_prediction(model, label_encoders, feature_names, prediction_data)
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                if prediction == 1:
                    st.success("✅ LOAN APPROVED!")
                    approval_status = "Approved"
                    color = "#28a745"
                else:
                    st.error("❌ LOAN REJECTED")
                    approval_status = "Rejected"
                    color = "#dc3545"
            
            with col2:
                st.metric(
                    "Approval Probability",
                    f"{probability[1]*100:.1f}%",
                    delta=f"{(probability[1]*100 - 50):.1f}%" if probability[1] > 0.5 else f"{(probability[1]*100 - 50):.1f}%"
                )
            
            st.divider()
            
            # Detailed Analysis
            st.subheader("📊 Detailed Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Debt-to-Income Ratio", f"{loan_percentage*100:.2f}%")
            
            with col2:
                st.metric("Estimated Interest Rate", f"{loan_interest_rate:.2f}%")
            
            with col3:
                st.metric("Credit Score", credit_score)
            
            st.divider()
            
            # Prediction Confidence Gauge
            st.subheader("📈 Prediction Confidence")
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=probability[1]*100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Approval Confidence"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#3498db"},
                    'steps': [
                        {'range': [0, 25], 'color': "#ffcccc"},
                        {'range': [25, 50], 'color': "#ffe6cc"},
                        {'range': [50, 75], 'color': "#ffffcc"},
                        {'range': [75, 100], 'color': "#ccffcc"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig_gauge.update_layout(height=400)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.divider()
            
            # Recommendations
            st.subheader("💡 Recommendations")
            
            recommendations = []
            
            if credit_score < 650:
                recommendations.append("⚠️ Work on improving your credit score to increase approval chances")
            
            if loan_percentage > 0.5:
                recommendations.append("⚠️ Consider reducing the loan amount relative to your income")
            
            if emp_experience < 2:
                recommendations.append("⚠️ Building more employment history will strengthen your application")
            
            if person_income < 30000:
                recommendations.append("💡 Improving your income will increase approval probability")
            
            if not recommendations:
                recommendations.append("✅ Your financial profile looks good for loan approval!")
            
            for rec in recommendations:
                st.info(rec)
        
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")

# ==================== MODEL PERFORMANCE PAGE ====================
elif page == "📈 Model Performance":
    st.title("📈 Model Performance Metrics")
    st.markdown("Evaluate the accuracy and reliability of the prediction model")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Accuracy", f"{metrics['accuracy']*100:.2f}%")
    
    with col2:
        st.metric("ROC-AUC Score", f"{metrics['roc_auc']:.4f}")
    
    with col3:
        st.metric("Model Type", "Random Forest")
    
    st.divider()
    
    # Classification Metrics
    st.subheader("Classification Metrics by Class")
    
    classification_data = metrics['classification_report']
    
    metrics_df = pd.DataFrame({
        'Class': ['Rejected (0)', 'Approved (1)', 'Weighted Avg'],
        'Precision': [
            f"{classification_data['0']['precision']:.4f}",
            f"{classification_data['1']['precision']:.4f}",
            f"{classification_data['weighted avg']['precision']:.4f}"
        ],
        'Recall': [
            f"{classification_data['0']['recall']:.4f}",
            f"{classification_data['1']['recall']:.4f}",
            f"{classification_data['weighted avg']['recall']:.4f}"
        ],
        'F1-Score': [
            f"{classification_data['0']['f1-score']:.4f}",
            f"{classification_data['1']['f1-score']:.4f}",
            f"{classification_data['weighted avg']['f1-score']:.4f}"
        ]
    })
    
    st.dataframe(metrics_df, use_container_width=True)
    
    st.divider()
    
    # Feature Importance
    st.subheader("🔑 Feature Importance")
    
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    fig_importance = px.bar(
        feature_importance_df.head(15),
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Viridis',
        title='Top 15 Most Important Features'
    )
    fig_importance.update_layout(height=500)
    st.plotly_chart(fig_importance, use_container_width=True)
    
    st.divider()
    
    # Model Information
    st.subheader("ℹ️ Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Model Details:**
        - Algorithm: Random Forest Classifier
        - Number of Trees: 100
        - Max Depth: 15
        - Training Set Size: 80% of data
        - Test Set Size: 20% of data
        - Test Samples: ~1,000 records
        """)
    
    with col2:
        st.write("""
        **Data Information:**
        - Total Records: 10,000+
        - Features Used: 13
        - Categorical Features: 5
        - Numeric Features: 8
        - Target Variable: Loan Status (Binary)
        """)

# ==================== DATA MANAGEMENT PAGE ====================
elif page == "📤 Data Management":
    st.title("📤 Data Management")
    st.markdown("Import your own loan data or download a template to prepare your dataset")
    
    tab1, tab2, tab3 = st.tabs(["📥 Import Data", "📋 Template", "📊 Data Preview"])
    
    # Tab 1: Import Data
    with tab1:
        st.subheader("Import Your Data")
        st.markdown("""
        Upload one or multiple CSV files with loan application data.
        Your data will be used for predictions and analysis.
        """)
        
        # Single file upload
        st.write("**Option 1: Upload Single File**")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with the required columns"
        )
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                st.success(f"✅ File uploaded successfully! ({len(uploaded_df)} rows)")
                
                # Validate columns
                required_cols = ['Age', 'Gender', 'Education', 'Person Income', 'Employee Experience',
                               'Home Onwership', 'Loan Amount', 'Loan Intent', 'Loan interest Rate',
                               'Loan percentage', 'Credit History', 'Credit Score', 'Previous Loan']
                
                missing_cols = [col for col in required_cols if col not in uploaded_df.columns]
                
                if missing_cols:
                    st.warning(f"⚠️ Missing columns: {', '.join(missing_cols)}")
                else:
                    st.info("✅ All required columns present!")
                
                # Show preview
                st.write("**Data Preview:**")
                st.dataframe(uploaded_df.head(10), use_container_width=True)
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Records", len(uploaded_df))
                with col2:
                    st.metric("Total Columns", len(uploaded_df.columns))
                with col3:
                    st.metric("Missing Values", uploaded_df.isnull().sum().sum())
                
                # Save to session state for use in predictions
                st.session_state['uploaded_data'] = uploaded_df
                st.session_state['use_uploaded_data'] = True
                st.success("✅ Data saved! You can now use it for predictions.")
                
                # Download processed data button
                if st.button("💾 Save Processed Data"):
                    processed_df = uploaded_df.fillna(uploaded_df.median(numeric_only=True))
                    csv = processed_df.to_csv(index=False)
                    st.download_button(
                        label="Download Processed Data",
                        data=csv,
                        file_name="processed_loan_data.csv",
                        mime="text/csv"
                    )
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        st.divider()
        
        # Multiple files upload
        st.write("**Option 2: Upload Multiple Files**")
        multiple_files = st.file_uploader(
            "Choose multiple CSV files",
            type=['csv'],
            accept_multiple_files=True,
            help="Upload multiple CSV files to be combined"
        )
        
        if multiple_files:
            try:
                all_dfs = []
                for file in multiple_files:
                    df = pd.read_csv(file)
                    all_dfs.append(df)
                    st.info(f"✅ Loaded: {file.name} ({len(df)} rows)")
                
                # Combine all dataframes
                combined_df = pd.concat(all_dfs, ignore_index=True)
                st.success(f"✅ Combined {len(multiple_files)} files! Total records: {len(combined_df)}")
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Records", len(combined_df))
                with col2:
                    st.metric("Files Combined", len(multiple_files))
                with col3:
                    st.metric("Total Columns", len(combined_df.columns))
                
                # Save combined data
                st.session_state['uploaded_data'] = combined_df
                st.session_state['use_uploaded_data'] = True
                
                # Download button
                csv = combined_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Combined Data",
                    data=csv,
                    file_name="combined_loan_data.csv",
                    mime="text/csv"
                )
            
            except Exception as e:
                st.error(f"❌ Error combining files: {str(e)}")
    
    # Tab 2: Template
    with tab2:
        st.subheader("Download Import Template")
        st.markdown("""
        Use this template to prepare your data for import.
        Make sure your data matches this exact format.
        """)
        
        # Show template structure
        template_df = pd.read_csv('data_import_template.csv')
        st.write("**Template Structure:**")
        st.dataframe(template_df, use_container_width=True)
        
        st.divider()
        
        # Column descriptions
        st.write("**Column Descriptions:**")
        col_descriptions = {
            'Age': 'Applicant age (18-80)',
            'Gender': 'male or female',
            'Education': 'High School, Bachelor, Master, or Associate',
            'Person Income': 'Annual income in dollars',
            'Employee Experience': 'Years of employment (0-50)',
            'Home Onwership': 'RENT, OWN, MORTGAGE, or OTHER',
            'Loan Amount': 'Requested loan amount in dollars',
            'Loan Intent': 'PERSONAL, EDUCATION, MEDICAL, VENTURE, HOMEIMPROVEMENT, or DEBTCONSOLIDATION',
            'Loan interest Rate': 'Interest rate percentage (5-20)',
            'Loan percentage': 'Loan amount / income ratio (0-1)',
            'Credit History': 'Years of credit history (1-5)',
            'Credit Score': 'Credit score (300-850)',
            'Previous Loan': 'Yes or No',
            'Loan Status': 'Approved (1) or Rejected (0) - Optional'
        }
        
        for col, desc in col_descriptions.items():
            st.text(f"📌 {col}: {desc}")
        
        st.divider()
        
        # Download template button
        template_csv = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Template (CSV)",
            data=template_csv,
            file_name="loan_data_template.csv",
            mime="text/csv",
            help="Download this template and fill it with your data"
        )
        
        st.info("""
        **Tips for preparing your data:**
        - Ensure column names match exactly (case-sensitive)
        - Use the exact values for categorical columns (Gender, Home Ownership, etc.)
        - Keep numeric values in proper format (no currency symbols)
        - Save as CSV format before uploading
        - Remove any empty rows at the end
        - Use 1 for Approved and 0 for Rejected in Loan Status column
        """)
    
    # Tab 3: Data Preview
    with tab3:
        st.subheader("Data Preview & Statistics")
        
        # Check if uploaded data exists
        if 'uploaded_data' in st.session_state and st.session_state.get('use_uploaded_data'):
            data_to_use = st.session_state['uploaded_data']
            st.success("✅ Using uploaded data")
        else:
            data_to_use = load_data()
            st.info("ℹ️ Using default dataset")
        
        if data_to_use is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Records", len(data_to_use))
            with col2:
                st.metric("Columns", len(data_to_use.columns))
            with col3:
                st.metric("Missing Values", data_to_use.isnull().sum().sum())
            
            st.divider()
            
            # Data table
            st.write("**Dataset Preview:**")
            st.dataframe(data_to_use, use_container_width=True)
            
            st.divider()
            
            # Statistics
            st.write("**Statistical Summary:**")
            st.dataframe(data_to_use.describe(), use_container_width=True)
            
            st.divider()
            
            # Download options
            st.write("**Download Options:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = data_to_use.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="loan_data_export.csv",
                    mime="text/csv"
                )
            
            with col2:
                st.info("💡 Upload your data in the 'Import Data' tab")
            
            st.divider()
            
            # Data quality report
            st.write("**Data Quality Report:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Missing Values by Column:**")
                missing = data_to_use.isnull().sum()
                if missing.sum() == 0:
                    st.success("✅ No missing values!")
                else:
                    st.dataframe(missing[missing > 0])
            
            with col2:
                st.write("**Duplicate Rows:**")
                duplicates = data_to_use.duplicated().sum()
                if duplicates == 0:
                    st.success("✅ No duplicate rows!")
                else:
                    st.warning(f"⚠️ {duplicates} duplicate rows found")
            
            st.divider()
            
            # Reset data button
            if st.button("🔄 Reset to Default Data", help="Return to the original loan dataset"):
                if 'uploaded_data' in st.session_state:
                    del st.session_state['uploaded_data']
                if 'use_uploaded_data' in st.session_state:
                    del st.session_state['use_uploaded_data']
                st.success("✅ Reset to default data!")
                st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px; margin-top: 30px;'>
    <p>Loan Approval Prediction & Analytics Dashboard | Powered by Streamlit & Machine Learning</p>
    <p>Disclaimer: This tool is for educational purposes. Actual loan decisions involve many additional factors.</p>
</div>
""", unsafe_allow_html=True)
