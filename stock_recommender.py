import os
import requests
import base64
import yfinance as yf
from langchain.agents import Tool
from langchain_community.callbacks import StreamlitCallbackHandler
import streamlit as st
import warnings
from langchain_google_genai import ChatGoogleGenerativeAI
warnings.filterwarnings("ignore")
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, MessagesState



if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = ''


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('bcg_light.png')
st.header('Stock Recommendation System')

st.sidebar.write('This tool provides recommendations based on the RAG:')
lst = ['Fetch Historic Data on Stock', 'Get Financial Statements', 
'Use Finnhub for Stock News', 'LLM ReAct based Verbal Analysis',
 'Output Recommendation: Buy, Sell, or Hold with Justification',
 '''Ask for Detailed Explanation by using one of the following keywords in the prompt "clarify", "explain", "what do you mean",
  "elaborate" e.g. elaborate more on the Market Sentiment Part and make a reference to a concrete article''',]

s = ''
for i in lst:
    s += "- " + i + "\n"

st.sidebar.markdown(s)


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    request_timeout=120,
)

# Get Historical Stock Closing Price for Last 1 Year
def get_stock_price(ticker):
    if "." in ticker:
        ticker = ticker.split(".")[0]
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    df = df[["Close", "Volume"]]
    df.index = [str(x).split()[0] for x in list(df.index)]
    df.index.rename("Date", inplace=True)
    return df.to_string()



# Get Recent Stock News using Finhub
def get_recent_stock_news(ticker):
    api_key = ''  # Replace with your actual Finhub API key

    url = f'https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2023-01-01&to=2023-12-31&token={api_key}'

    # Make a request to the Finhub API
    response = requests.get(url).json()

    # Check if the response is valid and contains articles
    if not isinstance(response, list):
        return "No recent news found or invalid ticker."
    
    if len(response) == 0:
        return "No recent news found or invalid ticker."
    
    # Extract news articles with links
    news_articles = [
        f"{article['datetime']} {article['headline'].replace('$', 'dollar')} {article['summary'].replace('$', 'dollars')} [Read more]({article['url']})\n"
        for article in response if 'headline' in article and 'summary' in article and 'url' in article
    ]
    
    if not news_articles:
        return "No recent news found or invalid ticker."
    
    return ' '.join(news_articles)



def get_financial_statements(ticker):
    try:
        # Remove anything after "." in the ticker, like 'AAPL.US'
        if "." in ticker:
            ticker = ticker.split(".")[0]

        # Fetch company data
        company = yf.Ticker(ticker)
        balance_sheet = company.balance_sheet
        
        # Check if the balance sheet data exists
        if balance_sheet is None or balance_sheet.empty:
            raise ValueError(f"No balance sheet data found for {ticker}")
        
        # Limit the balance sheet to the first 3 columns if more are available
        if balance_sheet.shape[1] > 3:
            balance_sheet = balance_sheet.iloc[:, :3]
        
        # Drop rows with any missing values
        balance_sheet = balance_sheet.dropna(how="any")
        balance_sheet_str = balance_sheet.to_string()
        
        return balance_sheet_str

    except Exception as e:
        print(f"Error retrieving financial statements for {ticker}: {e}")
        return None


# Define your agent configuration
system_message = SystemMessage(content="You are a helpful assistant.")

# Adding predefined evaluation steps in the agent Prompt
stock_prompt="""You are a financial advisor. Give stock recommendations for given query. You are not allowed to use dollar sign ($) in your answer but you can use the word dollar(s).

{tools}
Question: the input question you must answer
Thought: you should always think about what to do.
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: make an observation about the action you took.
... (this Thought/Action/Action Input/Observation can repeat N times, if Thought is empty go to the next Thought and skip Action/Action Input and Observation)
Thought: I now know the final answer
Final Answer: Broke down the analysis into five distinct steps and write two paragraphs of text for each of the category : Recent Performance, Market Sentiment, Financial Health, Growth Potential, Risk and Overall advice either buy, sell or hold. (in the text use concrete prices, percentages, and reasons to justify your answer, and make references to concrete news articles): 
Begin!

Question: {input}
Thought:{agent_scratchpad}"""


# Define tools with valid names
tools = [
    Tool(
        name="get_stock_historical_price",  # Changed to valid name format
        func=get_stock_price,
        description="Fetch the historical price data for a stock ticker."
    ),
    Tool(
        name="get_recent_news",  # Changed to valid name format
        func=get_recent_stock_news,
        description="Retrieve recent news articles related to a company's stock."
    ),
    Tool(
        name="get_financial_statements",  # Changed to valid name format
        func=get_financial_statements,
        description="Obtain the financial statements for a company."
    )
]


prompt= ChatPromptTemplate.from_template(stock_prompt)


agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    # max_iterations=17,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
)

# Define the function to check if the user is asking for clarification
def is_clarification_request(user_input):
    clarification_keywords = ["clarify", "explain", "what do you mean", "elaborate"]
    return any(keyword in user_input.lower() for keyword in clarification_keywords)

# Initialize memory and workflow
memory = MemorySaver()
workflow = StateGraph(state_schema=MessagesState)

# Define the function that the workflow will use to call the agent
def call_model(state: MessagesState):
    system_prompt = (
        "You are a helpful assistant. "
        "Answer all questions to the best of your ability."
    )
    # Construct the messages using memory and input
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    # Call the agent_executor with the conversation history
    response = agent_executor.invoke({"input": messages})
    return {"messages": response["output"]}

# Add the model node and workflow configuration
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# Compile the workflow with the memory checkpointer
app = workflow.compile(checkpointer=memory)

# Initialize session state for chat history and last response tracking
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_ai_response" not in st.session_state:
    st.session_state.last_ai_response = ""  # Track last AI response

# Display chat history first (managed by memory now)
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Input from user
if prompt := st.chat_input():
    # Append user's input to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Display the user's message (new content)
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        try:
            # Check if the user is asking for clarification
            if is_clarification_request(prompt) and st.session_state.last_ai_response:
                # User is asking for clarification on the last AI response
                clarification_prompt = f"User asked: ({prompt}).   Can you clarify it based on your previous response: {st.session_state.last_ai_response}?"
                input_message = HumanMessage(content=clarification_prompt)
            else:
                # Regular query, use the user's input
                input_message = HumanMessage(content=prompt)

            # Invoke the workflow with the latest user input or clarification request
            response = app.invoke(
                {"messages": [input_message]}, 
                config={"configurable": {"thread_id": "1"}}  # Thread id to manage conversation
            )

            # Extract the assistant's response from memory and append it to chat history
            assistant_response = response["messages"][-1].content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            st.session_state.last_ai_response = assistant_response  # Track the last response

            # Display the assistant's response (new content)
            st.write(assistant_response)

        except Exception as e:
            # In case of error, display it and append to chat history
            error_message = f"Error: {e}"
            st.session_state.chat_history.append({"role": "assistant", "content": error_message})
            st.write(error_message)
