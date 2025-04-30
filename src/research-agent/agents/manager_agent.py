from smolagents import Tool, OpenAIServerModel, CodeAgent
from . import web_agent
from ..models import gpt4o
from typing import Any
from smolagents.utils import make_image_url, encode_image_base64
import os

def check_reasoning(final_answer, agent_memory):
    final_answer

    prompt = (
        f"Here is a user-given task and the agent steps: {agent_memory.get_succinct_steps()}."
        "Please check that the reasoning process is correct: do they correctly answer the given task?"
        "First list reasons why yes/no, then write your final decision: PASS in caps lock if it is satisfactory, FAIL if it is not."
        "Don't be pedantic: if a reasonable person would agree that this solves the task, it should pass."
        "Also, any run that invents numbers should fail."
    )
    messages = [
        {
            "role": "user",
            "content": [
                { 
                    type: "text", 
                    "text": prompt,
                },
                # {
                #     "type": "image_url",
                #     "image_url": {"url": make_image_url(encode_image_base64)},
                # },
            ],
        }
    ]
    output = gpt4o(messages).content
    print("Feedback ", output)
    if "FAIL" in output:
        raise Exception(output)
    return True


web_agent = web_agent.web_agent

model=gpt4o
model.client.max_tokens = 8096

manager_agent = CodeAgent(
    model=model,
    tools=[],
    managed_agents=[web_agent],
    additional_authorized_imports=[
        "geopandas",
        "plotly",
        "plotly.express",
        "plotly.express.colors",
        "shapely",
        "json",
        "pandas",
        "numpy",
    ],
    planning_interval = 5,
    verbosity_level=2,
    final_answer_checks=[check_reasoning],
    max_steps=15,
)
manager_agent.logger.console.width = 66

manager_agent.visualize()