from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

class ApplicantState(TypedDict):
    experience_years: int
    has_degree: bool
    has_skills: bool

    summary: str
    decision: str

def summarize_applicant(state: ApplicantState):
    summary = (
        f"Experience: {state['experience_years']} years, "
        f"Degree: {'Yes' if state['has_degree'] else 'No'}, "
        f"Skills: {'Yes' if state['has_skills'] else 'No'}"
    )
    return {'summary': summary}

def evaluate_application(state: ApplicantState) -> Literal["accept", "hold", "reject"]:
    if state['experience_years'] >= 5 and state['has_degree'] and state['has_skills']:
        return "accept"
    elif state['experience_years'] >= 2 and (state['has_degree'] or state['has_skills']):
        return "hold"
    else:
        return "reject"

def accept(state: ApplicantState):
    return {'decision': "Accepted 🎉"}

def hold(state: ApplicantState):
    return {'decision': "Put on Hold ⏳"}

def reject(state: ApplicantState):
    return {'decision': "Rejected ❌"}

graph = StateGraph(ApplicantState)

graph.add_node('summarize_applicant', summarize_applicant)
graph.add_node('accept', accept)
graph.add_node('hold', hold)
graph.add_node('reject', reject)

graph.add_edge(START, 'summarize_applicant')
graph.add_conditional_edges('summarize_applicant', evaluate_application)
graph.add_edge('accept', END)
graph.add_edge('hold', END)
graph.add_edge('reject', END)

workflow = graph.compile()

initial_state = {
    'experience_years': 3,
    'has_degree': False,
    'has_skills': True
}

output = workflow.invoke(initial_state)
print(output)
