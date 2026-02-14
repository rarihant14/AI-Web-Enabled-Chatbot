import os
import logging
from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv
load_dotenv()

from memory_store import MemoryStore
from web_chatbot import chat_with_bot



# Docs Logger Setup (File + Console)
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("ChatbotLogger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
console_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# folder name where html and static files are stored
app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

memory = MemoryStore(user_id="arihant")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.form.get("user_query", "").strip()

    if not user_query:
        return jsonify({"reply": "Type something bro 😭", "sources": []})

    logger.info(f"👤 User: {user_query}")

    # store message of user 
    memory.add_message("user", user_query)

    #  load memory context
    memory_context = memory.get_recent_memory(limit=10)

# if bot is not able to respond it will print crash
    try:
        bot_data = chat_with_bot(user_query, memory_context)
        logger.info(f"🤖 Bot: {bot_data.get('reply','')[:200]}...")
    except Exception as e:
        logger.error(f"💀 Bot crashed: {str(e)}", exc_info=True)
        bot_data = {"reply": f"💀 Bot crashed.\nError: {str(e)}", "sources": []}

    memory.add_message("assistant", bot_data["reply"])
    return jsonify(bot_data)


@app.route("/clear_memory", methods=["POST"])
def clear_memory():
    try:
        memory.clear()
        return jsonify({"reply": "✅ Memory cleared 😏", "sources": []})
    except Exception as e:
        return jsonify({"reply": f"❌ Memory clear failed: {str(e)}", "sources": []})


if __name__ == "__main__":
    logger.info("🔥 Chatbot Server Started...")
    app.run(debug=True)
