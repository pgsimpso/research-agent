from tavily import TavilyClient
from smolagents import tool, Tool
import os

from .agents import manager_agent


manager_agent = manager_agent.manager_agent



def main():
    manager_agent.run("If you use GitHub for SCM in Harness Platform, do you lose out on any features?")



if __name__ == "__main__":
    main()
