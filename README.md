# Langchain Chat-CSV with OpenAI (Tutorial)
> You can find the step-by-step video tutorial to build this application [on YouTube](https://youtu.be/tjeti5vXWOU).

This is a Python application that enables you to load a CSV file and ask questions about its contents using natural language. The application leverages Language Models (LLMs) to generate responses based on the CSV data. The LLM will only provide answers related to the information present in the CSV.

## How it works

The application reads the CSV file and processes the data. It utilizes OpenAI LLMs alongside with Langchain Agents in order to answer your questions. The CSV agent then uses tools to find solutions to your questions and generates an appropriate response with the help of a LLM.

The application employs Streamlit to create the graphical user interface (GUI) and utilizes Langchain to interact with the LLM.

## Installation

To install the repository, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Additionally, you need to obtain an OpenAI API key and add it to the `.env` file.

## Usage

To use the application, execute the `agents.py` file using the Streamlit CLI. Make sure you have Streamlit installed before running the application. Run the following command in your terminal:

```
streamlit run agents.py
```

## How the AI Agent Works

This application uses a LangChain Pandas DataFrame Agent to enable natural language querying of CSV files using OpenAI’s GPT model.

When a CSV file is uploaded, it is converted into a pandas DataFrame. The LangChain agent connects this DataFrame to a language model (GPT-3.5) so users can ask questions in plain English about the dataset.

The agent interprets the user's question, generates the corresponding pandas code, executes it on the DataFrame, and returns the result as a readable answer.

### Key Features

- Translates natural language into pandas code.
- Executes the code on the uploaded CSV data.
- Handles parsing errors and displays results in a user-friendly way.
- Supports a wide range of queries: filtering, aggregating, counting, grouping, and more.

The agent makes it possible to explore and analyze data without writing any code, simply by asking questions.

| LangChain CSV Agent with OpenAI | Streamlit prototype using `create_pandas_dataframe_agent` for uploading and querying CSVs. | [View Demo](https://drive.google.com/file/d/14DQc-aMyZuPqHDyI9S5ongd_6D-fPTwW/view?usp=drive_link) |