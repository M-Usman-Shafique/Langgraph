from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description='Sentiment of the review')

structured_model = model.with_structured_output(SentimentSchema)

class ReviewState(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    response: str

def find_sentiment(state: ReviewState):
    prompt = f'For the following review find out the sentiment \n {state["review"]}'
    sentiment = structured_model.invoke(prompt).sentiment
    return {'sentiment': sentiment}

def check_sentiment(state: ReviewState) -> Literal["positive_response", "negative_response"]:
    if state['sentiment'] == 'positive':
        return 'positive_response'
    else:
        return 'negative_response'

def positive_response(state: ReviewState):
    response = f"Thank you for your positive feedback! We're glad you enjoyed the experience."
    return {"response": response}

def negative_response(state: ReviewState):
    response = f"We're sorry to hear about your experience. We'll look into the issue and get back to you."
    return {"response": response}

graph = StateGraph(ReviewState)

graph.add_node('find_sentiment', find_sentiment)
graph.add_node('positive_response', positive_response)
graph.add_node('negative_response', negative_response)

graph.add_edge(START, 'find_sentiment')
graph.add_conditional_edges('find_sentiment', check_sentiment)
graph.add_edge('positive_response', END)
graph.add_edge('negative_response', END)

workflow = graph.compile()

intial_state={
    'review': "This app keeps crashing every time I try to open it!",
}
workflow.invoke(intial_state)