import os

from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch
loadenv = load_dotenv()
print(os.getenv("GROQ_API_KEY"))

def get_symbol(name) -> str:
    """
    this function takes a company name and returns the symbol
    Args:
    :param name: str the name of the company
    :return:str the symbol of the company
    """
    if name == "Apple":
        return "AAPL"
    elif name == "Phidata":
        return "MSFT"
    else:
        raise ValueError("Unknown company name")

groq = Groq(id="llama-3.3-8b-versatile", model="llama2", api_key=os.getenv("GROQ_API_KEY"))

web_Agent = Agent(
    name = "web_search_agent",
    model = groq,
    tools = [GoogleSearch()],
    instructions=["Always use the web search tool to get the latest information"],
    show_tool_calls="true",
    markdown=True,
    verbose = True
)

financeAgent = Agent(
    model = groq,
    tools = [YFinanceTools(stock_price = True, analyst_recommendations = True, stock_fundamentals = True), get_symbol],
    instructions=["if you don't know the company symbol, please use the get_symbol tool for Phidata"],
    show_tool_calls="true",
    markdown=True,
    verbose = True)

agent_squad = Agent(
    model = groq,
    team =[web_Agent, financeAgent],
    instructions=["always include sources",
                 "use table format to display information about stocks" ],
    show_tool_calls=True,
    markdown=True
)

agent_squad.print_response("Summarize stock price of Apple and latest news")