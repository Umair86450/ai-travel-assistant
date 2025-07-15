
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import convert_to_messages
from langgraph_supervisor import create_supervisor
from langchain_core.tools import tool
import os
import getpass
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Initialize LLMs
groq_model = ChatGroq(model="llama3-70b-8192", temperature=0.7)
groq_strict = ChatGroq(model="llama3-70b-8192", temperature=0.3)

# Tools
web_search = TavilySearch(max_results=5)

# Math tools
@tool
def calculate_trip_cost(
    round_trip_km: float,
    mileage_km_per_ltr: float,
    fuel_price_per_ltr: float,
    hotel_nights: int,
    hotel_price_per_night: float,
    food_per_day: float,
    days: int
) -> dict:
    """Calculate total cost of a trip including fuel, hotel, and food."""
    fuel_cost = (round_trip_km / mileage_km_per_ltr) * fuel_price_per_ltr
    hotel_cost = hotel_nights * hotel_price_per_night
    food_cost = food_per_day * days
    total = fuel_cost + hotel_cost + food_cost
    return {
        "fuel": round(fuel_cost, 2),
        "hotel": round(hotel_cost, 2),
        "food": round(food_cost, 2),
        "total": round(total, 2),
        "currency": "PKR"
    }

# Get Weather for Destinations
def get_weather_for(destination: str, date: str):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": destination,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params).json()
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"{destination}: {temp}°C, {description}"
    except Exception as e:
        return f"{destination}: Error fetching weather"

@tool
def get_weather_for_destinations(destinations: list, travel_dates: list) -> dict:
    """Fetches real-time weather for each destination on specified dates."""
    weather_info = {}
    for dest in destinations:
        forecast = []
        for date in travel_dates:
            weather = get_weather_for(dest, date)
            forecast.append(weather)
        weather_info[dest] = forecast
    return weather_info

# NLU Agent Prompt
nlu_prompt = """
You are an NLU agent. Extract structured data from user's natural language query.
Respond ONLY with JSON in this format:

{
  "origin": "Rawalpindi",
  "max_distance_km": 600,
  "budget": 20000,
  "travel_dates": ["not specified"],
  "currency": "PKR"
}

If travel dates not specified, respond with ["not specified"].
If max_distance_km not mentioned, default to 500 km.
If origin is international (like Dubai), set currency accordingly (e.g., AED).
"""

nlu_agent = create_react_agent(
    model=groq_model,
    tools=[],
    prompt=nlu_prompt,
    name="nlu_agent"
)

# Research Agent Prompt
research_prompt = """
You are a travel specialist. Find nearby destinations within max distance.
For EACH destination, return:
- Name
- Distance from origin (km)
- Recommended hotels (1–2)
- Must-see places (2–3)

Format:
Murree: 300 km
- Hotel: Grand Continental, Pine Resort
- Must-see: Mall Road, Patriata Chairlift
"""

research_agent = create_react_agent(
    model=groq_model,
    tools=[web_search],
    prompt=research_prompt,
    name="research_agent"
)

# Weather Agent Prompt
weather_prompt = """
You are a weather expert. Check weather for each destination on travel dates.
For EACH destination, return:
- Name
- Avg Temp (°C)
- Rain Chance (%)
- Weather Status (Sunny/Cloudy/Rainy)

Format:
Murree: 22°C, 15% chance of rain, Sunny
"""

weather_agent = create_react_agent(
    model=groq_model,
    tools=[get_weather_for_destinations],
    prompt=weather_prompt,
    name="weather_agent"
)

# Math Agent Prompt
math_prompt = """
You are a math expert. Calculate trip cost based on inputs.
Return breakdown like this:
Transportation: X PKR
Accommodation: Y PKR
Food & Activities: Z PKR
Total: T PKR

Make sure total matches budget.
"""

math_agent = create_react_agent(
    model=groq_model,
    tools=[calculate_trip_cost],
    prompt=math_prompt,
    name="math_agent"
)

# Decision Agent Prompt
decision_prompt = """
You are a decision agent. Finalize feasibility based on all steps.
Respond ONLY with the final verdict in this format:

🎉 FINAL TRAVEL PLAN:
————————————————————————————————————
📍 Origin: [origin]
🗓️ Dates: [travel_dates]
💰 Budget: [currency][budget]

✅ TRIP IS FEASIBLE

Destinations:
- [destination 1] | [distance] km | [weather]
- [destination 2] | [distance] km | [weather]
- [destination 3] | [distance] km | [weather]

Recommended Destination: [recommended_destination]
- Distance: [distance] km
- Average Temp: [avg_temp]°C
- Rain Chance: [rain_chance]%
- Weather: [weather_status]

Budget Breakdown:
- Transportation: [currency][transport_cost]
- Accommodation: [currency][hotel_cost]
- Food & Activities: [currency][food_cost]
- Total: [currency][total_cost]

Must-see Places in [recommended_destination]:
- [place 1]
- [place 2]
- [place 3]

Recommended Hotels:
- [hotel 1]
- [hotel 2]

Enjoy your safe and exciting adventure!
"""

decision_agent = create_react_agent(
    model=groq_model,
    tools=[],
    prompt=decision_prompt,
    name="decision_agent"
)

# --- Smart Supervisor (Fixed: Now passing agent objects instead of strings) ---
supervisor = create_supervisor(
    model=groq_strict,
    agents=[
        nlu_agent,
        research_agent,
        weather_agent,
        math_agent,
        decision_agent
    ],
    prompt="""
You are the trip planning supervisor.
Your job is to route the request through these agents in order:
1. nlu_agent: To extract travel details from natural language
2. research_agent: To find nearby destinations
3. weather_agent: To check weather at each destination
4. math_agent: To calculate costs
5. decision_agent: To finalize feasibility

Only respond with the name of the next agent to call.
Never do calculations or research yourself.

Once all agents have completed their tasks, compile and present the final trip plan in a clean, readable format.

Final Output should include:
- Recommended destination
- Weather status
- Cost breakdown
- Must-see places
- Recommended hotels

Do NOT say 'I'm done!' or 'Transfer back'
Only respond with the final verdict in this format:

""",
    add_handoff_back_messages=True
).compile()


# Add this function to draw graph
def get_graph_image():
    """Returns graph image data for display"""
    try:
        # Draw graph as PNG
        return supervisor.get_graph().draw_mermaid_png()
    except Exception as e:
        st.error(f"Error generating graph: {str(e)}")
        return None