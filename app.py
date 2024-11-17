import streamlit as st
import requests
import json
from typing import Dict, Any
import time

# Custom CSS to enhance the UI
def apply_custom_css():
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #ffffff;  /* Set background color to white */
            color: black;  /* Ensure text is black */
        }
        
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        .search-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .result-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            color: black;  /* Ensure text inside results is black */
        }
        
        .source-link {
            color: #4a90e2;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .source-link:hover {
            color: #357abd;
        }
        
        .loading-spinner {
            text-align: center;
            padding: 2rem;
        }
        
        .stButton>button {
            width: 100%;
            background-color: #4a90e2;
            color: white;
            height: 3rem;
            transition: background-color 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #357abd;
        }
        
        .error-message {
            background-color: #ffe6e6;
            color: #dc3545;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .stMarkdown, .stText, .stHeader, .stSubheader, .stCode {
            color: black;  /* Ensure text is black across various elements */
        }
        </style>
    """, unsafe_allow_html=True)

def query_backend(query: str) -> Dict[str, Any]:
    """Send query to backend with error handling and retry logic."""
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://backend-server-ffo7.onrender.com/query",
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=50
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                st.error(f"Error connecting to backend service: {str(e)}")
                return {"error": "Service unavailable"}
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff

def display_answer(answer: str):
    """Display the answer with custom styling."""
    st.markdown(
        f"""
        <div class="result-container">
            <h3>📝 Answer</h3>
            <p>{answer}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_sources(sources: list):
    """Display sources with custom styling."""
    st.markdown(
        """
        <div class="result-container">
            <h3>🔍 Sources</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    for idx, source in enumerate(sources, 1):
        st.markdown(
            f"""
            <div style="margin: 0.5rem 0;">
                {idx}. <a href="{source}" target="_blank" class="source-link">{source}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    st.set_page_config(
        page_title="AI-Powered Search Assistant",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Main header
    st.markdown(
        """
        <div class="main-header">
            <h1>🔍 AI-Powered Search Assistant</h1>
            <p>Your intelligent companion for web research</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Search container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)

    # Create a form for input
    with st.form("search_form", clear_on_submit=True):
        query = st.text_input(
            "What would you like to know?",
            key="query",
            placeholder="Enter your question here..."
        )
        
        # Center the button
        button_col = st.columns([3, 1, 3])  # Create empty columns around the button for centering
        with button_col[1]:
            submit_button = st.form_submit_button(
                "🔍 Search",
                use_container_width=True  # This expands the button width inside the column
            )

    st.markdown('</div>', unsafe_allow_html=True)

    if submit_button and query:
        with st.spinner("🔄 Searching and analyzing..."):
            try:
                result = query_backend(query)
                
                if "error" in result:
                    st.markdown(
                        f"""
                        <div class="error-message">
                            ❌ {result["error"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    # Display the answer
                    display_answer(result["answer"])
                    
                    # Display sources
                    if "sources" in result:
                        display_sources(result["sources"])
            
            except Exception as e:
                st.markdown(
                    f"""
                    <div class="error-message">
                        ❌ An error occurred: {str(e)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()

