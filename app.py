import streamlit as st
from openai import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)


from streamlit_chat import message

from PIL import Image


class ChatBot:
    def __init__(self) -> None:
        self.set_up()
        self.chat_loop()
        # self.take_user_input()
        # self.display_messages()

    def prompt_chatbot(self):
        prompt_path = "prompt.txt"
        with open(prompt_path, "r") as file:
            prompt = file.read()
        return prompt

    def set_up(self):
        self.image = Image.open(f"images/co-thinker_logo.png")
        st.image(self.image, width=110)
        st.title("Perspective Circle co-thinker")
        st.header(
            "A 5-step tool to facilitate sustainable decision making by embracing the perspective of multiple stakeholders."
        )
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        self.chat = ChatOpenAI(temperature=0)
        # set default model
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.memory.load_memory_variables({})
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    """
                    Act as an expert in sustainable decision-making and perspective-taking. 
                    Help the user evaluate the decision taking into consideration multiple stakeholders and trade-offs. 
                    Go step by step. Wait for the user's answers before moving on to the sequential steps.
                    """
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
        self.conversation = LLMChain(llm=self.chat, prompt=prompt, memory=self.memory)
        # initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def chat_loop(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("enter your prompt"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
                self.conversation({"question": user_input})
                print(self.conversation)

    def take_user_input(self):
        user_input = st.text_input("your message", key="user_input")

        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("thinking..."):
                response = self.chat(st.session_state.messages)
                print(response)
            st.session_state.messages.append(AIMessage(content=response.content))

    def display_messages(self):
        messages = st.session_state.get("messages", [])
        for i, stored_message in enumerate(messages[1:]):
            if i % 2 == 0:
                message(stored_message, is_user=True, key=str(i) + "_user")
            else:
                message(stored_message, is_user=True, key=str(i) + "_ai")


if __name__ == "__main__":
    session = ChatBot()
