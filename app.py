import streamlit as st
from openai import OpenAI

# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
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
import time


class ChatBot:
    def __init__(self) -> None:
        self.set_up()
        self.chat_loop()
        # self.take_user_input()
        # self.display_messages()

    def prompt_chatbot(self, specific_paragraph: int = ""):
        prompt_path = "prompt_alter.txt"

        with open(prompt_path, "r") as file:
            full_prompt = file.read()
            paragraphs = full_prompt.split("\n\n")

        if specific_paragraph == "":
            return full_prompt

        elif specific_paragraph > len(paragraphs):
            return full_prompt

        else:
            return paragraphs[specific_paragraph]

    def set_up(self):
        self.bot_image = Image.open(f"images/co-thinker_logo.png")
        self.user_image = "👨‍💻"
        st.image(self.bot_image, width=110)
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
                SystemMessagePromptTemplate.from_template(self.prompt_chatbot(0)),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
        self.conversation = LLMChain(
            llm=self.chat, prompt=prompt, memory=self.memory, verbose=True
        )
        # initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def chat_loop(self):
        # update the ui
        i = 0
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.markdown(message["content"])
                print(i)
                i += 1

        # actual chat loop
        if user_input := st.chat_input("enter your prompt"):
            st.session_state.messages.append(
                {"role": "user", "avatar": self.user_image, "content": user_input}
            )
            with st.chat_message("user", avatar=self.user_image):
                st.markdown(user_input)
                self.conversation({"question": user_input})

            with st.chat_message("assistant", avatar=self.bot_image):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = self.conversation.dict()["memory"]["chat_memory"][
                    "messages"
                ][1]["content"]
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "avatar": self.bot_image,
                        "content": full_response,
                    }
                )


if __name__ == "__main__":
    session = ChatBot()
