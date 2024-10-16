## Requirements

Please refer to `requirements.txt` for a list of necessary packages and libraries.

### Setup Instructions

1. **Set Your Google API Key:**
   - Replace the following line in your code:
     ```python
     os.environ["GOOGLE_API_KEY"] = ''
     ```
   - Insert your actual Google AI Studio API key in place of the empty quotes.

2. **Set Your Finhub API Key:**
   - Locate the `get_recent_stock_news` function in your code.
   - Replace the variable `api_key` with your actual Finhub API key:
     ```python
     api_key = 'your_finhub_api_key'
     ```
   - You can obtain a free Finhub API key [here](https://finnhub.io/), if you don't already have one. Or you can ask me for mine.

3. **Launch the LLM App:**
   - Use the following command to run the application and open the user interface in your web browser:
     ```bash
     streamlit run c:/Users/.../stock_recommender.py
     ```
   - Make sure to replace the path with the correct location of `stock_recommender.py` on your machine.

### Additional Notes

- Ensure you have all required dependencies installed as listed in `requirements.txt`.
- If you encounter any issues, feel free to reach out for help.
