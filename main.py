import requests
import streamlit as st
import os

from datetime import datetime
import re

# Load environment variables


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
        .stimage > img {
            max-width: 100px;  
            height: auto;      
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
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "myend"

def run_flow(message: str) -> dict:
    try:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
        
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
        }
        
        headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
        response = requests.post(api_url, json=payload, headers=headers)
        response_json = response.json()
        
        # Check if response has the expected structure
        if (response_json and 
            'outputs' in response_json and 
            response_json['outputs'] and 
            response_json['outputs'][0] and 
            'outputs' in response_json['outputs'][0] and 
            response_json['outputs'][0]['outputs'] and 
            'results' in response_json['outputs'][0]['outputs'][0] and 
            'message' in response_json['outputs'][0]['outputs'][0]['results'] and 
            'text' in response_json['outputs'][0]['outputs'][0]['results']['message']):
            return response_json
        else:
            raise ValueError("Invalid response format from API")
            
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return {"outputs": [{"outputs": [{"results": {"message": {"text": "I apologize, but I encountered an error processing your request. Please try again."}}}]}]}

def main():
    # Initialize session states
    if 'current_stats' not in st.session_state:
        st.session_state.current_stats = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Sidebar
    with st.sidebar:
        st.image("logo.jpg", caption="404BrainNotFound")
        st.markdown("---")
        st.markdown("### About")
        st.write("This AI Social media analyzing tool was built for Level Super Mind Hackathon qualifying assignment. Developed by the team '404BrainNotFound'")
        st.markdown("---")
        
        st.markdown("### GitHub Repository")
        st.markdown("""
            <div style='text-align: ;'>
                <a href='https://github.com/ANIMANxd/' target='_blank' class='github-link'>
                    <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' 
                         width='50px' style='margin-bottom: 10px;'>
                    <br>
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.title("🤖 SocialMatrices")
    st.markdown("#### Your AI-Powered Social Media Assistant developed by Team 404BrainNotFound")
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Form for input
    with st.form(key="message_form"):
        message = st.text_area(
            "Message",
            placeholder="Type your prompt here...",
            height=100,
            key="message_input"
        )
        
        submit_button = st.form_submit_button("Send Message 🚀")
        
        if submit_button and message.strip():
            try:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": message})
                
                with st.spinner("🤔 Thinking..."):
                    response = run_flow(message)
                    if response:  # Check if response exists
                        response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                        if response_text:  # Check if response_text exists
                            # Extract statistics from the response
                            stats = extract_statistics(response_text)
                            if stats:
                                st.session_state.current_stats = stats
                            
                            # Add assistant response to chat history
                            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                    
                st.session_state.submitted = True
                st.rerun()
                
            except Exception as e:
                st.error("I apologize, but I encountered an error processing your request. Please try again.")
                print(f"Debug - Error details: {str(e)}")  # For debugging
    
    # Footer
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.markdown("📊 Developed by Team 404BrainNotFound")
    with footer_col2:
        st.markdown(f"🕒 Current Time: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()