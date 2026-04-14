# Beginner Finance Dashboard

## 1. Problem and User

Many beginner investors and business students find it difficult to understand stock charts, financial indicators, and company comparison results. They may see numbers such as return, volatility, or profit margin, but still not know what these values actually mean.

This project aims to solve that problem by building a beginner-friendly interactive finance dashboard. The tool is designed for beginner investors and business students with limited prior knowledge of financial analysis.

## 2. Product Overview

The dashboard allows users to:

* select one or two companies
* choose a date range
* view stock price trends
* view market indicators such as total return and volatility
* view financial indicators such as revenue, net profit, profit margin, quick ratio, and current ratio
* compare two companies side by side
* explore key concepts and formulas through a concept explorer
* read beginner-friendly interpretations and key takeaways

The goal is to turn real financial data into a learning-oriented product rather than just displaying raw code or raw tables.

## 3. Data Source

The data used in this project are retrieved from **WRDS**.

Two main types of data are used:

* **Market data** from CRSP monthly stock files
* **Financial statement data** from Compustat fundamentals

These data are used to help beginner users understand both stock market performance and company fundamentals.

**Access date:** 9 April 2026

## 4. Methods

This project uses Python to complete a full analytical workflow.

Main steps include:

1. connect to WRDS
2. retrieve stock market data using SQL queries
3. retrieve financial statement data using SQL queries
4. clean and organise the data with pandas
5. calculate key indicators such as:

   * Total Return
   * Volatility
   * Profit Margin
   * Quick Ratio
   * Current Ratio
6. visualise price trends and financial trends with matplotlib
7. generate beginner-friendly explanations and comparisons
8. present the results in an interactive Streamlit dashboard

## 5. Key Features

### Market analysis

* stock price trend chart
* total return
* volatility
* short market interpretation

### Financial analysis

* fundamentals table with clearer column names and units
* revenue trend
* net profit trend
* profit margin trend
* quick ratio trend
* current ratio trend
* short fundamentals interpretation

### Comparison function

* optional Company B selection
* side-by-side comparison table
* comparison interpretation in Beginner mode or Deeper mode

### Concept Explorer

The dashboard also includes a concept explorer covering important terms such as:

* Company
* Ticker
* Fiscal Year
* Price
* Price Trend
* Trend
* Return
* Total Return
* Volatility
* Risk
* Revenue
* Net Profit
* Profit Margin
* Quick Ratio
* Current Ratio
* Liquidity
* Profitability
* Fundamentals
* Market Performance
* Comparison
* Beginner Mode
* Deeper Mode
* Key Takeaways

Each concept includes:

* meaning
* importance
* formula (when relevant)
* role in the project

## 6. Key Findings

This project shows that market performance and company fundamentals are related, but they are not always the same.

For example:

* a company with stronger stock return may also have higher volatility
* a company with stronger profitability may not have the strongest stock return
* liquidity, profitability, and market performance may move in different directions

This makes the dashboard useful for beginners because it encourages them to look at multiple indicators together rather than relying on only one number.

## 7. How to Run

To run this project locally, make sure the required packages are installed.

Suggested packages include:

* streamlit
* wrds
* pandas
* matplotlib

Then run the app with:

```bash
streamlit run app.py
```

Please note that this project uses WRDS data, so access may depend on a valid WRDS account and connection setup.

## 8. Project Files

Typical project files include:

* `app.py` — the Streamlit dashboard
* `mini assignment.ipynb` — the notebook showing the analytical workflow
* `README.md` — project introduction and instructions

## 9. Product Link / Demo

* **Local app preview:** run through Streamlit on the local machine
* **Demo video:** to be added
* **Deployment link:** to be added if deployed online

## 10. Limitations

This project has several limitations.

* It currently includes a limited set of companies.
* The dashboard focuses on a small number of beginner-friendly indicators rather than a full professional valuation system.
* Some companies may have limited market data in certain date ranges.
* The app currently relies on WRDS access, which makes public sharing more difficult.
* The interpretations are simplified for beginner learning purposes.

## 11. Future Improvements

This product can be improved in several ways:

* add more companies
* add more financial indicators
* improve public deployment
* make the interface more polished
* add more personalised explanations
* expand the concept explorer further

## 12. AI Use

AI tools were used to support coding, debugging, explanation writing, and product structure design during the development of this project.

All final code, structure, and wording were checked and revised by the student before submission.
