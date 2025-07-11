#please please active venv\Sripts\active before working on this :')
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(
    page_title="Therapy Bot",
    page_icon="🌿"
)

st.title("🌿Therapy Bot")

#get response
def get_response(query, chat_history):
    template = """
        You are a compassionate, non-judgmental therapy chatbot named "CalmMind". You are trained to listen actively, show empathy, and provide helpful but non-intrusive reflections or suggestions. You don't diagnose. Your main goal is to make the user feel heard and supported. Answer the following questions considering the history of the conversation:

        Chat history: {chat_history}

        User question: {user_question}
        """
    
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(api_key=st.secrets["api_keys"]["openai_api_key"])

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": query
    })



#conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

#user input
user_query = st.chat_input("Speak your mind🍃")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(ai_response))