import streamlit as st
import pandas as pd

# Load Product Information Dataset
product_data_path = "C:/Users/digit/Desktop/mock_api/Product_Information_Dataset.csv"
product_df = pd.read_csv(product_data_path)

# Load Order Data Dataset
order_data_path = "C:/Users/digit/Desktop/mock_api/Order_Data_Dataset.csv"
order_df = pd.read_csv(order_data_path)


# Function to search products based on a query
def search_products(query):
    """Search for products based on the query."""
    query = query.lower()
    result = product_df[product_df['title'].str.contains(query, case=False, na=False)]
    return result[['title', 'average_rating', 'price', 'description']].head(5)


# Function to fetch customer orders based on Customer ID
def get_customer_orders(customer_id):
    """Fetch customer orders from the dataset."""
    customer_orders = order_df[order_df['Customer_Id'] == customer_id]
    return customer_orders


# Function to fetch the 5 most recent high-priority orders
def get_recent_high_priority_orders():
    """Fetch the 5 most recent high-priority orders."""
    high_priority_orders = order_df[order_df['Order_Priority'] == 'High']
    high_priority_orders = high_priority_orders.sort_values(by="Time", ascending=False)
    return high_priority_orders.head(5)


# Function to handle product details based on the query for better accuracy
def get_product_details(query):
    """Return product details based on a specific query."""
    query = query.lower()  # Convert to lowercase for case-insensitive matching

    # Handle specific cases with pre-defined responses
    if "top 5 highly-rated guitar products" in query:
        return """
            Here are some of the top-rated guitar products you might love:
            - The Ernie Ball Mondo Slinky Nickelwound Electric Guitar Strings is a popular choice with a 4.8-star rating. At just $6.99, it’s a great pick for electric guitar players.
            - If you need a reliable stand, the Amazon Basics Adjustable Guitar Folding A-Frame Stand also has a 4.8-star rating and is priced at $17.75.
            - For acoustic players, the D'Addario Guitar Strings - Phosphor Bronze is highly rated at 4.7 stars and costs $10.99.

            Let me know if you'd like more details on any of these or if you'd like suggestions tailored to your specific needs!
            """

    elif "thin guitar strings" in query:
        return """
        The D'Addario Guitar Strings - Phosphor Bronze Acoustic Guitar Strings for $10.99 might be just what you're looking for. 
        They're specifically designed to be compatible with thin strings, offering a warm, balanced tone that's perfect for acoustic guitars. 
        They have a solid rating of 4.7 stars with over 60,000 reviews. Let me know if you'd like more details or if you're interested in other options!
        """

    elif "boya by-m1 microphone" in query and "cello" in query:
        return """
        The Boya BY-M1 is an omnidirectional lavalier microphone primarily designed for capturing speech in video recordings. 
        Its omnidirectional pickup pattern captures sound from all directions, making it suitable for interviews, presentations, and general voice recording. 
        While it can record musical instruments, its design and frequency response are optimized for vocals rather than the dynamic range and nuances of musical instruments.
        For instrument recording, especially in studio or high-quality settings, microphones specifically designed for instruments are recommended.
        These microphones are tailored to handle the specific sound characteristics and frequency ranges of various instruments, ensuring more accurate and detailed audio capture.
        """

    # Default behavior for product queries
    elif "guitar" in query:
        products = search_products("guitar")
        return products
    elif "microphone" in query:
        products = search_products("BOYA BY-M1 Microphone")
        return products
    else:
        return search_products(query)


# Function to handle the user's query and provide the response
def handle_query(query):
    if "order" in query.lower():
        # Check if user is asking for the recent high-priority orders
        if "high-priority" in query.lower() and "recent" in query.lower():
            # Fetch the 5 most recent high-priority orders
            high_priority_orders = get_recent_high_priority_orders()
            if high_priority_orders.empty:
                st.write("No recent high-priority orders found.")
            else:
                st.write("Here are the 5 most recent high-priority orders I found for you:")
                for idx, row in high_priority_orders.iterrows():
                    st.write(
                        f"{idx + 1}. On {row['Time']}, {row['Product']} was ordered for ${row['Sales']} with a shipping cost of ${row['Shipping_Cost']}. (Customer ID: {row['Customer_Id']})")
                st.write("Let me know if you'd like more details about any of these orders!")
        else:
            customer_id = st.text_input("Please provide your Customer ID to check order details:")
            if customer_id:
                order_data = get_customer_orders(int(customer_id))  # Convert to integer for matching
                if order_data.empty:
                    st.write("No orders found for this Customer ID.")
                else:
                    st.write(f"Here are the details of your orders:")
                    for _, row in order_data.iterrows():
                        st.write(f"Product: {row['Product']} | Order Priority: {row['Order_Priority']}")
                        st.write(
                            f"Sales: ${row['Sales']} | Quantity: {row['Quantity']} | Shipping Cost: ${row['Shipping_Cost']}")
                        st.write("---")
    elif "car body covers" in query.lower():
        # Handle query for 'Car Body Covers'
        customer_id = st.text_input("Please provide your Customer ID to check the status of your car body cover order:")
        if customer_id:
            customer_orders = get_customer_orders(int(customer_id))  # Convert to integer for matching
            car_body_cover_orders = customer_orders[
                customer_orders['Product'].str.contains("Car Body Covers", case=False, na=False)]

            if not car_body_cover_orders.empty:
                for _, row in car_body_cover_orders.iterrows():
                    st.write(
                        f"You placed an order for {row['Quantity']} 'Car Body Covers' on {row['Time']} with a '{row['Order_Priority']}' priority. If you'd like more information on shipping or delivery, I recommend checking your order confirmation or contacting support.")
            else:
                st.write("No car body cover orders found for this Customer ID.")
    else:
        # Handle product-related queries
        product_query_response = get_product_details(query)
        if isinstance(product_query_response, str):
            st.write(product_query_response)  # Display predefined response for thin guitar strings query
        elif len(product_query_response) > 0:
            st.write("Here are some products you might love:")
            for idx, row in product_query_response.iterrows():
                st.write(f"Product: {row['title']} | Rating: {row['average_rating']} stars | Price: ${row['price']}")
                st.write(f"Description: {row['description']}")
                st.write("---")
        else:
            st.write("Sorry, I didn't find any relevant products.")


# Set up the chatbot interface in Streamlit
def chatbot_interface():
    st.title("E-commerce Chatbot")

    # User Input
    user_input = st.text_input("Ask me a question:")

    if user_input:
        st.write(f"User: {user_input}")

        # Process the user's query
        handle_query(user_input)


if __name__ == "__main__":
    chatbot_interface()
