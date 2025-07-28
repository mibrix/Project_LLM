# AI-Powered Stock Market Recommendation Agent

This project develops a Large Language Model (LLM) agent designed to gather comprehensive data from various sources and generate actionable stock market recommendations for users. The goal is to provide individuals with data-driven insights to inform their investment decisions, especially those with limited time for in-depth research.

## Features

* **Automated Financial Research:** Tracks stock performance and analyzes news to democratize access to financial insights.

* **Data-Driven Recommendations:** Provides "buy," "hold," or "sell" recommendations based on real-time and historical data.

* **Elaboration Capability:** Allows users to request further details and sources on specific parts of the agent's response.

* **User-Friendly Interface:** An interactive web application for easy interaction.

## Technical Implementation

The LLM-based application is built using a robust set of Python libraries and a powerful language model.

### Core Technologies

* **Langchain:** Used for constructing the LLM agent, enabling it to retrieve data from diverse sources and generate structured responses.

* **Streamlit:** Provides an intuitive and interactive user interface for the web application, including side panels, background images, and other UI components.

* **Gemini 1.5 Flash:** The chosen LLM model, offering a generous number of requests per minute, crucial for processing multiple data sources per interaction. The model's temperature is set to 0 for deterministic output.

### Data Sources and Tools

The Langchain agent utilizes the following functions to gather necessary financial data:

* `get_financial_statements(ticker)`: Retrieves the last three financial statements of a given company using the `yfinance` library.

* `get_stock_price(ticker)`: Fetches historical stock prices for the last year of a given company, also using `yfinance`.

* `get_recent_stock_news(ticker)`: Gathers recent news summaries and metadata related to a company's stock using the **Finnhub API**.

### How the Agent Works

The LLM agent follows a step-by-step "thought" mechanism to process user queries and formulate recommendations. When a user submits a query, the agent:

1.  **Identifies Information Needs:** Determines what data is required (e.g., stock price, news, financial statements).

2.  **Executes Actions:** Calls the appropriate data retrieval functions (e.g., `get_stock_price`, `get_recent_stock_news`, `get_financial_statements`).

3.  **Synthesizes Information:** Processes the gathered data to assess the asset.

4.  **Generates Recommendation:** Forms a final recommendation (buy, hold, or sell) based on its analysis, following a predefined prompt template.

**Example Agent Thought Process:**

1.  **Thought:** I need to gather information about Amazon to make a recommendation.
    **Action:** `get_stock_price(AMZN)`

2.  **Thought:** I need more information about Amazon.
    **Action:** `get_recent_stock_news(AMZN)`

3.  **Thought:** I still need more information.
    **Action:** `get_financial_statements(AMZN)`

4.  **Thought:** I now have all the information to make a recommendation.

Here's an illustration of the Langchain instructions for the Agent:

*Please replace this placeholder image with the actual image URL of your `stock_prompt.png`*

### Elaboration Feature

A key feature allows users to request further elaboration on specific parts of the agent's response. The agent maintains context of previous interactions, enabling it to provide more in-depth information on particular sections.

For example, if a user asks, "Can you elaborate more on market sentiment and include the name of the article you used to generate the answer?", the agent will adjust its output for the "Market Sentiment" section to include the requested details and source.

### User Interface

The application features an interactive web interface built with Streamlit, providing a clean and intuitive experience for users to input queries and receive recommendations.

Here's a glimpse of the user interface:

*Please replace this placeholder image with the actual image URL of your `user_interface.png`*

## Validation

The agent generates well-reasoned recommendations and explanations, considering both the pros and cons of a given company. Initial reviews show accurate assessments of historical stock prices and data from financial reports. For a more comprehensive evaluation, future work would include backtesting the recommendations against actual market movements.

## Getting Started

## Requirements

Please refer to `requirements.txt` for a list of necessary packages and libraries.

### Setup Instructions

1.  **Set Your Google API Key:**
    -   Replace the following line in your code:
        ```python
        os.environ["GOOGLE_API_KEY"] = ''
        ```
    -   Insert your actual Google AI Studio API key in place of the empty quotes.

2.  **Set Your Finnhub API Key:**
    -   Locate the `get_recent_stock_news` function in your code.
    -   Replace the variable `api_key` with your actual Finnhub API key:
        ```python
        api_key = 'your_finhub_api_key'
        ```
    -   You can obtain a free Finnhub API key [here](https://finnhub.io/), if you don't already have one.

3.  **Launch the LLM App:**
    -   Use the following command to run the application and open the user interface in your web browser:
        ```bash
        streamlit run c:/Users/.../stock_recommender.py
        ```
    -   Make sure to replace the path with the correct location of `stock_recommender.py` on your machine.

### Additional Notes

* Ensure you have all required dependencies installed as listed in `requirements.txt`.
* If you encounter any issues, feel free to reach out for help.

## References

* **GitHub Repository:** [Mibrix's Project LLM](https://github.com/mibrix/Project_LLM)

* **Finnhub API:** [Market News API](https://finnhub.io/docs/api/market-news)

* **Streamlit:** [The fastest way to build and share data apps](https://streamlit.io/)

* **Langchain:** [Langchain Documentation](https://python.langchain.com/docs/concepts/#react-agents)

* **Fool.com Article:** [Can Amazon Stay Ahead of PDD's Temu and Shein in 2024?](https://www.fool.com/investing/2023/12/30/can-amazon-stay-ahead-of-pdds-temu-and-shein-in-20/)
