def planner_prompt(user_prompt : str)->str:
  
  PLANNER_PROMPT = f"""
  
  You are the PLANNER agent. convert the user prompt into a complete engineering project.

  User Request : {user_prompt}
  
  """
  
  return PLANNER_PROMPT


def architect_prompt(plan : str)->str:
  
  ARCHITECT_PROMPT = f"""
  
  You are the ARCHITECT agent. Given this project plan, break it down into explicit engineering tasks.
  
  RULES:
  -For each file in the plan, create one or more IMPLEMENTATION TASKS.
  -In each task description:
   *Specify exactly what to implement.
   *Name the variable , functions, classes and components to be defined.
   *Mention how this task depends on or will be used by previous tasks.
   *Include integration details : imports, expected function signatures data flow.
  
  -Order tasks so that dependencies are implemneted first.
  -Each step must be SELF-contained but also carry FORWARD the relevant context.
  
  Project Plan:
  {plan}
  
  """
  
  return ARCHITECT_PROMPT

def coder_system_prompt()-> str:
  
  CODER_SYSTEM_PROMPT = """
  
  You are the coder agent.
  You are implementing a specific engineering task.
  You are given a task description, below, write the complete code for it
  
  """
  
  return CODER_SYSTEM_PROMPT