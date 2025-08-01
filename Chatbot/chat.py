from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

#==================================================================================================
    # No memory chatbot, because although we are appending messages into the state but after the complete execution of workflow, the previous state gets reset.
#==================================================================================================
class ChatState(TypedDict):
    # add_message reducer to append msgs into the list
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOpenAI()


def chat_node(state: ChatState):
    # take user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages)

    # response store state
    return {'messages': [response]}

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile()

while True:
    user_message = input("Type here: ")
    print("User:", user_message)

    if user_message.strip().lower() in ['exit', 'quit', 'bye']:
        break

    response = chatbot.invoke({ 'messages': [HumanMessage(content=user_message)]})
    print(response['messages'][-1].content)