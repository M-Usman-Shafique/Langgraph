from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

# define states
class BlogState(TypedDict):
    title: str
    outline: str
    blog: str

# for 1st node
def create_outline(state: BlogState) -> BlogState:
    # extract title from state
    title = state['title']

    # call llm to generate an outline using title
    prompt = f'Generate a detailed outline for a blog on the topic - {title}'
    outline = model.invoke(prompt).content

    # update state
    state['outline'] = outline

    return state

def create_blog(state: BlogState) -> BlogState:
    # extract states
    title = state['title']
    outline = state['outline']

    # call llm to generate a blog using title and outline
    prompt = f'Write a detailed blog on the title - {title} using the follwing outline \n {outline}'
    blog = model.invoke(prompt).content

    state['blog'] = blog

    return state

# form graph
graph = StateGraph(BlogState)

# form nodes
graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_blog)

# form edges
graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', END)

workflow = graph.compile()
intial_state = {'title': 'Rise of AI in the World'}

final_state = workflow.invoke(intial_state)

print(final_state)
print(final_state['outline'])
print(final_state['blog'])
