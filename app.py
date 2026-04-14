import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


st.set_page_config(page_title="Beginner Finance Dashboard", layout="wide")

st.title("Beginner Finance Dashboard")
st.subheader("ACC102 Mini Assignment – Track 4")
st.write("This tool helps beginner users compare companies using market data and basic financial statement data.")
st.write("Users can explore stock performance, company fundamentals, concept explanations, and beginner-friendly interpretations.")


company_dict = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "McDonald's": "MCD",
    "Spotify": "SPOT",
    "Duolingo": "DUOL",
    "Reddit": "RDDT",
    "Robinhood": "HOOD",
    "Airbnb": "ABNB",
    "Uber": "UBER",
    "Palantir": "PLTR",
    "Netflix": "NFLX"
}


def get_return_comment(total_return_pct):
    if total_return_pct is None or pd.isna(total_return_pct):
        return "not enough market data"
    if total_return_pct < 0:
        return "weak market performance"
    elif total_return_pct <= 20:
        return "modest market performance"
    return "strong market performance"


def get_volatility_comment(volatility_pct):
    if volatility_pct is None or pd.isna(volatility_pct):
        return "not enough market data"
    if volatility_pct < 10:
        return "relatively stable stock movement"
    elif volatility_pct <= 20:
        return "moderate stock volatility"
    return "high stock volatility"


def get_quick_ratio_comment(value):
    if value < 1:
        return "weak short-term liquidity"
    elif value <= 1.5:
        return "acceptable short-term liquidity"
    return "relatively strong short-term liquidity"


def get_current_ratio_comment(value):
    if value < 1:
        return "weak current liquidity position"
    elif value <= 1.5:
        return "acceptable current liquidity position"
    return "relatively strong current liquidity position"


def get_profit_margin_comment(value):
    if value < 10:
        return "weak profitability"
    elif value <= 20:
        return "moderate profitability"
    return "strong profitability"


def fetch_market_data(db, ticker, start_date, end_date):
    query = f"""
    SELECT
        a.date,
        a.permno,
        b.htsymbol,
        a.prc,
        a.ret
    FROM crsp.msf AS a
    LEFT JOIN crsp.msfhdr AS b
        ON a.permno = b.permno
    WHERE b.htsymbol = '{ticker}'
      AND a.date >= '{start_date}'
      AND a.date <= '{end_date}'
    """
    df = db.raw_sql(query, date_cols=["date"])
    df = df.sort_values("date").reset_index(drop=True).copy()
    df = df.dropna(subset=["prc"])
    df.loc[:, "prc"] = pd.to_numeric(df["prc"], errors="coerce").abs()
    df.loc[:, "ret"] = pd.to_numeric(df["ret"], errors="coerce")
    df = df.dropna(subset=["prc"])
    return df


def fetch_fundamental_data(db, ticker, start_year, end_year):
    query = f"""
    SELECT
        tic,
        fyear,
        sale,
        ni,
        act,
        lct,
        invt
    FROM comp.funda
    WHERE tic = '{ticker}'
      AND fyear >= {start_year}
      AND fyear <= {end_year}
    """
    df = db.raw_sql(query)
    df = df.dropna(subset=["act", "lct", "invt"]).drop_duplicates().reset_index(drop=True).copy()

    df["sale"] = pd.to_numeric(df["sale"], errors="coerce")
    df["ni"] = pd.to_numeric(df["ni"], errors="coerce")
    df["act"] = pd.to_numeric(df["act"], errors="coerce")
    df["lct"] = pd.to_numeric(df["lct"], errors="coerce")
    df["invt"] = pd.to_numeric(df["invt"], errors="coerce")

    df["profit_margin"] = df["ni"] / df["sale"]
    df["profit_margin_pct"] = df["profit_margin"] * 100
    df["quick_ratio"] = (df["act"] - df["invt"]) / df["lct"]
    df["current_ratio"] = df["act"] / df["lct"]

    return df


