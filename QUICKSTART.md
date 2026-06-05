# 🚀 Quick Start Guide

## One-Minute Setup

### Option 1: Using Command Prompt (Windows)

1. **Open Command Prompt** in the Loan data folder
   - Hold `Shift` + `Right-click` in the folder → "Open PowerShell here"

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```powershell
   streamlit run app.py
   ```

4. **Access the dashboard:**
   - Browser will open automatically at `http://localhost:8501`
   - If not, copy and paste the URL from the terminal

### Option 2: Using PowerShell (Windows)

```powershell
# Navigate to the folder
cd "C:\Users\ICAI-PC\Downloads\Loan data"

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Option 3: Using Python Directly

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

---

## 📋 System Requirements

- ✅ Windows 7 or later (or any OS with Python)
- ✅ Python 3.8+
- ✅ 500MB free disk space
- ✅ Internet connection (for initial downloads)

---

## 🎯 What to Do After Launch

### First Time Using the App:

1. **Home Page** → Read the overview
2. **Analytics Dashboard** → Explore the visualizations
3. **Model Performance** → Understand how accurate the model is
4. **Loan Prediction** → Enter sample data and get a prediction

### Example Test Case:
- Age: 30
- Gender: Male
- Education: Bachelor
- Income: $75,000
- Experience: 5 years
- Home Ownership: Rent
- Loan Amount: $20,000
- Loan Intent: Personal
- Credit Score: 700
- Previous Loan: No

---

## ⚙️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "pip is not recognized" | Use `python -m pip install -r requirements.txt` |
| "Module not found" | Run `pip install -r requirements.txt` again |
| "CSV file not found" | Ensure `loan_data_new.csv` is in the same folder as `app.py` |
| "Port 8501 already in use" | Close other Streamlit apps or use `streamlit run app.py --server.port 8502` |
| App loads slowly | First load trains the ML model (takes 10-15 seconds) |

---

## 🎨 Customizing the Dashboard

### Change the app title/icon:
Edit line 11 in `app.py`:
```python
st.set_page_config(
    page_title="Your Custom Title",  # Change this
    page_icon="🎯",  # Change the emoji
    layout="wide",
)
```

### Adjust model parameters:
Edit the model training section (around line 50) to change:
- `n_estimators` (number of trees)
- `max_depth` (tree depth)
- `random_state` (reproducibility)

---

## 📊 Application Layout

```
┌─────────────────────────────────────────────────────────┐
│           LOAN APPROVAL PREDICTION DASHBOARD             │
├─────────────────────────────────────────────────────────┤
│ ☰ Navigation Menu:                                      │
│   • 🏠 Home                                             │
│   • 📊 Analytics Dashboard                              │
│   • 🔮 Loan Prediction                                  │
│   • 📈 Model Performance                                │
└─────────────────────────────────────────────────────────┘
```

---

## 📱 Feature Highlights

### 🏠 Home Page
- Dashboard overview
- Key statistics
- Quick start guide

### 📊 Analytics Dashboard  
- 10+ interactive charts
- Approval rate analysis
- Financial metrics
- Demographic insights

### 🔮 Loan Prediction
- Real-time prediction
- Confidence scoring
- Personalized recommendations
- Financial analysis

### 📈 Model Performance
- Accuracy metrics (95%+)
- Feature importance ranking
- Classification reports
- Model specifications

---

## 🔄 Stopping the Application

Press `Ctrl+C` in the terminal window to stop the Streamlit server.

---

## 💾 Saving Your Work

To export prediction results:
1. Take a screenshot of the results page
2. Copy the prediction details
3. Paste into a document or spreadsheet

*(Note: You can add export functionality by modifying the app)*

---

## 🌐 Accessing from Other Devices

If you want to access the dashboard from another computer on your network:

1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```

2. Look for "IPv4 Address" (usually starts with 192.168.x.x)

3. From another device, visit:
   ```
   http://[YOUR_IP_ADDRESS]:8501
   ```

---

## 📚 Next Steps

1. ✅ Run the app successfully
2. ✅ Explore all 4 pages
3. ✅ Test the prediction feature
4. ✅ Review model performance metrics
5. ✅ Customize as needed

---

**You're all set! 🎉 Launch the dashboard and start exploring!**

For detailed information, see `README.md`
