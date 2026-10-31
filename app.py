import os
import certifi
import requests
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchainhub import Client
from langgraph.prebuilt import create_react_agent

# ── env ──────────────────────────────────────────────────────────────────────
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()
GEMINI_API_KEY       = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY       = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# ── tools ─────────────────────────────────────────────────────────────────────
search_tool = TavilySearchResults(max_results=2)

@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather information for a city."""
    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )
    response = requests.get(url)
    data = response.json()
    if "current" not in data:
        return f"Could not fetch weather data for {city}"
    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

# ── llm & agent (cached so they load once) ───────────────────────────────────
@st.cache_resource
def load_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0,
        api_key=GEMINI_API_KEY,
    )
    client = Client()
    prompt = client.pull("hwchase17/react")
    tools  = [search_tool, get_weather_data]
    return create_react_agent(model=llm, tools=tools, prompt=prompt)

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="ReAct Agent", page_icon="🤖", layout="centered")
st.title("🤖 ReAct Agent")
st.caption("Powered by Gemini · Tavily Search · Weatherstack")
st.divider()

# ── query input & run button ──────────────────────────────────────────────────
query = st.text_area(
    label="Enter your query",
    placeholder="e.g. What is the weather in Kathmandu? / Search latest AI news",
    height=120,
)

run = st.button("▶ Run Agent", type="primary", use_container_width=True)

# ── agent execution ───────────────────────────────────────────────────────────
if run:
    if not query.strip():
        st.warning("⚠️ Please enter a query before running the agent.")
    else:
        agent = load_agent()
        with st.spinner("🤖 Agent is thinking..."):
            try:
                result = agent.invoke({"messages": [("human", query)]})
                # Extract the final answer from the last message
                final_message = result["messages"][-1]
                answer = (
                    final_message.content
                    if hasattr(final_message, "content")
                    else str(final_message)
                )

                st.success("✅ Done!")
                st.divider()
                st.subheader("📋 Response")
                st.markdown(answer)

                # Optional: show agent steps in an expander
                with st.expander("🔍 View Agent Steps"):
                    for i, msg in enumerate(result["messages"]):
                        role = type(msg).__name__.replace("Message", "")
                        st.markdown(f"**Step {i+1} — {role}:**")
                        st.code(
                            msg.content if hasattr(msg, "content") else str(msg),
                            language="markdown",
                        )

            except Exception as e:
                st.error(f"❌ Error: {e}")
