# 📤 Data Import Guide

## Overview

The **Data Management** feature allows you to:
- ✅ Upload your own loan datasets
- ✅ Import multiple files at once
- ✅ Download a template to prepare your data
- ✅ Preview and validate your data
- ✅ Export processed data

---

## 🚀 Quick Start

### Step 1: Download Template
1. Go to **📤 Data Management** page
2. Click on **📋 Template** tab
3. Click **📥 Download Template (CSV)** button
4. Save the file to your computer

### Step 2: Prepare Your Data
1. Open the template in Excel or a text editor
2. Fill in your loan application data
3. Match the format exactly (column names, data types)
4. Save as CSV format

### Step 3: Upload Your Data
1. Go to **📥 Import Data** tab
2. Choose your CSV file
3. System validates the data automatically
4. Your data is ready to use!

---

## 📋 Template Structure

The template includes the following columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Age | Numeric | Applicant age | 28-45 |
| Gender | Text | Male or Female | male, female |
| Education | Text | Education level | Bachelor, Master, High School, Associate |
| Person Income | Numeric | Annual income ($) | 50000, 85000 |
| Employee Experience | Numeric | Years of employment | 0-50 |
| Home Onwership | Text | Home ownership type | RENT, OWN, MORTGAGE, OTHER |
| Loan Amount | Numeric | Requested loan ($) | 10000, 25000 |
| Loan Intent | Text | Purpose of loan | PERSONAL, EDUCATION, MEDICAL, VENTURE, HOMEIMPROVEMENT, DEBTCONSOLIDATION |
| Loan interest Rate | Numeric | Interest rate (%) | 5.0-20.0 |
| Loan percentage | Numeric | Loan/Income ratio | 0.0-1.0 |
| Credit History | Numeric | Years of credit history | 1-5 |
| Credit Score | Numeric | Credit score | 300-850 |
| Previous Loan | Text | Has previous loan | Yes, No |
| Loan Status | Numeric | Approved (1) or Rejected (0) | 0 or 1 (Optional) |

---

## 📤 Upload Options

### Single File Upload
- Upload one CSV file at a time
- Automatic validation of required columns
- Instant preview of data
- Perfect for small datasets

**Steps:**
1. Click file uploader in "Import Data" tab
2. Select your CSV file
3. System validates automatically
4. Review the preview
5. Data is saved for use in predictions

### Multiple File Upload
- Upload several CSV files at once
- Automatically combined into one dataset
- Perfect for batch imports or distributed data

**Steps:**
1. Hold `Ctrl` (or `Cmd` on Mac) and click multiple files
2. Click "Upload" button
3. System combines all files
4. Download combined data if needed

---

## ✅ Data Validation

The system automatically checks for:

### Required Columns
All of these columns must be present (case-sensitive):
```
Age, Gender, Education, Person Income, Employee Experience,
Home Onwership, Loan Amount, Loan Intent, Loan interest Rate,
Loan percentage, Credit History, Credit Score, Previous Loan
```

### Data Quality
- ✅ No missing critical values
- ✅ Correct data types
- ✅ Value ranges within acceptable limits
- ✅ No duplicate records (warning only)

### Validation Messages
- 🟢 **Green** (Success) - Data is valid and ready
- 🟡 **Yellow** (Warning) - Minor issues (duplicates, empty rows)
- 🔴 **Red** (Error) - Critical issues that prevent use

---

## 📝 Data Preparation Tips

### 1. Column Names
- **MUST match exactly** (case-sensitive)
- Do NOT rename columns
- Keep original spelling (including typos in "Home Onwership")

### 2. Categorical Values
Use EXACT text values:
- **Gender:** `male` or `female` (lowercase)
- **Education:** `High School`, `Bachelor`, `Master`, or `Associate`
- **Home Onwership:** `RENT`, `OWN`, `MORTGAGE`, or `OTHER` (uppercase)
- **Loan Intent:** `PERSONAL`, `EDUCATION`, `MEDICAL`, `VENTURE`, `HOMEIMPROVEMENT`, or `DEBTCONSOLIDATION` (uppercase)
- **Previous Loan:** `Yes` or `No` (capitalized)

### 3. Numeric Values
- **Age:** 18-80 years
- **Person Income:** Dollar amounts (no commas or currency symbols)
- **Employee Experience:** 0-50 years
- **Loan Amount:** Dollar amounts
- **Loan interest Rate:** 5.0-20.0 (percentage as decimal)
- **Loan percentage:** 0.0-1.0 (ratio, not percentage)
- **Credit History:** 1-5 years
- **Credit Score:** 300-850
- **Loan Status:** 0 (Rejected) or 1 (Approved) - Optional

### 4. Format Issues to Avoid
❌ Don't use: `$50,000` → Use: `50000`
❌ Don't use: `12.5%` → Use: `12.5`
❌ Don't use: `MALE` → Use: `male`
❌ Don't use: Extra spaces or symbols

### 5. Empty Rows
- Remove completely empty rows at the end
- Remove rows with all missing values
- Keep header row at the top

---

## 📊 Using Your Data

### In Predictions
1. Upload your data in **Data Management**
2. Go to **🔮 Loan Prediction**
3. The system uses your uploaded data for training the model
4. Make predictions on new applicants

