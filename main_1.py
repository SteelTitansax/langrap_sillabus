from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph # framework that helps you to design the flow of tasks in your application
                                       #  using a graph

# We now create an AgentState - shared data structure that keeps track of information as your application runs.
class AgentState(TypedDict):
    values : List[int]
    name : str
    result : str


def process_values(state: AgentState) -> AgentState:
    """" This function handles multiple different inputs """
    state['result'] = f"Hey there {state["name"]}! , your sum = {sum(state["values"])}"
    print(state)
    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))

answers = app.invoke({"values" : {1,2,3,4},"name": "Bob"})

print(answers['result'])

