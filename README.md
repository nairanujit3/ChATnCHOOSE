# CHATnCHOOSE

Chat your way to the best deal!!

## 👥 Team Members
- Dhruv Jain (202418020)  
- Anujit Nair (202418036)
- Sreelakshmi Nair (202418037)  
- Shaili Parikh (202418049)

## 📖 Problem Definition
Users often find it challenging to compare prices of products across multiple e-commerce platforms in India. Manually searching each website is time-consuming and can lead to inconsistent results. CHATnCHOOSE addresses this by providing an AI-powered chatbot that automatically queries major Indian e-commerce sites (Amazon.in, Flipkart, Croma), compares prices, and presents users with clear, actionable information—either directly from product listings or by searching the web for relevant links.

## Tools and APIs Used
- LangGraph & LangChain: For building stateful, multi-step chatbot workflows.

- ChatNVIDIA (meta/llama3-70b-instruct): Large Language Model for reasoning and response generation.

- AgentQL: For structured web scraping of product listings from Amazon.in, Flipkart, and Croma.

- Tavily Search API: For fallback web search when direct scraping is not possible.

## Methodology

CHATnCHOOSE uses a tool-based agent workflow powered by LangGraph and LangChain. The process is as follows:

User Query: The user asks for a product price comparison.

Reasoning Node (LLM): The LLM analyzes the request and determines whether to use a tool.

Tool Use: If needed, the compare_prices tool queries AgentQL for direct product data from e-commerce sites. If AgentQL fails, it falls back to Tavily for broader web search results.

Response Generation: The LLM processes the retrieved data and generates a user-friendly summary or table of prices.

State Management: The chatbot maintains conversation state using LangGraph’s StateGraph, enabling multi-turn interactions and robust tool orchestration.

## Challenges and Fixes

Failed Attempts:

- Direct Scraping Limitations: Initially, direct scraping failed due to site structure changes and anti-bot measures.

- Context Length Issues: LLM struggled with large product lists, requiring result filtering.

Lessons Learned:

- Fallback Mechanisms: Essential for robustness; implemented Tavily as a backup.

- Result Filtering: Added relevance checks to improve output quality.

- State Management: LangGraph’s state machine was crucial for multi-turn conversations.

Future Fixes:

- Enhanced Filtering: Further refine product relevance algorithms.

- UI Integration: Plan to build a web or mobile frontend for better user experience.

- Error Handling: Improve logging and user feedback for failed queries.

CHATnCHOOSE demonstrates how modern AI tools can simplify price comparison for users by automating data retrieval, reasoning, and response generation. The project highlights the importance of robust state management, fallback mechanisms, and iterative testing in building reliable AI-driven applications. Future work will focus on improving filtering, user interfaces, and error handling for a seamless user experience.
