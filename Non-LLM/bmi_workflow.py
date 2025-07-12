from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# define state
class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    category: str

# for 1st node
def calculate_bmi(state: BMIState) -> BMIState:
    # extract states
    weight = state['weight_kg']
    height = state['height_m']

    bmi = weight/(height**2)

    # update state
    state['bmi'] = round(bmi, 2)

    return state

# for 2nd node
def label_bmi(state: BMIState) -> BMIState:
    # extract state
    bmi = state['bmi']

    # update state
    if bmi < 18.5:
        state["category"] = "Underweight"
    elif 18.5 <= bmi < 25:
        state["category"] = "Normal"
    elif 25 <= bmi < 30:
        state["category"] = "Overweight"
    else:
        state["category"] = "Obese"

    return state

# define graph
graph = StateGraph(BMIState)

# add nodes to graph
graph.add_node('calculate_bmi', calculate_bmi)
graph.add_node('label_bmi', label_bmi)

# add edges to graph
graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', 'label_bmi')
graph.add_edge('label_bmi', END)


# compile graph
workflow = graph.compile()

# execute graph
intial_state = {'weight_kg':80, 'height_m':1.73}

final_state = workflow.invoke(intial_state)

print(final_state)