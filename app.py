import streamlit as st
from openai import OpenAI
import openai

from PIL import Image
import time


class ChatBot:
    def __init__(self) -> None:
        self.set_up()
        self.chat_loop()
        # self.take_user_input()
        # self.display_messages()

    def prompt_chatbot(self, specific_paragraph: int = ""):
        prompt_path = "prompt.txt"

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
        self.client = openai.Client(api_key=st.secrets["OPENAI_API_KEY"])
        # streamlit set up
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        self.bot_image = ""
        self.user_image = "👨‍💻"

        # st.image(self.bot_image, width=110)
        # st.image("🐓")
        st.title("Snark-o bot")
        st.header("A gpt clone for when you are feeling a little bit too cocky.")
        st.caption("You can start by introducing yourself or asking any question.")

        # initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def check_run(self, client, thread_id, run_id):
        while True:
            # Refresh the run object to get the latest status
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

            if run.status == "completed":
                print(f"Run is completed.")
                break
            elif run.status == "expired":
                print(f"Run is expired")
                break
            else:
                print(f"OpenAI: Run is not yet completed. Waiting...{run.status} ")
                time.sleep(3)

    def chat_loop(self):
        # call the assistant
        assistant = self.client.beta.assistants.create(
            name="Perspective_Circle",
            instructions="""
            Be helpful at answering the user's questions, but always be snarky.
            Every time you answer the user, question their intelligence or their looks.
            If the user gives you their name, make a joke about it after greeting them.
            """,
            model="gpt-4-1106-preview",
        )
        thread = self.client.beta.threads.create()

        # update the ui
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.markdown(message["content"])

        # actual chat loop
        if user_input := st.chat_input("type here"):
            st.session_state.messages.append(
                {"role": "user", "avatar": self.user_image, "content": user_input}
            )
            with st.chat_message("user", avatar=self.user_image):
                st.markdown(user_input)
                # send and retrieve msg to assistant
                msg = self.client.beta.threads.messages.create(
                    thread_id=thread.id, role="user", content=user_input
                )
                run = self.client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=assistant.id,
                )
                self.check_run(self.client, thread.id, run.id)
                all_msg = self.client.beta.threads.messages.list(thread_id=thread.id)
                # self.conversation({"question": user_input})

            with st.chat_message("assistant", avatar=self.bot_image):
                message_placeholder = st.empty()
                full_response = ""

                assistant_response = all_msg.data[0].content[0].text.value
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
