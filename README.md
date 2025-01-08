
# Chatbot with mock_api

This project implements a chatbot capable of answering product-related and order-related queries. It uses machine learning models and embeddings for accurate information retrieval and text generation. The chatbot queries two datasets (Product Information Dataset and Order Data Dataset), fetches information using a mock API, and generates responses using a language model.


## Features

•	Product Query: Answer questions related to product information (e.g., ratings, price, and categories).
•	Order Query: Fetch order details, including customer-related data such as the most recent order, order priority, and shipping costs.
•	Integration with Mock API: Fetch order data using a mock FastAPI-based API.
•	Embedding-based Query Processing: Uses embeddings to process queries efficiently.
•	Text Generation: Generates context-aware responses using pre-trained LLM models.


## Project Setup

Follow these steps to set up and run the project locally.

## Prerequisites

•	Python 3.7 or higher
•	Streamlit (for the frontend)
•	Hugging Face's transformers library (for using LLMs like distilgpt2 or similar models)
•	FastAPI (for the mock API)


## Step 1 : Clone the repository

First, clone this repository to your local machine:


## Step 2: Set up a virtual environment
Create a virtual environment to isolate the project dependencies:
code
python -m venv myenv
Activate the virtual environment:

•	On Windows:
code
myenv\Scripts\activate
•	On Linux/Mac:
code
source myenv/bin/activate


## Step 3: Install dependencies
Install the required dependencies using pip:
Code:

#### pip install streamlit transformers fastapi pandas requests scikit-learn faiss-cpu

## Step 4: Set up the API
In the mock_api.py file, you have endpoints that fetch order data. Make sure your CSV file paths for the datasets are correct.
Run the FastAPI server by executing the following command in the mock_api directory:
# code
uvicorn mock_api:app --reload

This will start the FastAPI server locally on http://localhost:8000. Make sure it’s running before interacting with the chatbot.


## Step 5: Run the Streamlit App
To run the chatbot application, run the following command:
# code
streamlit run chatbot.py

This will open the Streamlit interface in your browser at http://localhost:8501.

## How to Use the Chatbot
Once the Streamlit app is running, you will see an interactive interface where you can:

1.	Select the Type of Query: Choose between "Product Query" or "Order Query."

2.	Ask Your Query: Type your question in the input box.

o	Product Query examples:

	What’s a good product for thin guitar strings?
	What are the top-rated electric guitars?

o	Order Query examples:

	What is the status of my last order?
	Fetch 5 most recent high-priority orders.

3.	Get Responses: The chatbot will fetch relevant data from the datasets or API and generate responses based on your query.



