from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph,START,END # framework that helps you to design the flow of tasks in your application
                                       #  using a graph


# We now create an AgentState - shared data structure that keeps track of information as your application runs.
class AgentState(TypedDict):
    number1 : int
    operation : str
    number2 : int
    finalNumber : int


def adder(state:AgentState) -> AgentState:
    """ This node adds the 2 numbers """

    state["finalNumber"] = state["number1"] + state["number2"]

    return state

def substractor(state:AgentState) -> AgentState:
    """ This node substracts the 2 numbers """

    state["finalNumber"] = state["number1"] - state["number2"]

    return state

def decide_next_node(state:AgentState) -> AgentState:
    """ This node will select the next node of the graph """

    if state["operation"] == "+":
        return "addition_operation"
    elif state["operation"] == "-":
        return "substraction_operation"


graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("substract_node", substractor)
graph.add_node("router", lambda state:state) # passthrough function

graph.add_edge(START,"router")
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        #Edge: Node
        "addition_operation" : "add_node",
        "substraction_operation": "substract_node"
    }
)

graph.add_edge("add_node", END)
graph.add_edge("substract_node", END)

app = graph.compile()


from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

inital_state_1 = AgentState(number1 = 10, operation="-", number2 = 5)
print(app.invoke(inital_state_1))