### In Analytics
1. Upload your data
2. Go to **📊 Analytics Dashboard**
3. All visualizations use your data
4. See trends specific to your dataset

### In Model Performance
1. Upload your data
2. Go to **📈 Model Performance**
3. Model metrics are calculated on your data
4. Feature importance based on your dataset

---

## 💾 Exporting Data

### Export Processed Data
- Click **💾 Save Processed Data**
- Missing values are filled automatically
- Download the cleaned dataset

### Export Combined Data
- After uploading multiple files
- Click **📥 Download Combined Data**
- All files merged into one CSV

### Export Current Data
- Go to **📊 Data Preview** tab
- Click **📥 Download as CSV**
- Get current dataset in CSV format

---

## 🔄 Common Workflows

### Workflow 1: Single Dataset Import
```
1. Download template
2. Fill with your data
3. Upload single file
4. Use for predictions
5. Export results
```

### Workflow 2: Batch Import
```
1. Prepare multiple CSV files
2. Use Data Management → Import Data
3. Upload multiple files
4. Download combined data
5. Analyze combined dataset
```

### Workflow 3: Template-Based Entry
```
1. Get blank template
2. Enter data manually
3. Save as CSV
4. Upload in app
5. Get predictions
```

---

## 🆘 Troubleshooting

### "Missing columns" Error
**Problem:** Some required columns are missing
**Solution:** 
- Download template again
- Match column names exactly
- Use exact capitalization and spelling

### "File could not be read" Error
**Problem:** File format is incorrect
**Solution:**
- Save file as CSV (not Excel)
- Check for special characters
- Remove any formatting from cells
- Try opening and re-saving the file

### "No data uploaded" 
**Problem:** Upload didn't work
**Solution:**
- Check file size (should be under 200MB)
- Verify file is CSV format
- Try smaller file first
- Check browser console for errors

### Data shows as "Rejected" for everyone
**Problem:** Model is too strict or data doesn't match training
**Solution:**
- Check credit scores (should be 300-850)
- Verify income values are reasonable
- Ensure categorical values match exactly
- Use Data Preview to check for outliers

---

## 🎯 Best Practices

### ✅ Do:
- Validate data before uploading
- Use the provided template
- Check for missing values
- Test with small dataset first
- Keep backup of original data
- Document any data transformations

### ❌ Don't:
- Change column names
- Use different formats for categories
- Upload files with thousands of rows without testing
- Trust predictions without reviewing model performance
- Skip data validation steps
- Use special characters in text fields

---

## 📈 Dataset Recommendations

### Optimal Dataset Size
- **Minimum:** 50 records
- **Recommended:** 500+ records
- **Large:** 10,000+ records
- **Maximum:** 100,000+ records

### Data Quality
- **Complete:** 95%+ non-null values
- **Consistent:** Values match expected formats
- **Valid:** Data within realistic ranges
- **Unique:** Minimal duplicates

### Diversity
- Mix of different genders
- Various education levels
- Range of income levels
- Different loan intents
- Mix of approved/rejected

---

## 🔐 Data Security

- **Local Processing:** All data processed on your machine
- **No Storage:** Data not saved to server
- **No Transmission:** Data doesn't leave your browser (except to train model locally)
- **No Sharing:** Your data is private
- **Downloadable:** You can export your data anytime

---

## 📚 Example Datasets

### Sample 1: Small Business Loans
```
Age: 35-55
Income: $60K-$150K
Loan Amount: $20K-$50K
Intent: BUSINESS (use VENTURE)
```

### Sample 2: Student Loans
```
Age: 22-35
Income: $25K-$60K
Loan Amount: $5K-$15K
Intent: EDUCATION
Previous Loan: Mix of Yes/No
```

### Sample 3: Personal Loans
```
Age: 25-45
Income: $30K-$100K
Loan Amount: $5K-$25K
Intent: PERSONAL or DEBTCONSOLIDATION
Credit Score: 600-750
```

---

## 💡 Tips for Success

1. **Start Small:** Upload 10-20 records first to test
2. **Validate Format:** Check one row matches template exactly
3. **Check Data Types:** Numbers as numbers, text as text
4. **Review Preview:** Always check preview before using
5. **Export Results:** Save processed data for records
6. **Compare Models:** Test different datasets
7. **Document Changes:** Track what you modified
8. **Use Insights:** Review analytics before predictions

---

## 🚀 Advanced Features

### Bulk Processing
- Upload multiple files
- Combine into one dataset
- Process all at once
- Export combined results

### Data Preprocessing
- System fills missing values
- Automatically encodes categorical data
- Normalizes numeric ranges
- Removes obvious errors

### Quality Reports
- Missing value summary
- Duplicate detection
- Statistical summaries
- Value range verification

---

## 📞 Getting Help

**Can't upload?**
- Check file format (must be CSV)
- Verify file size
- Try different browser

**Data validation failed?**
- Download template
- Compare your data to template
- Check column names and values
- Ensure no extra spaces

**Predictions seem wrong?**
- Review model performance page
- Check your data quality
- Verify categorical values
- Look at feature importance

**Need more features?**
- Check the main documentation
- Review other dashboard pages
- Explore analytics section

---

**Ready to import your data?** 🚀 
Go to **📤 Data Management** and start with the **📋 Template** tab!
