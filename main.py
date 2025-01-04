#main2.py

import requests
import streamlit as st
import os
from datetime import datetime
import pandas as pd
import json

# Configure Streamlit page
st.set_page_config(
    page_title="SocialMatrices",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the UI
st.markdown("""
    <style>
        .stTextInput > div > div > input {
            background-color: #f0f6f6;
        }
        .stTextArea > div > div > textarea {
            background-color: #202224;
        }
        .stButton > button {
            width: 100%;
            border-radius: 20px;
            height: 3em;
            background-color: #FF4B4B;
            color: white;
        }
        .stButton > button:hover {
            background-color: #FF6B6B;
            color: white;
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        .output-container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# API Configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "b90d566a-8de1-482e-a09f-81b7eb853eab"
FLOW_ID = "b2747eff-cc7c-463d-82d3-9934a20f40f2"
APPLICATION_TOKEN = "AstraCS:WpYXlHktWAZPJJCinEcBleAR:1126154f660ddf3ce9da55adcfddd492a167e84424e34a2bf314341f80d04fcd"
ENDPOINT = "myend"

LANGFLOW_ID1 = "b90d566a-8de1-482e-a09f-81b7eb853eab"
FLOW_ID1 = "7b2a0d66-c104-45be-9e6a-4da6265db76c"
APPLICATION_TOKEN1 = "AstraCS:GLsElqsSHgOLoxwdaLOOEKzA:5977dd882c8ae6dde5762fadc7235de17031e0bbc7ae270ddfb2ca6337c58d48"
ENDPOINT1 = ""

def run_flow(message: str) -> dict:
    """Execute the first API call for text response"""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return {"outputs": [[{"results": {"message": {"text": "Sorry, I encountered an error processing your request."}}}]]}

def call_langflow1(message: str) -> dict:
    """Execute the second API call for visualization data"""
    api_url1 = f"{BASE_API_URL}/lf/{LANGFLOW_ID1}/api/v1/run/{FLOW_ID1}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers1 = {
        "Authorization": f"Bearer {APPLICATION_TOKEN1}",
        "Content-Type": "application/json",
    }
    try:
        response1 = requests.post(api_url1, json=payload, headers=headers1)
        response1.raise_for_status()
        return response1.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Visualization API Error: {str(e)}")
        return {}

def process_message(message: str):
    """Process both text and visualization in a single function"""
    # Get text response
    text_response = run_flow(message)
    response_text = text_response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    
    # Get visualization data
    try:
        viz_response = call_langflow1(message)
        artifacts_message = viz_response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("artifacts", {}).get("message")
        
        if artifacts_message:
            try:
                json_data = json.loads(artifacts_message)
                return response_text, json_data
            except json.JSONDecodeError:
                return response_text, None
        return response_text, None
    except Exception as e:
        st.error(f"Visualization error: {str(e)}")
        return response_text, None

def display_chart(chart_type, data):
    """Display the appropriate chart based on the type and data"""
    try:
        categories = data.get("categories", [])
        values = data.get("values", [])
        
        if not categories or not values:
            st.warning("Invalid chart data received")
            return
            
        chart_data = pd.DataFrame({"Category": categories, "Value": values})

        if chart_type == "bar":
            st.bar_chart(chart_data.set_index("Category"))
        elif chart_type == "line":
            st.line_chart(chart_data.set_index("Category"))
        elif chart_type == "histogram":
            st.bar_chart(chart_data.set_index("Category"))
        elif chart_type == "pie":
            # Alternative display for pie chart
            st.write("Data for pie chart:")
            st.dataframe(chart_data)
        else:
            st.warning(f"Unsupported chart type: {chart_type}")
    except Exception as e:
        st.error(f"Error displaying chart: {str(e)}")

def main():
    # Initialize session states
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar
    with st.sidebar:
        st.image("logo.jpg", caption="404BrainNotFound")
        st.markdown("---")
        st.markdown("### About")
        st.write("This AI Social media analyzing tool was built for Level Super Mind Hackathon qualifying assignment. Developed by the team '404BrainNotFound'")
        st.markdown("---")
        st.markdown("### Team Members")
        st.write("""
            - [Aniruddha Bhide](https://github.com/ANIMANxd)
            - [Mahalaxmi Singh]()
            - [Nayaneka Yalavarthy](https://github.com/nayanekaa)
            - [Sanay Krishna](https://github.com/ReMochi)""")
        st.markdown("---")
        
        st.markdown("### GitHub Repository")
        st.markdown("""
            <div style='text-align: ;'>
                <a href='https://github.com/ANIMANxd/Social-Matrices' target='_blank' class='github-link'>
                    <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' 
                         width='50px' style='margin-bottom: 10px;'>
                    <br>
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.title("🤖 SocialMatrices")
    st.markdown("#### Your AI-Powered Social Media Assistant developed by Team 404BrainNotFound")
    st.markdown("### Instructions for Input Prompts:")
    st.write("""
        1. Please provide **clear** and **concise** prompts.
        2. If you want to **generate graphs**, make sure to mention **'generate graph'** in your prompt.
        3. You can request bar charts, line charts, or histograms by specifying that in the prompt.
    """)
    
    # Chat container
    chat_container = st.empty()
    
    # Form for input
    with st.form(key="message_form"):
        message = st.text_area(
            "Message",
            placeholder="Type your prompt here...",
            height=100,
            key="message_input"
        )
        
        submitted = st.form_submit_button("Send Message 🚀")
        
        if submitted and message.strip():
            with st.spinner("🤔 Processing your request..."):
                # Process message and get both text and visualization data
                response_text, viz_data = process_message(message)
                
                # Add messages to chat history
                st.session_state.chat_history.append({"role": "user", "content": message})
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                
                # Display visualization if available
                if viz_data:
                    chart_type = viz_data.get("chart_type")
                    chart_data = viz_data.get("data")
                    if chart_type and chart_data:
                        st.subheader("Generated Visualization")
                        display_chart(chart_type, chart_data)
    
    # Display chat history
    with chat_container.container():
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    
    # Footer
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.markdown("📊 Developed by Team 404BrainNotFound")
    with footer_col2:
        st.markdown(f"🕒 Current Time: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()