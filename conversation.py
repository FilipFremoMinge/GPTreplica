from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import configparser
import os


class ChatInstance:
    def __init__(self) -> None:
        self.set_environment()

    def get_access_info(self, storage_id: str):
        """Retrieves log-in information from config file.

        Args:
            storage_id (str): _description_

        Returns:
            str: stored_key, stored_environment, stored_url
        """

        config = configparser.ConfigParser()
        config.read(self.PARENT_FOLDER_PATH / "config.ini")
        try:
            stored_key = config["credentials"][f"{storage_id}_key"]
        except:
            stored_key = ""
        try:
            stored_env = config["credentials"][f"{storage_id}_env"]
        except:
            stored_env = ""
        try:
            stored_url = config["credentials"][f"{storage_id}_url"]
        except:
            stored_url = ""

        return stored_key, stored_env, stored_url

    def set_environment(self):
        """Sets necessary environment variables for ChatOpenAI LLM. If needed, sets up the variables
        for the vector stores as well."""

        (
            os.environ["OPENAI_API_KEY"],
            os.environ["OPENAI_API_TYPE"],
            os.environ["OPENAI_API_BASE"],
        ) = self.get_access_info("openai")

    def prompt_chatbot(self):
        prompt_path = "prompt.txt"
        with open(prompt_path, "r") as file:
            prompt = file.read()
        return prompt

    def get_response(self):
        chat = ChatOpenAI()
        messages = [SystemMessage(content=self.prompt_chatbot()), HumanMessage()]
