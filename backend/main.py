from backend.services import chatbot

@app.post("/api/chat")
def query_chatbot(prompt: str):
    return {"response": chatbot_interface.get_chat_response(prompt)}