def build_market_summary(market_df):
    valid_prices = market_df["prc"].dropna()

    if market_df.empty or len(valid_prices) < 2:
        return {
            "total_return_pct": None,
            "volatility_pct": None,
            "return_comment": "not enough market data",
            "volatility_comment": "not enough market data",
        }

    start_price = valid_prices.iloc[0]
    end_price = valid_prices.iloc[-1]

    if pd.isna(start_price) or pd.isna(end_price) or start_price == 0:
        return {
            "total_return_pct": None,
            "volatility_pct": None,
            "return_comment": "not enough market data",
            "volatility_comment": "not enough market data",
        }

    total_return = (end_price - start_price) / start_price
    total_return_pct = float(total_return * 100) if pd.notna(total_return) else None

    valid_returns = market_df["ret"].dropna()
    if len(valid_returns) == 0:
        volatility_pct = None
    else:
        volatility = valid_returns.std()
        volatility_pct = float(volatility * 100) if pd.notna(volatility) else None

    return {
        "total_return_pct": total_return_pct,
        "volatility_pct": volatility_pct,
        "return_comment": get_return_comment(total_return_pct),
        "volatility_comment": get_volatility_comment(volatility_pct),
    }


def build_fundamental_summary(fund_df):
    latest_profit_margin = float(fund_df["profit_margin_pct"].iloc[-1])
    latest_quick_ratio = float(fund_df["quick_ratio"].iloc[-1])
    latest_current_ratio = float(fund_df["current_ratio"].iloc[-1])

    return {
        "latest_revenue": float(fund_df["sale"].iloc[-1]),
        "latest_net_profit": float(fund_df["ni"].iloc[-1]),
        "latest_profit_margin": latest_profit_margin,
        "latest_quick_ratio": latest_quick_ratio,
        "latest_current_ratio": latest_current_ratio,
        "profit_margin_comment": get_profit_margin_comment(latest_profit_margin),
        "quick_ratio_comment": get_quick_ratio_comment(latest_quick_ratio),
        "current_ratio_comment": get_current_ratio_comment(latest_current_ratio),
    }


def plot_price_trend(df, company_name):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["prc"])
    ax.set_title(f"{company_name} Price Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.xticks(rotation=45)
    return fig


def plot_fundamental_trend(df, company_name, metric_col, metric_label):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["fyear"], df[metric_col], marker="o")
    ax.set_title(f"{company_name} {metric_label} Trend")
    ax.set_xlabel("Year")
    ax.set_ylabel(metric_label)
    ax.set_xticks(df["fyear"])
    return fig


def format_fundamental_table(fund_df):
    display_df = fund_df[["fyear", "sale", "ni", "profit_margin_pct", "quick_ratio", "current_ratio"]].copy()
    display_df = display_df.rename(columns={
        "fyear": "Year",
        "sale": "Revenue (USD mn)",
        "ni": "Net Profit (USD mn)",
        "profit_margin_pct": "Profit Margin (%)",
        "quick_ratio": "Quick Ratio (x)",
        "current_ratio": "Current Ratio (x)"
    })
    return display_df


def display_market_summary(company_name, market_summary):
    st.subheader(f"{company_name} Market Summary")

    if market_summary["total_return_pct"] is not None:
        st.write(f"Total return: {market_summary['total_return_pct']:.2f}%")
    else:
        st.write("Total return: not enough market data")

    if market_summary["volatility_pct"] is not None:
        st.write(f"Volatility: {market_summary['volatility_pct']:.2f}%")
    else:
        st.write("Volatility: not enough market data")

    st.write(f"Return interpretation: {market_summary['return_comment']}")
    st.write(f"Volatility interpretation: {market_summary['volatility_comment']}")


def display_fundamental_summary(company_name, fund_summary):
    st.subheader(f"{company_name} Fundamentals Summary")
    st.write(f"Latest revenue: {fund_summary['latest_revenue']:,.2f} USD mn")
    st.write(f"Latest net profit: {fund_summary['latest_net_profit']:,.2f} USD mn")
    st.write(f"Latest profit margin: {fund_summary['latest_profit_margin']:.2f}%")
    st.write(f"Latest quick ratio: {fund_summary['latest_quick_ratio']:.2f}x")
    st.write(f"Latest current ratio: {fund_summary['latest_current_ratio']:.2f}x")
    st.write(f"Profitability interpretation: {fund_summary['profit_margin_comment']}")
    st.write(f"Quick ratio interpretation: {fund_summary['quick_ratio_comment']}")
    st.write(f"Current ratio interpretation: {fund_summary['current_ratio_comment']}")


