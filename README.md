# 🚗 AI-Powered Smart Travel Assistant

Welcome to the **AI-Powered Smart Travel Assistant** — a Streamlit-based application that helps you plan affordable and personalized road trips in Pakistan (or anywhere!) using cutting-edge AI models like **LLaMA3 (via Groq)** and **LangGraph agents**.

---

## ✨ Features

✅ Extracts trip details from natural language  
✅ Recommends destinations within your distance & budget  
✅ Provides real-time weather info using OpenWeatherMap  
✅ Calculates total trip cost (transport, hotel, food)  
✅ Finalizes a feasible trip plan with suggestions  
✅ Downloads the final plan as a professional PDF  
✅ Interactive, simple web-based interface

---

## 🧰 Technologies Used

- 🧠 [LangChain](https://github.com/langchain-ai/langchain)
- ⚙️ [LangGraph](https://github.com/langchain-ai/langgraph)
- 🌍 [Tavily Search Tool](https://docs.langchain.com/docs/integrations/tools/tavily/)
- 🌤️ OpenWeatherMap API
- 🧾 WeasyPrint (for PDF generation)
- 🧩 Streamlit (for the UI)
- 🔐 dotenv (to manage API keys)

---

## 📦 Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-trip-planner.git
cd smart-trip-planner
````

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If you're on **Linux**, install these system packages before running:

```bash
sudo apt install libpango1.0-0 libgdk-pixbuf2.0-0 libcairo2
```

### 3. Setup Environment Variables

Create a `.env` file in the root directory and add your OpenWeatherMap API key:

# 🔑 Groq API key (for LLaMA3 model access via LangChain)
```env
GROQ_API_KEY=your_groq_api_key_here
```

# 🌍 Tavily API key (used for web search results)
```env
TAVILY_API_KEY=your_tavily_api_key_here
```

# 🌤️ OpenWeatherMap API key (to fetch live weather for destinations)
```env
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
```


---

## ▶️ How to Run the App

Start the Streamlit app using the following command:

```bash
streamlit run streamlit_app.py
```

It will launch in your browser at: [http://localhost:8501](http://localhost:8501)

---

## ✍️ How to Use

1. **Enter your trip details** (e.g., `"Plan a 2-day trip from Islamabad under PKR 15,000"`)
2. The assistant will:

   * Understand your request
   * Suggest destinations
   * Check weather
   * Calculate total cost
   * Recommend a feasible travel plan
3. **View detailed updates** as each AI agent completes its task
4. **Download** your finalized trip plan as a **PDF**

---

## 📄 Output Format Example

```
🎉 FINAL TRAVEL PLAN:
——————————————————————————————
📍 Origin: Lahore
🗓️ Dates: 2025-08-01 to 2025-08-03
💰 Budget: PKR 20000

✅ TRIP IS FEASIBLE

Destinations:
- Murree | 300 km | 24°C, Sunny
- Nathia Gali | 340 km | 22°C, Cloudy

Recommended Destination: Murree
- Distance: 300 km
- Average Temp: 24°C
- Rain Chance: 10%
- Weather: Sunny

Budget Breakdown:
- Transportation: PKR 5000
- Accommodation: PKR 8000
- Food & Activities: PKR 6000
- Total: PKR 19000

Must-see Places:
- Mall Road
- Patriata Chairlift

Hotels:
- Grand Continental
- Pine Resort
```

---

## 📁 Project Structure

```
smart-trip-planner/
│
├── trip_planner_core.py        # Core LangGraph logic and agents
├── streamlit_app.py            # Streamlit UI
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment config
├── README.md                   # Project documentation
```
