import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import OpenAI

st.set_page_config(page_title="Ask your Data (CSV/JSON)")

MAX_ROWS = 500  # ✅ Limit the number of rows to prevent token overflow
MAX_COLUMNS = 20  # ✅ Limit the number of columns
MAX_CHARACTERS = 500  # ✅ Limit the number of characters per cell

def preprocess_dataframe(df):
    """Reduces the size of the dataframe to avoid exceeding token limits."""
    # ✅ Limit number of columns
    if df.shape[1] > MAX_COLUMNS:
        df = df.iloc[:, :MAX_COLUMNS]
    
    # ✅ Limit number of rows
    if df.shape[0] > MAX_ROWS:
        df = df.sample(n=MAX_ROWS, random_state=42)  # Sample instead of truncating

    # ✅ Truncate long text fields
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.slice(0, MAX_CHARACTERS)

    return df

def main():
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OPENAI_API_KEY is not set. Please check your .env file.")
        return

    st.success("OPENAI_API_KEY is set ✅")

    st.header("Ask your Data 📊 (CSV & JSON)")

    file = st.file_uploader("Upload a CSV or JSON file", type=["csv", "json"])
    
    if file is not None:
        try:
            file_name = file.name.lower()

            # ✅ Handle CSV files
            if file_name.endswith(".csv"):
                first_line = file.read(5000).decode("latin1").split("\n")[0]
                delimiter = ";" if ";" in first_line else ","
                file.seek(0)  # Reset pointer

                df = pd.read_csv(file, delimiter=delimiter, encoding="latin1")
                st.success(f"CSV file loaded with {df.shape[0]} rows and {df.shape[1]} columns ✅")

            # ✅ Handle JSON files
            elif file_name.endswith(".json"):
                df = pd.read_json(file)
                st.success(f"JSON file loaded with {df.shape[0]} rows and {df.shape[1]} columns ✅")

            else:
                st.error("Unsupported file format.")
                return

            # ✅ Reduce dataset size to prevent token overflow
            df = preprocess_dataframe(df)
            st.success(f"Dataset reduced to {df.shape[0]} rows and {df.shape[1]} columns for efficient querying ✅")

            # ✅ Create agent for querying the data
            agent = create_pandas_dataframe_agent(
                OpenAI(temperature=0),
                df,
                verbose=True,
                allow_dangerous_code=True  # Required for execution
            )

            # User input for queries
            user_question = st.text_input("Ask a question about your data:")

            if user_question:
                with st.spinner(text="In progress..."):
                    response = agent.run(user_question)
                    st.write(response)

        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    main()