st.subheader("User Selection")

if "analysis_started" not in st.session_state:
    st.session_state.analysis_started = False

if "saved_company_a" not in st.session_state:
    st.session_state.saved_company_a = "Apple"

if "saved_company_b" not in st.session_state:
    st.session_state.saved_company_b = "None"

if "saved_start_date" not in st.session_state:
    st.session_state.saved_start_date = pd.to_datetime("2019-01-01")

if "saved_end_date" not in st.session_state:
    st.session_state.saved_end_date = pd.to_datetime("2024-12-31")


with st.form("selection_form"):
    company_a = st.selectbox(
        "Select Company A",
        list(company_dict.keys()),
        index=list(company_dict.keys()).index(st.session_state.saved_company_a)
    )

    company_b_options = ["None"] + list(company_dict.keys())
    company_b = st.selectbox(
        "Select Company B (optional)",
        company_b_options,
        index=company_b_options.index(st.session_state.saved_company_b)
    )

    start_date = st.date_input(
        "Select start date",
        value=st.session_state.saved_start_date
    )

    end_date = st.date_input(
        "Select end date",
        value=st.session_state.saved_end_date
    )

    submitted = st.form_submit_button("Start Analysis")

if submitted:
    st.session_state.analysis_started = True
    st.session_state.saved_company_a = company_a
    st.session_state.saved_company_b = company_b
    st.session_state.saved_start_date = start_date
    st.session_state.saved_end_date = end_date

run_analysis = st.session_state.analysis_started

company_a = st.session_state.saved_company_a
company_b = st.session_state.saved_company_b
start_date = st.session_state.saved_start_date
end_date = st.session_state.saved_end_date

ticker_a = company_dict[company_a]
ticker_b = None if company_b == "None" else company_dict[company_b]


