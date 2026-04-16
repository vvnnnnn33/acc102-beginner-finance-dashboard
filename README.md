# Beginner Finance Dashboard

## ACC102 Mini Assignment – Track 4 Interactive Tool

This project is a beginner-friendly interactive finance dashboard built with Python and Streamlit.

It is designed to help beginner investors and business students understand companies through both market data and basic financial statement data. The tool combines automatic analysis, concept explanation, company comparison, and beginner-friendly interpretation.

---

## 1. Problem Definition

Beginners often find it difficult to understand stock charts, company performance, and financial terms. They may see numbers such as return, volatility, or profit margin, but still not know what those values actually mean.

This project aims to solve that problem by building a beginner-friendly learning tool that uses real company data to explain both market performance and basic financial fundamentals.

It also includes a comparison function that allows users to compare two companies using the same financial and market indicators, helping them develop a clearer understanding of business performance and stock market behaviour.

---

## 2. Intended User / Audience

This tool is designed for:

- beginner investors
- business students
- users with limited prior knowledge of financial analysis

The product focuses on learning, clarity, and accessibility rather than advanced professional valuation.

---

## 3. Product Overview

Users select one or two companies and choose a time range. The system then produces automatic analysis, including:

- stock price trend
- total return
- volatility
- revenue
- net profit
- profit margin
- quick ratio
- current ratio

Users can also:

- choose an explanation mode (Beginner or Deeper)
- compare two companies side by side
- explore key concepts and formulas through the Concept Explorer
- read beginner-friendly result interpretation
- read short Key Takeaways

The overall aim is to turn real financial data into a learning-oriented product rather than simply displaying raw code or raw tables.

---

## 4. Data Source

The original data used in this project were retrieved from WRDS.

Two main types of data were used:

- Market data from CRSP monthly stock files
- Financial statement data from Compustat fundamentals

These data were first analysed in the notebook. After that, the processed company datasets were exported as CSV files for the final Streamlit product.

Therefore:

- the notebook represents the full WRDS-based analytical workflow
- the final deployed app reads exported CSV files for stability and accessibility

**Access date:** 9 April 2026

---

## 5. Methods

This project uses Python to complete a full analytical workflow.

Main steps include:

1. connect to WRDS in the notebook
2. retrieve stock market data using SQL queries
3. retrieve financial statement data using SQL queries
4. clean and organise the data with pandas
5. calculate key indicators such as:
   - Total Return
   - Volatility
   - Profit Margin
   - Quick Ratio
   - Current Ratio
6. export processed company data into CSV files
7. visualise price trends and financial trends with matplotlib
8. generate beginner-friendly explanations and comparisons
9. present the results in an interactive Streamlit dashboard

This project therefore combines data retrieval, data cleaning, ratio calculation, visualisation, interpretation, and product design.

---

## 6. Key Features

### Market analysis
- stock price trend chart
- total return
- volatility
- short market interpretation

### Financial analysis
- fundamentals table with clearer column names and units
- revenue trend chart
- net profit trend chart
- profit margin trend chart
- quick ratio trend chart
- current ratio trend chart
- short fundamentals interpretation

### Comparison function
- optional Company B selection
- side-by-side comparison table
- comparison interpretation in Beginner mode or Deeper mode

### Concept Explorer

The dashboard also includes a concept explorer covering important terms such as:

- Company
- Ticker
- Date Range
- Fiscal Year
- Price
- Price Trend
- Trend
- Return
- Total Return
- Volatility
- Risk
- Revenue
- Net Profit
- Profit Margin
- Quick Ratio
- Current Ratio
- Liquidity
- Profitability
- Fundamentals
- Fundamentals Summary
- Market Summary
- Market Performance
- Comparison
- Comparison Summary
- Beginner Mode
- Deeper Mode
- Result Interpretation
- Key Takeaways
- Learning Report

Each concept includes:

- meaning
- importance
- formula (when relevant)
- role in the project

---

## 7. Key Findings

This project shows that market performance and company fundamentals are related, but they are not always the same.

For example:

- a company with stronger stock return may also have higher volatility
- a company with stronger profitability may not have the strongest stock return
- liquidity, profitability, and market performance may move in different directions

This makes the dashboard useful for beginners because it encourages them to look at multiple indicators together rather than relying on only one number.

---

## 8. How to Run

To run this project locally, make sure the required packages are installed.

Suggested packages include:

- streamlit
- pandas
- matplotlib

Then run the app with `streamlit run app.py`.

Please also make sure the `data` folder is included in the project directory, because the final app reads exported CSV files instead of connecting to WRDS live.

---

## 9. Project Files

Typical project files include:

- `app.py` — the final Streamlit dashboard using exported CSV files
- `mini_assignment.ipynb` — the notebook showing the full WRDS-based analytical workflow
- `README.md` — project introduction and instructions
- `requirements.txt` — required Python packages
- `data/` — exported company market and fundamentals CSV files

---

## 10. Product Link / Demo

- Local app preview: run through Streamlit on the local machine
- GitHub repository: included as project code link
- Deployment link: included if available
- Demo video: included separately

---

## 11. Limitations

This project has several limitations.

- It currently includes a limited set of companies.
- The dashboard focuses on a small number of beginner-friendly indicators rather than a full professional valuation system.
- Some companies may have limited market or financial data in certain ranges.
- The final deployed app uses exported CSV files rather than live WRDS queries.
- The interpretations are simplified for beginner learning purposes.

---

## 12. Future Improvements

This product can be improved in several ways:

- add more companies
- add more financial indicators
- improve interface design and styling
- add more personalised explanations
- expand the concept explorer further
- improve deployment and update workflow for refreshed datasets

---

## 13. AI Use

AI tools were used during this project to support code debugging, wording improvement, and product structuring.

All final code, analysis logic, and written content were reviewed, tested, and revised by the student before submission.

A fuller AI disclosure is provided at the end of the reflection report.
