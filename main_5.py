from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph # framework that helps you to design the flow of tasks in your application
                                       #  using a graph


# We now create an AgentState - shared data structure that keeps track of information as your application runs.
class AgentState(TypedDict):
    name : List[int]
    age : str
    skills: List[str]
    final : str


def first_node(state:AgentState) -> AgentState:
    """ This is the first node of our sequence"""

    state["final"] = f"Hi {state["name"]}. "
    return state

def second_node(state:AgentState) -> AgentState:
    """ This is the second node of our sequence"""

    state["final"] += f"You are {state["age"]} years old!"
    return state

def third_node(state:AgentState) -> AgentState:
    """ This is the second node of our sequence"""
    skills_str = ", ".join(state["skills"])
    state["final"] += f"You skills are {skills_str} "
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)


graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")

graph.set_finish_point("third_node")

app = graph.compile()

from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
skills = {"coding", "math", "problem solving", "search", "analysis"}
answers = app.invoke({"name": "Charlie", "age":38,"skills":skills})

print(answers['final'])


