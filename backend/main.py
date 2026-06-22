from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 

from agent.travel_agent import run_travel_agent 

app=FastAPI(title="TravelBuddy AI Agent Backend") 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelQueryRequest(BaseModel):
    user_input:str 

@app.post("/api/chat")
async def chat_endpoint(request:TravelQueryRequest):
    """
    Receives incoming text from Streamlit and feeds it 
    directly into your Gemini LangGraph agent.
    """

    try:
        agent_response=run_travel_agent(request.user_input)
        return {
            "status":"success",
            "response":agent_response
        }
    except Exception as error:
        return {"status":"error","message":str(error)} 
    
@app.get("/")
def health_check():
    return {
        "message":"TravelBuddy Backend is live and running!"
    }