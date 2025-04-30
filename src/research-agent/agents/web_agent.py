from smolagents import tool, Tool, CodeAgent, OpenAIServerModel
from tavily import TavilyClient
from ..models import gpt41mini
import os
from dotenv import load_dotenv
load_dotenv(override=True)


@tool
def web_search(query: str) -> str:
    """Searches the web for your query.
    
    Args:
        query: Your query
    """
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    return str(response["results"])

class VisitWebpageTool(Tool):
    name = "visit_webpage"
    description = (
        "Visits a webpage at the given url and reads its content as a markdown string. "
        "Use this to browse webpages."
    )
    inputs = {
        "url": {
            "type": "string",
            "description": "The url of the webpage to visit.",
        },
    }
    output_type = "string"

    def forward(self, url: str) -> str:
        try:
            import re
            import requests
            from markdownify import markdownify
            from requests.exceptions import RequestException

            from smolagents.utils import truncate_content

        except ImportError as e:
            raise ImportError(
                "Please install the required packages: `uv sync`"
            ) from e
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            markdown_content = markdownify(response.text).strip()
            markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)  # Remove excessive newlines
            return truncate_content(markdown_content, 40000)  # Truncate to 40000 characters
        
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again later."
        except RequestException as e:
            return f"An error occurred while fetching the webpage: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

web_agent = CodeAgent(
    model=gpt41mini,
    tools=[web_search, VisitWebpageTool()],
    max_steps=10,
    name="web_agent",
    description="Runs web searches for you."
)
web_agent.logger.console.width = 66