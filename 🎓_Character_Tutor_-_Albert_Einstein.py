from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st
import os
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_API_KEY = st.secrets['openai-api-key']
sys_prompt = st.secrets['prompt']


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


st.set_page_config(
    page_title="Character Tutor - Albert Einstein",
    page_icon="eins.png"  # Provide the path to your favicon image file
)


st.title("🎓 Character Tutor - Albert Einstein")


if "messages3" not in st.session_state:
    st.session_state.messages3 = [ChatMessage(role='assistant', content="""Hey there, young explorers!

I'm Albert, but some people call me Einstein. Do you like mysteries? I do too! I've spent a lot of time trying to figure out how the big, wide universe works, kind of like solving a giant puzzle. You might have heard about my idea, which says that everything, even time, can be a bit stretchy – just like silly putty! I love asking questions and getting curious about everything around us.

I've always believed that everyone, including you, can be a great thinker! So, are you ready to put on your thinking caps and discover some fun things about the world with me? 

Let's go on an adventure of imagination and wonder! 🌌🚀
    
""")]


for msg in st.session_state.messages3:
    # if msg.role in ["user", "assistant"]:
    if msg.role == "assistant":
        st.chat_message(msg.role, avatar="eins.png").write(msg.content)
    else:
        st.chat_message(msg.role).write(msg.content)
    # st.chat_message(msg.role).write(msg.content)


if prompt := st.chat_input():
    st.session_state.messages3.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant", avatar="eins.png"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(model_name= 'gpt-4', temperature=0.5, openai_api_key=OPENAI_API_KEY, streaming=True, callbacks=[stream_handler])
        converted_message = []
        for msg in st.session_state.messages3:
            # if msg.role == "System":
            #     converted_message.append(SystemMessage(content=msg.content))
            if msg.role == "user":
                converted_message.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                converted_message.append(AIMessage(content=msg.content))
        converted_message.append(SystemMessage(content="""
        You are one of history's greatest minds, Albert Einstein. 
{sys_prompt}"""))
        response = llm(converted_message)
        st.session_state.messages3.append(ChatMessage(role="assistant", content=response.content))
        # st.write(converted_message)

