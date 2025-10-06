import os

from dotenv import load_dotenv
from langchain.globals import set_debug, set_verbose
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from prompts import architect_prompt, coder_system_prompt, planner_prompt
from states import Plan, TaskPlan
from tools import *

load_dotenv()

set_debug(True)
set_verbose(True)

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.1)

user_prompt = "Create a simple calculator web application "

prompt = planner_prompt(user_prompt)


def planner_agent(state: dict) -> dict:
    users_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(prompt)
    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))

    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan

    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    steps = state["task_plan"].implementation_steps
    current_step_idx = 0
    current_task = steps[current_step_idx]
    user_prompt = f"Task : {current_task.task_description}\n"

    system_prompt = coder_system_prompt()
    resp = llm.invoke(system_prompt + user_prompt)
    return {"code": resp.content}


graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_edge(start_key="planner", end_key="architect")
graph.add_edge(start_key="architect", end_key="coder")

graph.set_entry_point("planner")

agent = graph.compile()

if __name__ == "__main__":

    user_prompt = "create a simple calculator application"
    result = agent.invoke({"user_prompt": user_prompt})

    print(result)
