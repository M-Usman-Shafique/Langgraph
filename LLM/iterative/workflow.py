from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

generator_llm = ChatOpenAI(model='gpt-4o-mini')
evaluator_llm = ChatOpenAI(model='gpt-4o-mini')
optimizer_llm = ChatOpenAI(model='gpt-4o-mini')

class TweetEvaluation(BaseModel):
    evaluation: str  # "approved" or "needs_improvement"
    feedback: str

structured_evaluator_llm = evaluator_llm.with_structured_output(TweetEvaluation)

class TweetState(BaseModel):
    topic: str
    tweet: str
    evaluation: str = "needs_improvement"
    feedback: str
    iteration: int = 1
    max_iteration: int = 5

def generate_tweet(state: TweetState):
    prompt = [
        SystemMessage(content="You are a funny Twitter influencer."),
        HumanMessage(content=f"Write a humorous tweet about: {state.topic}")
    ]

    response = generator_llm.invoke(prompt).content
    return {'tweet': response}

def evaluate_tweet(state: TweetState):
    prompt = [
        SystemMessage(content="Evaluate the tweet based on humor, originality, and virality."),
        HumanMessage(content=f"Tweet: {state.tweet}")
    ]

    response = structured_evaluator_llm.invoke(prompt)
    return {'evaluation': response.evaluation, 'feedback': response.feedback}

def optimize_tweet(state: TweetState):
    prompt = [
        SystemMessage(content="Optimize the tweet for humor and virality based on feedback."),
        HumanMessage(content=f"Improve tweet: {state.tweet} with feedback: {state.feedback}")
    ]

    response = optimizer_llm.invoke(prompt).content
    return {'tweet': response, 'iteration': state.iteration + 1}

def route_evaluation(state: TweetState):
    if state.evaluation == 'approved' or state.iteration >= state.max_iteration:
        return 'approved'
    else:
        return 'needs_improvement'

graph = StateGraph(TweetState)
graph.add_node('generate', generate_tweet)
graph.add_node('evaluate', evaluate_tweet)
graph.add_node('optimize', optimize_tweet)

graph.add_edge(START, 'generate')
graph.add_edge('generate', 'evaluate')
graph.add_conditional_edges('evaluate', route_evaluation, {'approved': END, 'needs_improvement': 'optimize'})
graph.add_edge('optimize', 'evaluate')

workflow = graph.compile()

initial_state = {
    "topic": "funny tweet topic",
    "iteration": 1,
    "max_iteration": 3
}

result = workflow.invoke(initial_state)
