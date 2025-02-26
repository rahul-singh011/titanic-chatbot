import streamlit as st
import requests
import json
from PIL import Image
import base64
from io import BytesIO
import io

st.set_page_config(
    page_title="Titanic Dataset Chat Assistant",
    page_icon="🚢",
    layout="wide"
)

# custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)


st.title("🚢 Titanic Dataset Chat Assistant")

# description
st.markdown("""
    Ask questions about the Titanic dataset! For example:
    - What percentage of passengers survived?
    - Show me a histogram of passenger ages
    - What was the average fare price?
    - Create a bar chart of survival by passenger class
""")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message["content"]:
            image_bytes = base64.b64decode(message["content"]["image"])
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image)
        else:
            st.markdown(message["content"])


if prompt := st.chat_input("Ask me about the Titanic dataset..."):

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"question": prompt},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()["response"]
                    
                    if isinstance(result, dict) and "image" in result:
                        image_bytes = base64.b64decode(result["image"])
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result
                        })
                    else:
                      
                        st.write(result)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result
                        })
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the server: {str(e)}")


with st.sidebar:
    st.header("About")
    st.markdown("""
        This chatbot helps you analyze the Titanic dataset through natural language queries.
        
        **Available Features:**
        - Statistical analysis
        - Data visualization
        - Passenger information
        - Survival statistics
        
        **Sample Questions:**
        1. How many passengers survived?
        2. Show age distribution
        3. Compare survival rates by class
        4. Average fare by passenger class
    """) 