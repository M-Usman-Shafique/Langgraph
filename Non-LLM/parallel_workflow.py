from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class BatsmanState(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int

    strike_rate: float
    boundary_pb: float
    boundary_percent: float
    summary: str

def calculate_sr(state: BatsmanState):
    strike_rate = (state['runs']/state['balls'])*100

    return {'strike_rate': strike_rate} # partial update

def calculate_bpb(state: BatsmanState):
    boundary_pb = state['balls']/(state['fours'] + state['sixes'])

    return {'boundary_pb': boundary_pb}

def calculate_boundary_percent(state: BatsmanState):
    boundary_percent = (((state['fours'] * 4) + (state['sixes'] * 6))/state['runs'])*100

    return {'boundary_percent': boundary_percent}

def summary(state: BatsmanState):
    summary = f"""
Strike Rate - {state['strike_rate']} \n
Balls per boundary - {state['boundary_pb']} \n
Boundary percent - {state['boundary_percent']}
"""

    return {'summary': summary}

graph = StateGraph(BatsmanState)

graph.add_node('calculate_sr', calculate_sr)
graph.add_node('calculate_bpb', calculate_bpb)
graph.add_node('calculate_boundary_percent', calculate_boundary_percent)
graph.add_node('summary', summary)

# edges
graph.add_edge(START, 'calculate_sr')
graph.add_edge(START, 'calculate_bpb')
graph.add_edge(START, 'calculate_boundary_percent')

graph.add_edge('calculate_sr', 'summary')
graph.add_edge('calculate_bpb', 'summary')
graph.add_edge('calculate_boundary_percent', 'summary')

graph.add_edge('summary', END)

workflow = graph.compile()

intial_state = {
    'runs': 100,
    'balls': 50,
    'fours': 6,
    'sixes': 4
}

workflow.invoke(intial_state)