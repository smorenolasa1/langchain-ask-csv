import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("models/gemini-1.5-pro")

# UI setup
st.set_page_config(page_title="Ask Your CSV")
st.title("Ask about your CSV")

if not google_api_key:
    st.error("❌ GOOGLE_API_KEY not set. Please check your .env file.")
    st.stop()

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(
            uploaded_file,
            sep=";",
            encoding="latin1",
            quotechar='"',
            on_bad_lines="skip"
        )
        st.success(f"✅ CSV loaded with {df.shape[0]} rows and {df.shape[1]} columns!")

        # Show preview
        st.dataframe(df.head())

        user_question = st.text_input("Ask a question about your CSV:")

        if user_question:
            with st.spinner("Thinking..."):
                csv_snippet = df.head(1).to_csv(index=False)

                prompt = f"""
You are a helpful data analyst. A scientist has uploaded the following CSV data (only the first row with the first 10 columns is shown here):

{csv_snippet}

They asked the following question:
"{user_question}"

Please answer the question based on the data and explain your answer clearly. Use bullet points if needed. Be concise and precise.
"""
                response = model.generate_content(prompt)
                st.markdown("### 🤖 Answer")
                st.write(response.text)

    except Exception as e:
        st.error(f"❌ Error loading or processing CSV: {e}")