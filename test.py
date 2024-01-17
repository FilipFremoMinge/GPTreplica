from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.chains import ConversationChain

llm = OpenAI(model_name="text-davinci-003", temperature=0, max_tokens=256)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, verbose=True, memory=memory)
