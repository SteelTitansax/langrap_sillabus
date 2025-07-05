from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

# Variables de entorno para Azure OpenAI
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # Ej: "https://mi-recurso-openai.openai.azure.com/"
azure_openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # Nombre del deployment en Azure

llm = ChatOpenAI(
    model="gpt-4o",  # modelo que tienes desplegado en Azure
    openai_api_key=azure_openai_api_key,
    openai_api_base=azure_openai_endpoint,
    openai_api_type="azure",
    openai_api_version="2023-05-15",  # asegúrate de que coincide con la versión que usas
    deployment_name=azure_openai_deployment_name,
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
