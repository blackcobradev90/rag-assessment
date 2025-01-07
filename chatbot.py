# chatbot.py
import streamlit as st
import pandas as pd
import re
from sentence_transformers import SentenceTransformer

# Load your datasets
product_df = pd.read_csv("C:/Users/digit/Desktop/mock_api/Product_Information_Dataset.csv")
order_df = pd.read_csv("C:/Users/digit/Desktop/mock_api/Order_Data_Dataset.csv")

# Load Sentence Transformers model (used for similarity comparison)
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')


# Function to fetch top-rated products in a category
def get_top_rated_products(category: str):
    filtered_products = product_df[product_df['categories'].str.contains(category, case=False, na=False)]
    sorted_products = filtered_products.sort_values(by='average_rating', ascending=False)
    top_products = sorted_products.head(5)

    if top_products.empty:
        return f"No top-rated products found for category '{category}'."

    response = f"Here are some of the top-rated {category} products:\n"
    for idx, row in top_products.iterrows():
        response += f"● {row['title']} - Rating: {row['average_rating']} | Price: ${row['price']} \n"

    return response


# Function to recommend products based on a specific need (e.g., thin guitar strings)
def recommend_product(product_description: str):
    # Extract products matching the description (e.g., 'thin guitar strings')
    recommended_products = product_df[product_df['title'].str.contains(product_description, case=False, na=False)]

    if not recommended_products.empty:
        product_row = recommended_products.iloc[0]  # Taking the first match
        return f"The {product_row['title']} might be a good fit for you. It is priced at ${product_row['price']} with a rating of {product_row['average_rating']} stars."
    else:
        return f"Sorry, I couldn't find any products matching '{product_description}'."


# Function to get the most recent order details by Customer ID
def get_order_details(customer_id: int):
    customer_orders = order_df[order_df['Customer_Id'] == customer_id]

    if customer_orders.empty:
        return f"No orders found for Customer ID {customer_id}."

    latest_order = customer_orders.sort_values(by='Time', ascending=False).iloc[0]
    response = f"Here's your most recent order:\n"
    response += f"Order Date: {latest_order['Time']}\n"
    response += f"Product: {latest_order['Product']}\n"
    response += f"Sales Amount: ${latest_order['Sales']}\n"
    response += f"Shipping Cost: ${latest_order['Shipping_Cost']}\n"
    response += f"Order Priority: {latest_order['Order_Priority']}\n"

    return response


# Function to fetch 5 most recent high-priority orders
def get_high_priority_orders():
    high_priority_orders = order_df[order_df['Order_Priority'] == 'Critical']
    high_priority_orders = high_priority_orders.sort_values(by='Time', ascending=False).head(5)

    if high_priority_orders.empty:
        return "No high-priority orders found."

    response = "Here are the 5 most recent high-priority orders:\n"
    for idx, order in high_priority_orders.iterrows():
        response += f"● On {order['Time']}, {order['Product']} was ordered for ${order['Sales']} with a shipping cost of ${order['Shipping_Cost']}.\n"

    return response


# Main Streamlit interface
st.title('E-commerce Chatbot')
user_query = st.text_input('Ask your question:')

# User query processing
if user_query:
    if "top-rated" in user_query.lower() or "best" in user_query.lower():
        # Handle top-rated product queries (e.g., "What are the top 5 highly-rated guitar products?")
        category = re.findall(r"(guitar|microphone|phone|camera|headphone)", user_query.lower())
        if category:
            category = category[0]
            response = get_top_rated_products(category)
            st.write(response)
        else:
            st.write("Please specify the product category you're interested in (e.g., guitar, microphone).")

    elif "recommend" in user_query.lower() or "good product" in user_query.lower():
        # Handle specific product recommendation queries
        product_description = re.findall(r"(thin guitar strings|acoustic guitar strings|microphone|headphones)",
                                         user_query.lower())
        if product_description:
            product_description = product_description[0]
            response = recommend_product(product_description)
            st.write(response)
        else:
            st.write("Sorry, I couldn't understand the product you're referring to.")

    elif "order" in user_query.lower():
        # Handle order-related queries (e.g., last order, high-priority orders)
        customer_id_match = re.search(r'\d+', user_query)
        if customer_id_match:
            customer_id = int(customer_id_match.group(0))
            if "last order" in user_query.lower():
                response = get_order_details(customer_id)
            elif "high-priority" in user_query.lower():
                response = get_high_priority_orders()
            else:
                response = "Please specify whether you want to see 'last order' or 'high-priority orders'."
            st.write(response)
        else:
            st.write("Please provide your Customer ID to proceed with order-related queries.")

    else:
        st.write("Sorry, I couldn't understand your query. Please ask about products or orders.")
