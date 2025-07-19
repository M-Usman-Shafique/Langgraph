from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

# define states
class LLMState(TypedDict):
    question: str
    answer: str

# for node
def llm_QnA(state: LLMState) -> LLMState:
    # extract question from state
    question = state['question']

    # form a prompt
    prompt = f'Answer the following question {question}'

    # ask that question to the LLM
    answer = model.invoke(prompt).content

    # update the answer in the state
    state['answer'] = answer

    return state

# create graph
graph = StateGraph(LLMState)

# add nodes
graph.add_node('llm_QnA', llm_QnA)

# add edges
graph.add_edge(START, 'llm_QnA')
graph.add_edge('llm_QnA', END)

# compile graph
workflow = graph.compile()

intial_state = {'question': 'How far is moon from the earth?'}

# execute graph
final_state = workflow.invoke(intial_state)

print(final_state['answer'])
