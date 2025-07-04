from typing import TypedDict, Sequence, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
import agentql
import os
from datetime import datetime
from typing import List
import streamlit as st
import requests
from bs4 import BeautifulSoup

nvidia_api_key = st.secrets["NVIDIA_API_KEY"]
tavily_api_key = st.secrets["TAVILY_API_KEY"]
agentql_api_key = st.secrets["AGENTQL_API_KEY"]

os.environ["TAVILY_API_KEY"] = tavily_api_key
os.environ["AGENTQL_API_KEY"] = agentql_api_key

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", api_key=nvidia_api_key)
tavily_tool = TavilySearch(
    max_results=5,
    include_domains=["amazon.in", "flipkart.com", "croma.com"],
    search_depth="advanced"
)

def is_relevant(name: str, query: str, threshold: float = 0.6) -> bool:
    from difflib import SequenceMatcher
    name_lower = name.lower()
    query_lower = query.lower()
    return SequenceMatcher(None, name_lower, query_lower).ratio() >= threshold

class ReActState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def compare_prices(product_query: str) -> str:
    """
    Compare product prices from Amazon, Flipkart, and Croma using AgentQL and Tavily fallback.
    Returns product name, price, and link. Picks lowest price and shows it to the user.
    """
    import re

    def extract_price(price_str):
        try:
            clean = re.sub(r"[^\d]", "", str(price_str))
            return int(clean)
        except:
            return float('inf')

    def extract_price_title(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            if "flipkart.com" in url:
                title = soup.find("span", {"class": "B_NuCI"}).text.strip()
                price = soup.find("div", {"class": "_30jeq3"}).text.strip()
            elif "amazon.in" in url:
                title = soup.find("span", {"id": "productTitle"}).text.strip()
                price = soup.find("span", {"class": "a-price-whole"})
                if price:
                    price = "₹" + price.text.strip()
                else:
                    price = "Price not found"
            else:
                return None

            return {"title": title, "price": price}

        except Exception as e:
            return None

    product = product_query.lower()
    sites = {
        "www.amazon.in": "{ products[] { title price } }",
        "www.flipkart.com": "{ products[] { name price } }",
        "www.croma.com": "{ items[] { description price } }"
    }

    prices = []
    lowest = {"price": float('inf'), "name": "", "site": ""}

    for site, query in sites.items():
        try:
            data = agentql.query(url=f"https://{site}/search?q={product}", query=query)
            key = "products" if "products" in data else "items"
            items = data.get(key, [])

            for item in items:
                name = item.get("name") or item.get("title") or item.get("description", "")
                price_str = item.get("price")
                price_val = extract_price(price_str)

                if price_val != float('inf') and is_relevant(name, product):
                    prices.append((name, site, price_str))
                    if price_val < lowest["price"]:
                        lowest = {"price": price_val, "name": name, "site": site}

                    if len(prices) >= 9:
                        break
        except Exception:
            continue

    if prices:
        price_lines = [f"- {name.title()} on **{site}**: ₹{price}" for name, site, price in prices]
        result = "### 🛍️ Price Comparison Results\n" + "\n".join(price_lines)
        if lowest["site"]:
            result += f"\n\n💰 **Lowest price is ₹{lowest['price']} on `{lowest['site']}` for:**\n- {lowest['name'].title()}"
        return result
    else:
        results = tavily_tool.invoke({
            "query": f"{product_query} price comparison india",
            "max_results": 5
        }).get("results", [])[:3]
        if results:
            final_lines = []
            for r in results:
                if r.get("url"):
                    data = extract_price_title(r["url"])
                    if data:
                        final_lines.append(f"🖥️ **{data['title']}**\n💰 {data['price']}")
            return "\n\n".join(final_lines) if final_lines else "Fallback links found, but product info couldn't be extracted."
        else:
            return "Sorry, no price information could be found."

llm_with_tools = llm.bind_tools([compare_prices])

def reasoning_node(state: ReActState) -> ReActState:
    system_prompt = SystemMessage(content=(
        "You are a smart shopping assistant that helps users compare prices "
        "across Amazon.in, Flipkart, and Croma. Use the tool to fetch up-to-date price info "
        "using AgentQL and Tavily both, and mention the prices. Also mention the site offering the lowest price. "
        "If data is not available from both AGENTQL and Tavily then use your own data. "
        "Add a note that prices may vary and should be checked on the official site. "
        "Use tools internally but do not mention tool names like compare_prices to the user."
    ))
    messages = [system_prompt] + state["messages"]

    print("🧠 Reasoning with user query...")
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: ReActState) -> str:
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        print("🔧 Tool use required.")
        return "tool_use"
    else:
        print("✅ Final answer ready.")
        return "final"

tools_node = ToolNode([compare_prices])

graph = StateGraph(ReActState)
graph.add_node("reasoning", reasoning_node)
graph.add_node("tool_use", tools_node)
graph.add_edge(START, "reasoning")
graph.add_conditional_edges("reasoning", should_continue, {
    "tool_use": "tool_use",
    "final": END
})
graph.add_edge("tool_use", "reasoning")
price_compare_app = graph.compile()

chat_history: list[BaseMessage] = []

def ask_bot(query: str, chat_history: List[BaseMessage]) -> (str, List[BaseMessage]):
    chat_history.append(HumanMessage(content=query))
    state = {"messages": chat_history}
    response_msg = price_compare_app.invoke(state)["messages"][-1]
    chat_history.append(response_msg)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_text = f"{response_msg.content}\n\n🕒 *Data fetched on {timestamp}*"
    return response_text, chat_history
