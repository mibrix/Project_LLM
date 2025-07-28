# 📊 LLM-Based Stock Recommender

Welcome to the **LLM-Based Stock Recommender**, an intelligent AI agent that combines real-time financial data with language model reasoning to generate stock market recommendations. Built with [Langchain](https://python.langchain.com/) and [Streamlit](https://streamlit.io/), this app provides users with actionable insights through an intuitive interface.

---

## 🌟 Project Overview

This project aims to:

- Develop a **Large Language Model (LLM)** agent capable of retrieving and analyzing financial data.
- Generate **Buy / Hold / Sell** recommendations using structured reasoning.
- Make stock market insights more **accessible**, especially to users with limited time or financial expertise.

---

## ⚙️ Technical Architecture

### 🔗 LLM Agent (Langchain)

The agent is implemented using the [Langchain](https://python.langchain.com/) framework and calls three main functions:

- `get_financial_statements(ticker)` – Retrieves the last 3 financial statements of a company using the `yfinance` library.
- `get_stock_price(ticker)` – Retrieves the past year's stock prices using `yfinance`.
- `get_recent_stock_news(ticker)` – Fetches recent news via the [Finnhub API](https://finnhub.io/).

These data sources are passed into a prompt template, where the LLM processes and reasons through a multi-step decision pipeline to generate investment recommendations.

### 💬 LLM Model

- **Model Used**: `gemini-1.5-flash`
- **Temperature**: `0` (for deterministic results)
- Supports high-frequency API usage to accommodate multi-prompt workflows.

### 🖥️ Frontend (Streamlit)

The frontend is built with [Streamlit](https://streamlit.io/), offering:
- A sidebar with usage instructions.
- A clean user interface for querying and viewing recommendations.
- Follow-up question functionality (e.g., asking for more details about market sentiment or risk).

---

## 🧾 Sample Output

Below is a simplified example of a model-generated output:



- Ensure you have all required dependencies installed as listed in `requirements.txt`.
- If you encounter any issues, feel free to reach out for help.
