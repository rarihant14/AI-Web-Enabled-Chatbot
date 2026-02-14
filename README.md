# 🛒 AI Web-Enabled Shopping Assistant  
### (Reasoning Model + Real-Time Web Search)

An intelligent AI shopping chatbot powered by:

- 🧠 Groq Reasoning LLM (Qwen 32B)
- 🌐 Tavily Real-Time Web Search
- 🚀 Flask Web Framework

This assistant doesn’t just generate text —  
it searches the web, filters trusted sources, builds structured context, and reasons before answering.

---

## 🔥 What Makes It Special?

- ✅ Uses a Reasoning Model (Qwen 32B via Groq)
- ✅ Performs live web search before answering
- ✅ Filters ONLY trusted domains (Amazon & Flipkart)
- ✅ Builds structured web context for accurate responses
- ✅ Maintains conversation memory
- ✅ Logging system (file + console)
- ✅ Clean Flask-based UI

---

## 🧠 How It Works

1. User sends a query  
2. Tavily performs real-time web search  
3. Results are filtered (Amazon / Flipkart only)  
4. Structured web context is built  
5. Reasoning LLM processes:
   - Conversation memory
   - Web context
   - User query
6. Returns:
   - Direct answer
   - Top 3 product options (when required)
   - Trusted links

---

## 🛠 Tech Stack

- Python  
- Flask  
- Groq (Qwen 32B Reasoning Model)  
- Tavily Search API  
- python-dotenv  
- Logging Module  

---

## 🔑 Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create `.env` file

```
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### Run the application

```bash
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## 📌 Example Queries

- Best gaming laptop under 80000  
- Top 3 smartphones under 50000  
- Best budget earbuds for gym  

---

## ⚠ Smart Rules

- Must search internet before answering  
- Must use trusted sources  
- Cannot invent prices/specs  
- If no trusted result → informs user  

---

## 💡 Why a Reasoning Model?

Instead of simple text generation, this project uses a reasoning LLM that:

- Processes structured web context  
- Combines memory + real-time data  
- Makes logical comparisons  
- Reduces hallucination risk  

---

# 🚀 AI-Web-Enabled-Chatbot

Real Search. Real Reasoning. Real Links.
