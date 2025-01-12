import streamlit as st
import warnings
from langchain_community.vectorstores import Chroma
import sys
print(sys.path)  # Debug sys.path

from watsonx import *  # Import watsonx directly
from preprocessing import *

from prompts import *
from PIL import Image

warnings.filterwarnings("ignore")
proxy = "proxy.us.ibm.com:8080"
wx = WatsonxAI()
wx.connect()

# checking if collection exist, if no, create new collection
vectorstore = Chroma(persist_directory="./recordb", embedding_function=embeddings_model)


documents1 = [
    "CHATBOTFOOD.pdf"
]


if vectorstore._collection.count() == 0:
    for doc in documents1:
        print(f"Ingesting document: {doc}")
        vectorstore = vectorstore_ingest(doc)

img_url = "https://media.tenor.com/x5eWIvHg1yYAAAAM/sad-hamster-hampter.gif"

st.title(":writing_hand: Employment contract assistant (Understands Singlish)")
st.sidebar.image(img_url)
st.sidebar.title("Customise your responses")
model_id = st.sidebar.selectbox("Please select a model",("OLLAMA_GRANITE_3_1_8B_CODE_INSTRUCT"))

col_1,col_2 = st.sidebar.columns(2)

with col_1:
    temp = st.slider("Creativity of responses", 0.0,1.0,0.0,0.1)
    top_k = st.slider("Top K",0,100,1,1)
with col_2:
    max_token = st.slider("Length of response",0,10000,4000,100)
    repeat_penalty = st.slider("Repeat Penalty", 0.0,2.0,1.1,0.1)
enable_stream = st.sidebar.toggle("Enable Word Stream")

reset = st.sidebar.button("Reset",type="primary")
if reset:
    st.session_state.messages = []
    

if "tokens" not in st.session_state: 
    st.session_state['tokens'] = {
    "prompt_tokens":0,
    "response_tokens":0,
    "total_tokens":0
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

if prompt := st.chat_input("Ask me about anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        context = vectorstore.similarity_search(prompt, k=3)
        print(context)
        qna_prompt = question_prompt(context, prompt)
        print(qna_prompt)
        if (getattr(wx,model_id,None)==None):
            st.warning("Please select model")
            st.stop()
        stream = wx.watsonx_gen_stream(qna_prompt,getattr(wx,model_id,""),max_token,temp,top_k,repeat_penalty,enable_stream)
        response = st.write_stream(stream)

    st.sidebar.write("Prompt Tokens Used: ",st.session_state['tokens']['prompt_tokens'])
    st.sidebar.write("Response Tokens Used: ",st.session_state['tokens']['response_tokens'])
    st.sidebar.write("Total Tokens Used: ",st.session_state['tokens']['total_tokens'])

    st.session_state.messages.append({"role": "assistant", "content": response})

