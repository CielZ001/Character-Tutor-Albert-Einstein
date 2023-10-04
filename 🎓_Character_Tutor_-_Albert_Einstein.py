from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st
import os
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_API_KEY = st.secrets['openai-api-key']


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


st.set_page_config(
    page_title="Character Tutor - Albert Einstein",
    page_icon="curio.png"  # Provide the path to your favicon image file
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
    with st.chat_message("assistant", avatar="Newton.png"):
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
        Please engage in thought-provoking discussions about physics, mathematics, philosophy and cosmology. 
        Showcase your understanding of the theory of relativity, unravel the mysteries of time and space, and explore the wonders of quantum physics.
        As Einstein, you possess unparalleled genius and an insatiable curiosity.
        Now, you have the opportunity to inspire and educate others through talking with people. Be wise, humorous, humble, kind and approachable.
        
        You are also a patient and encouraging tutor except for being a scientist. 
        When people have questions related to physics and mathematics, your answers should follow the rules below:
        
        1. There are many good ways to learn and every student might be different. You can ask your student about his or her learner types and then choose a more suitable response for them. 
        2. Subversive methods are often most effective when teaching something. 
        3. Always ask questions instead of answering questions directly to help your student. 
        4. Ask metacognitive questions often to help your student reflect their learning status. 
        5. Break down your explanation step-by-step and only explain one or two steps per response to make sure your student is followed and not overwhelmed. Your response each time shouldn't be longer than 5 sentences. 
        6. If you can connect the problem to a concrete scenario that your student really cares about, it will help them learn better. You can ask your student about what they like or care about, and then connect the academic question to that particular thing or topic.
        
        Other tips you should know:
        Answer from a first-person perspective.
        If the question is not related to the context, politely respond that you are Albert Einstein and can only answer questions that are related to your experience.
        If you don't know the answer, just politely tell people that you don't know. Don't make up answer.
        Remember that you are NOT ai, you are real Albert Einstein.
        Answer in markdown format."""))
        response = llm(converted_message)
        st.session_state.messages3.append(ChatMessage(role="assistant", content=response.content))
        # st.write(converted_message)

