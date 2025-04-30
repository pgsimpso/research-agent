from smolagents import OpenAIServerModel
import os

gpt4o = OpenAIServerModel(
    model_id="openai/gpt-4o",
    api_key=os.getenv("GITHUB_TOKEN"),
    api_base="https://models.github.ai/inference",
    
)

gpt41mini=OpenAIServerModel(
    model_id="openai/gpt-4.1-mini",
    api_key=os.getenv("GITHUB_TOKEN"),
    api_base="https://models.github.ai/inference",
    max_completion_tokens=8096,
)