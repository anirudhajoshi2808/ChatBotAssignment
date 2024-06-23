import streamlit as st
import requests

# Use Streamlit secrets to get the API key
openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.error("OpenAI API key is not set. Please check your secrets.")
    st.stop()

# Function to get response from OpenAI API
def get_openai_response(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Conversation starters
conversation_starters = [
    "Tell me about the Renaissance.",
    "Who was Cleopatra?",
    "What caused World War II?",
    "Describe the impact of the Industrial Revolution.",
    "How did the Roman Empire fall?"
]

st.title('History Chatbot')
st.write('Ask me anything about history!')

# Display conversation starters
st.write("Conversation Starters:")
for starter in conversation_starters:
    if st.button(starter):
        st.session_state.history.append({"role": "user", "content": starter})
        response = get_openai_response(starter)
        st.session_state.history.append({"role": "assistant", "content": response})

# Accept user input with chat input widget
prompt = st.chat_input("Ask a question about history...")
if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    response = get_openai_response(prompt)
    st.session_state.history.append({"role": "assistant", "content": response})

# Display chat history
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Optional: Clear chat history
if st.button('Clear Chat'):
    st.session_state.history = []