if run_analysis:
    if start_date >= end_date:
        st.error("The start date must be earlier than the end date.")
        st.stop()

    username = "yuqingwu24"
    db = wrds.Connection(wrds_username=username)

    try:
        market_data_a = fetch_market_data(db, ticker_a, start_date, end_date)
        fund_data_a = fetch_fundamental_data(db, ticker_a, start_date.year, end_date.year)

        market_summary_a = build_market_summary(market_data_a)
        fund_summary_a = build_fundamental_summary(fund_data_a)

        st.header(f"{company_a} Analysis")

        st.subheader(f"{company_a} Price Trend")
        st.pyplot(plot_price_trend(market_data_a, company_a))

        display_market_summary(company_a, market_summary_a)

        st.subheader(f"{company_a} Fundamentals Table")
        st.caption("Revenue and Net Profit are displayed in USD mn. Quick Ratio and Current Ratio are shown in times (x).")
        st.dataframe(format_fundamental_table(fund_data_a))

        st.subheader(f"{company_a} Fundamentals Trend")
        metric_a = st.selectbox(
            f"Choose a financial metric for {company_a}",
            ["Revenue", "Net Profit", "Profit Margin (%)", "Quick Ratio", "Current Ratio"],
            key="fundamental_metric_a"
        )

        metric_map = {
            "Revenue": ("sale", "Revenue (USD mn)"),
            "Net Profit": ("ni", "Net Profit (USD mn)"),
            "Profit Margin (%)": ("profit_margin_pct", "Profit Margin (%)"),
            "Quick Ratio": ("quick_ratio", "Quick Ratio (x)"),
            "Current Ratio": ("current_ratio", "Current Ratio (x)")
        }

        metric_col_a, metric_label_a = metric_map[metric_a]
        st.pyplot(plot_fundamental_trend(fund_data_a, company_a, metric_col_a, metric_label_a))

        display_fundamental_summary(company_a, fund_summary_a)

        has_company_b = ticker_b is not None

        if has_company_b:
            market_data_b = fetch_market_data(db, ticker_b, start_date, end_date)
            fund_data_b = fetch_fundamental_data(db, ticker_b, start_date.year, end_date.year)

            market_summary_b = build_market_summary(market_data_b)
            fund_summary_b = build_fundamental_summary(fund_data_b)

            st.header(f"{company_b} Analysis")

            if market_data_b.empty or market_summary_b["total_return_pct"] is None:
                st.warning(f"{company_b} does not have enough market data in the selected date range to produce a full market analysis.")
            else:
                st.subheader(f"{company_b} Price Trend")
                st.pyplot(plot_price_trend(market_data_b, company_b))

            display_market_summary(company_b, market_summary_b)

            st.subheader(f"{company_b} Fundamentals Table")
            st.caption("Revenue and Net Profit are displayed in USD mn. Quick Ratio and Current Ratio are shown in times (x).")
            st.dataframe(format_fundamental_table(fund_data_b))

            st.subheader(f"{company_b} Fundamentals Trend")
            metric_b = st.selectbox(
                f"Choose a financial metric for {company_b}",
                ["Revenue", "Net Profit", "Profit Margin (%)", "Quick Ratio", "Current Ratio"],
                key="fundamental_metric_b"
            )

            metric_col_b, metric_label_b = metric_map[metric_b]
            st.pyplot(plot_fundamental_trend(fund_data_b, company_b, metric_col_b, metric_label_b))

            display_fundamental_summary(company_b, fund_summary_b)

            st.header("Combined Comparison")

            comparison_summary = pd.DataFrame({
                "Company": [company_a, company_b],
                "Ticker": [ticker_a, ticker_b],
                "Total Return (%)": [market_summary_a["total_return_pct"], market_summary_b["total_return_pct"]],
                "Volatility (%)": [market_summary_a["volatility_pct"], market_summary_b["volatility_pct"]],
                "Revenue (USD mn)": [fund_summary_a["latest_revenue"], fund_summary_b["latest_revenue"]],
                "Net Profit (USD mn)": [fund_summary_a["latest_net_profit"], fund_summary_b["latest_net_profit"]],
                "Profit Margin (%)": [fund_summary_a["latest_profit_margin"], fund_summary_b["latest_profit_margin"]],
                "Quick Ratio (x)": [fund_summary_a["latest_quick_ratio"], fund_summary_b["latest_quick_ratio"]],
                "Current Ratio (x)": [fund_summary_a["latest_current_ratio"], fund_summary_b["latest_current_ratio"]],
            })
            st.dataframe(comparison_summary)

        concept_explanations = {
            "Company": {
                "meaning": "Company refers to the business selected for analysis in the project.",
                "importance": "It is the main object of the analysis and helps users focus on one business at a time.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, users select one or two companies to explore their market performance and fundamentals."
            },
            "Ticker": {
                "meaning": "Ticker is the short stock code used to identify a company in the stock market.",
                "importance": "It is needed to retrieve market and financial statement data from WRDS.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, the ticker is automatically matched after the user selects a company name."
            },
            "Date Range": {
                "meaning": "Date range refers to the selected start date and end date used in the analysis.",
                "importance": "It defines the period over which the stock data and financial data are analysed.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, the selected date range determines which market observations and fiscal years are included."
            },
            "Fiscal Year": {
                "meaning": "Fiscal year is the reporting year used in the company’s financial statements.",
                "importance": "It helps users compare company performance across different reporting periods.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, fiscal year is used to organise revenue, net profit, and ratio data."
            },
            "Price": {
                "meaning": "Price is the market value of one share of the company at a given time.",
                "importance": "It helps users see how the stock moves over time.",
                "formula": "Price is directly retrieved from the market dataset rather than calculated here.",
                "project": "In this project, price is used to draw the stock price trend chart."
            },
            "Price Trend": {
                "meaning": "Price trend refers to the overall direction of stock price movement over time.",
                "importance": "It helps users identify whether the stock generally increased, decreased, or fluctuated.",
                "formula": "Based on the time series of stock prices across the selected date range.",
                "project": "In this project, price trend is visualised through a line chart based on historical market data."
            },
            "Trend": {
                "meaning": "Trend refers to the general direction of change in a variable over time.",
                "importance": "It helps users judge whether an indicator is increasing, decreasing, or fluctuating.",
                "formula": "Trend is interpreted from the pattern of values across time rather than one single formula.",
                "project": "In this project, trend is shown through line charts for price, revenue, net profit, profit margin, and liquidity ratios."
            },
            "Return": {
                "meaning": "Return shows how much the stock price changed over a period of time.",
                "importance": "It helps beginners understand whether a stock performed positively or negatively.",
                "formula": "Return = (Ending Price - Starting Price) / Starting Price",
                "project": "In this project, return is used as the basis for total return analysis."
            },
            "Total Return": {
                "meaning": "Total return is the overall percentage change in stock price over the selected period.",
                "importance": "It helps users compare overall stock performance across companies.",
                "formula": "Total Return (%) = [(Ending Price - Starting Price) / Starting Price] × 100",
                "project": "In this project, total return is displayed in the market summary and comparison table."
            },
            "Volatility": {
                "meaning": "Volatility shows how strongly the stock price moved up and down.",
                "importance": "It helps users understand whether a company appears relatively stable or risky.",
                "formula": "Volatility = standard deviation of returns; Volatility (%) = std(return) × 100",
                "project": "In this project, volatility is calculated from return data to show market fluctuation."
            },
            "Risk": {
                "meaning": "Risk refers to the uncertainty or instability in investment outcomes.",
                "importance": "It helps users understand that stronger price fluctuation may mean less stability.",
                "formula": "In this project, risk is mainly represented by Volatility.",
                "project": "In this project, users interpret market risk mainly through stock volatility."
            },
            "Market Summary": {
                "meaning": "Market summary is the section that reports the key market indicators of the selected company.",
                "importance": "It gives users a short overview of stock performance before deeper interpretation.",
                "formula": "Main metrics shown here include Total Return and Volatility.",
                "project": "In this project, the market summary explains stock growth and price fluctuation."
            },
            "Revenue": {
                "meaning": "Revenue is the total income generated from the company’s business activities.",
                "importance": "It helps users understand the scale of the company’s operations.",
                "formula": "Revenue is directly retrieved from the financial statement dataset rather than calculated here.",
                "project": "In this project, revenue is used to show changes in business size across fiscal years."
            },
            "Net Profit": {
                "meaning": "Net profit is the amount of earnings left after costs and expenses are deducted.",
                "importance": "It helps users understand whether the company is making money.",
                "formula": "Net Profit is directly retrieved from the financial statement dataset rather than calculated here.",
                "project": "In this project, net profit is used to show the company’s profitability over time."
            },
            "Profit Margin": {
                "meaning": "Profit margin is the percentage of revenue that is converted into profit.",
                "importance": "It helps users understand how efficiently the company turns revenue into earnings.",
                "formula": "Profit Margin = Net Profit / Revenue; Profit Margin (%) = (Net Profit / Revenue) × 100",
                "project": "In this project, profit margin is used to compare profitability between companies."
            },
            "Quick Ratio": {
                "meaning": "Quick ratio is a liquidity indicator based on liquid current assets relative to current liabilities.",
                "importance": "It helps users understand whether a company can cover short-term obligations without relying heavily on inventory.",
                "formula": "Quick Ratio = (Current Assets - Inventory) / Current Liabilities",
                "project": "In this project, quick ratio is used to compare short-term liquidity strength."
            },
            "Current Ratio": {
                "meaning": "Current ratio compares current assets with current liabilities.",
                "importance": "It helps users understand the company’s short-term liquidity position.",
                "formula": "Current Ratio = Current Assets / Current Liabilities",
                "project": "In this project, current ratio is used together with quick ratio to assess liquidity."
            },
            "Liquidity": {
                "meaning": "Liquidity refers to the company’s ability to meet short-term obligations.",
                "importance": "It helps users judge whether the company appears financially flexible in the short term.",
                "formula": "Main liquidity indicators here: Quick Ratio and Current Ratio",
                "project": "In this project, liquidity is assessed mainly through quick ratio and current ratio."
            },
            "Profitability": {
                "meaning": "Profitability refers to the company’s ability to generate earnings from its operations.",
                "importance": "It helps users judge whether the company turns revenue into meaningful profit.",
                "formula": "Main profitability indicator here: Profit Margin = Net Profit / Revenue",
                "project": "In this project, profitability is mainly represented by profit margin and net profit."
            },
            "Fundamentals": {
                "meaning": "Fundamentals refer to the basic financial condition and operating performance of a company.",
                "importance": "They help users understand the company beyond stock price movements.",
                "formula": "Main fundamentals used here: Revenue, Net Profit, Profit Margin, Quick Ratio, Current Ratio",
                "project": "In this project, fundamentals are represented by revenue, net profit, profitability, and liquidity indicators."
            },
            "Fundamentals Summary": {
                "meaning": "Fundamentals summary is the section that reports the latest key financial indicators of the selected company.",
                "importance": "It gives users a short overview of the company’s business condition and financial strength.",
                "formula": "Main metrics shown here: Revenue, Net Profit, Profit Margin, Quick Ratio, Current Ratio",
                "project": "In this project, the fundamentals summary helps users interpret business performance more quickly."
            },
            "Comparison": {
                "meaning": "Comparison means evaluating two companies using the same indicators.",
                "importance": "It helps users identify differences in market performance and business fundamentals.",
                "formula": "Comparison is based on side-by-side indicator values rather than one formula.",
                "project": "In this project, comparison is used to show that stock performance and financial strength may differ across companies."
            },
            "Comparison Summary": {
                "meaning": "Comparison summary is the table that puts two selected companies side by side using the same measures.",
                "importance": "It helps users compare return, risk, profitability, and liquidity in one place.",
                "formula": "Main measures compared: Total Return, Volatility, Revenue, Net Profit, Profit Margin, Quick Ratio, Current Ratio",
                "project": "In this project, the comparison summary is a key user-facing output."
            },
            "Market Performance": {
                "meaning": "Market performance refers to how a company performs in the stock market.",
                "importance": "It helps users understand price movement, return, and market risk.",
                "formula": "Main market indicators here: Price Trend, Total Return, Volatility",
                "project": "In this project, market performance is represented by price trend, return, and volatility."
            },
            "Beginner Mode": {
                "meaning": "Beginner mode is a simpler explanation mode designed for new users.",
                "importance": "It lowers the learning barrier and makes the results easier to understand.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, beginner mode provides shorter and clearer explanations of the indicators."
            },
            "Deeper Mode": {
                "meaning": "Deeper mode is a more detailed explanation mode for users who want stronger analytical understanding.",
                "importance": "It allows users to explore the same results with slightly more depth.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, deeper mode provides more analytical explanations of indicators and company comparison."
            },
            "Result Interpretation": {
                "meaning": "Result interpretation is the explanation layer that turns numerical outputs into readable conclusions.",
                "importance": "It helps users understand what the calculated indicators mean in practice.",
                "formula": "Not a calculated indicator. It is based on the combined reading of market and financial indicators.",
                "project": "In this project, result interpretation is available in Beginner mode and Deeper mode."
            },
            "Key Takeaways": {
                "meaning": "Key takeaways are short beginner-friendly lessons summarised from the analysis results.",
                "importance": "They help users focus on the most important insights without reading every chart or table in detail.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, key takeaways summarise what beginner users should learn from the comparison of market performance and fundamentals."
            },
            "Learning Report": {
                "meaning": "Learning report is a short summary written for beginner users based on the analysis results.",
                "importance": "It helps turn charts and numbers into easier conclusions.",
                "formula": "Not a calculated indicator.",
                "project": "In this project, the learning report combines market indicators and financial statement indicators into a simple summary."
            }
        }

        concept_table = pd.DataFrame(concept_explanations).T
        st.header("Concept Explorer")
        selected_concept = st.selectbox(
            "Choose a concept to explore",
            list(concept_explanations.keys()),
            key="concept_select"
        )
        st.write(concept_table.loc[selected_concept])

        st.header("Result Interpretation")

        def format_pct_or_na(value):
            if value is None or pd.isna(value):
                return "not enough market data"
            return f"{value:.2f}%"

        result_explanations = {
            "Single Company": {
                "Beginner": f"""
{company_a} showed {market_summary_a['return_comment']} over the selected period.

Its total return was {format_pct_or_na(market_summary_a['total_return_pct'])}, and its volatility was {format_pct_or_na(market_summary_a['volatility_pct'])}, which suggests {market_summary_a['volatility_comment']}.

From the financial statement side, the latest profit margin was {fund_summary_a['latest_profit_margin']:.2f}%, the quick ratio was {fund_summary_a['latest_quick_ratio']:.2f}, and the current ratio was {fund_summary_a['latest_current_ratio']:.2f}.

This suggests {fund_summary_a['profit_margin_comment']}, {fund_summary_a['quick_ratio_comment']}, and {fund_summary_a['current_ratio_comment']}.
""",
                "Deeper": f"""
{company_a} generated a total return of {format_pct_or_na(market_summary_a['total_return_pct'])} over the selected period, while its volatility was {format_pct_or_na(market_summary_a['volatility_pct'])}.

From the operating perspective, the company reported a latest profit margin of {fund_summary_a['latest_profit_margin']:.2f}%, a quick ratio of {fund_summary_a['latest_quick_ratio']:.2f}, and a current ratio of {fund_summary_a['latest_current_ratio']:.2f}.

Taken together, these results suggest {fund_summary_a['profit_margin_comment']}. In addition, the liquidity indicators imply {fund_summary_a['quick_ratio_comment']} and {fund_summary_a['current_ratio_comment']}. This means the company should be assessed using both market performance and financial condition.
"""
            }
        }

        if has_company_b and market_summary_a["total_return_pct"] is not None and market_summary_b["total_return_pct"] is not None:
            if market_summary_a["total_return_pct"] > market_summary_b["total_return_pct"]:
                higher_return_company = company_a
            else:
                higher_return_company = company_b

            if market_summary_a["volatility_pct"] > market_summary_b["volatility_pct"]:
                higher_volatility_company = company_a
            else:
                higher_volatility_company = company_b

            if fund_summary_a["latest_profit_margin"] > fund_summary_b["latest_profit_margin"]:
                higher_profit_margin_company = company_a
            else:
                higher_profit_margin_company = company_b

            if fund_summary_a["latest_quick_ratio"] > fund_summary_b["latest_quick_ratio"]:
                higher_quick_ratio_company = company_a
            else:
                higher_quick_ratio_company = company_b

            if fund_summary_a["latest_current_ratio"] > fund_summary_b["latest_current_ratio"]:
                higher_current_ratio_company = company_a
            else:
                higher_current_ratio_company = company_b

            if higher_return_company == higher_volatility_company:
                comparison_market_sentence = f"{higher_return_company} performed better in stock market return, but it also showed stronger price fluctuations."
            else:
                comparison_market_sentence = f"{higher_return_company} performed better in stock market return, while {higher_volatility_company} showed stronger price fluctuations."

            if higher_quick_ratio_company == higher_current_ratio_company:
                comparison_liquidity_sentence = f"{higher_quick_ratio_company} showed relatively stronger liquidity positions."
            else:
                comparison_liquidity_sentence = f"{higher_quick_ratio_company} showed a stronger quick ratio, while {higher_current_ratio_company} showed a stronger current ratio."

            result_explanations["Company Comparison"] = {
                "Beginner": f"""
{company_a} and {company_b} showed different patterns in both stock market performance and company fundamentals.

{company_a} had a total return of {market_summary_a['total_return_pct']:.2f}% and volatility of {market_summary_a['volatility_pct']:.2f}%, while {company_b} had a total return of {market_summary_b['total_return_pct']:.2f}% and volatility of {market_summary_b['volatility_pct']:.2f}%.

This means that {comparison_market_sentence}

From the financial statement side, {company_a} had a profit margin of {fund_summary_a['latest_profit_margin']:.2f}%, a quick ratio of {fund_summary_a['latest_quick_ratio']:.2f}, and a current ratio of {fund_summary_a['latest_current_ratio']:.2f}. {company_b} had a profit margin of {fund_summary_b['latest_profit_margin']:.2f}%, a quick ratio of {fund_summary_b['latest_quick_ratio']:.2f}, and a current ratio of {fund_summary_b['latest_current_ratio']:.2f}.

This suggests that {higher_profit_margin_company} was stronger in profitability. In addition, {comparison_liquidity_sentence}
""",
                "Deeper": f"""
The comparison between {company_a} and {company_b} shows a clear difference between market performance and operating fundamentals.

In market terms, {company_a} generated a total return of {market_summary_a['total_return_pct']:.2f}% with volatility of {market_summary_a['volatility_pct']:.2f}%, whereas {company_b} generated a total return of {market_summary_b['total_return_pct']:.2f}% with volatility of {market_summary_b['volatility_pct']:.2f}%. {comparison_market_sentence}

From the perspective of operating performance, {company_a} reported a profit margin of {fund_summary_a['latest_profit_margin']:.2f}%, a quick ratio of {fund_summary_a['latest_quick_ratio']:.2f}, and a current ratio of {fund_summary_a['latest_current_ratio']:.2f}. By contrast, {company_b} reported a profit margin of {fund_summary_b['latest_profit_margin']:.2f}%, a quick ratio of {fund_summary_b['latest_quick_ratio']:.2f}, and a current ratio of {fund_summary_b['latest_current_ratio']:.2f}.

These results suggest that {higher_profit_margin_company} had stronger profitability. In addition, {comparison_liquidity_sentence} This comparison demonstrates that return, risk, profitability, and liquidity can move in different directions.
"""
            }

        interpretation_case = st.selectbox(
            "Choose interpretation type",
            list(result_explanations.keys()),
            key="interpretation_case"
        )

        interpretation_mode = st.radio(
            "Choose explanation mode",
            ["Beginner", "Deeper"],
            key="interpretation_mode"
        )

        st.write(result_explanations[interpretation_case][interpretation_mode])

        st.header("Key Takeaways for Beginners")

        if has_company_b and market_summary_a["total_return_pct"] is not None and market_summary_b["total_return_pct"] is not None:
            if higher_return_company == higher_volatility_company:
                takeaway_market_sentence = f"{higher_return_company} showed stronger stock return, but it also showed higher volatility."
            else:
                takeaway_market_sentence = f"{higher_return_company} showed stronger stock return, while {higher_volatility_company} showed higher volatility."

            if higher_quick_ratio_company == higher_current_ratio_company:
                takeaway_liquidity_sentence = f"{higher_quick_ratio_company} showed relatively stronger short-term liquidity."
            else:
                takeaway_liquidity_sentence = f"{higher_quick_ratio_company} showed a stronger quick ratio, while {higher_current_ratio_company} showed a stronger current ratio."

            st.write(f"1. {takeaway_market_sentence}")
            st.write(f"2. {higher_profit_margin_company} showed stronger profitability.")
            st.write(f"3. {takeaway_liquidity_sentence}")
            st.write("4. This comparison suggests that stock market performance, profitability, and liquidity do not always move in the same direction.")
            st.write("5. Beginner investors should compare market indicators and financial indicators together.")
        else:
            st.write("1. Positive return means the stock price increased overall when enough market data are available.")
            st.write("2. Volatility helps users understand how stable or risky the stock appears.")
            st.write("3. Profit margin helps explain profitability, while quick ratio and current ratio help explain short-term liquidity.")
            st.write("4. Revenue and net profit trends help users see how the company’s financial performance changed over time.")
            st.write("5. Beginner investors should look at both market indicators and fundamentals together.")

    finally:
        db.close()