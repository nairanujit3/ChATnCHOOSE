# 🛍️ PriceWise Assistant

**PriceWise Assistant** is an intelligent shopping chatbot built using **Streamlit**, **LangGraph**, and **NVIDIA NIMs (NeMo)**.  
It helps users compare real-time product prices across top Indian e-commerce platforms like **Amazon.in**, **Flipkart**, **Croma**, and **Reliance Digital**.

---

## 🚀 Features

- 🔍 Live product price comparison from multiple sources
- 🧠 LLM-powered reasoning using `meta/llama-3.1-70b-instruct`
- 🛠️ Tool-based workflow with LangGraph and LangChain
- 🌐 Uses AgentQL + Tavily Search + fallback scraping
- 📱 Mobile-friendly responsive UI (Streamlit)
- 💬 Persistent, chat-based shopping assistant

---

## 🧩 Tech Stack

| Tool / Library        | Purpose                                    |
|------------------------|---------------------------------------------|
| `Streamlit`            | Frontend UI                                 |
| `LangGraph` / `LangChain` | Agent orchestration & tool management   |
| `ChatNVIDIA`           | LLM-based decision making                   |
| `AgentQL`              | Structured e-commerce data extraction       |
| `Tavily Search`        | Search fallback (Amazon, Flipkart, Croma)   |

---

## 🔐 API Keys Required

Use [Streamlit's secrets](https://docs.streamlit.io/streamlit-cloud/secrets-management) to store keys:

`.streamlit/secrets.toml`:

```toml
NVIDIA_API_KEY = "your-nvidia-api-key"
TAVILY_API_KEY = "your-tavily-api-key"
AGENTQL_API_KEY = "your-agentql-api-key"
```

▶️ Getting Started

✅ Run Locally

(1) Clone the repository
```
git clone https://github.com/nairanujit3/priceWise.git

cd pricewise-assistant
```
(2) Install dependencies
```
pip install -r requirements.txt
```
(3) Launch the app
```
streamlit run app.py
```
