import os  
from dotenv import load_dotenv 
from langchain_core.messages import HumanMessage ,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent 
from langgraph.checkpoint.memory import InMemorySaver 

from backend.agent.tools import get_tavily_tool,search_flights 

load_dotenv() 


google_api_key=os.getenv("GOOGLE_API_KEY")

model=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=google_api_key,
    temperature=0.1
)

system_prompt="""You are a TravelBuddy assistant that helps travelers plan trips.
You have access to these tools:
- destination_research_tool: Research attractions, culture, and travel tips
- search_flights: Find flight options (use IATA codes: HYD=Hyderabad, GOI=Goa, BOM=Mumbai, DEL=Delhi, BLR=Bangalore)

CRITICAL INSTRUCTIONS FOR TOOLS:
1. When searching for flights using the `search_flights` tool, ALWAYS use the user's **Start Date** as the `date` parameter to check outbound flights.
2. Align all your accommodation, dining, and activity suggestions to fit within the user's total budget.
3. Structure the final response day-by-day between the provided start date and end date.
4. Customize the itinerary style to match the user's description/preferences.
Present results in a clean, readable format with clear markdown sections."""


tools_list=[get_tavily_tool(),search_flights]

checkpointer=InMemorySaver() 

config={"configurable":{"thread_id":"travel_session_1"}}


agent_executor=create_agent(
    model=model,
    tools=tools_list,
    system_prompt=system_prompt,
    checkpointer=checkpointer,
    debug=True
)


def run_travel_agent(prompt_text:str)->str:
    """
    Wrapper function called by your FastAPI endpoints to interface with LangGraph.
    """

    try:
        inputs={"messages":[
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt_text)
            ]}
        response=agent_executor.invoke(inputs,config=config)

        raw_content= response["messages"][-1].content 

        if isinstance(raw_content,list):
            text_parts=[]
            for block in raw_content:
                if isinstance(block,dict) and "text" in block:
                    text_parts.append(block["text"])
                elif hasattr(block,"text"):
                    text_parts.append(block.text)
                elif isinstance(block,str):
                    text_parts.append(block)
            return "\n".join(text_parts)
        
        return str(raw_content)
    
    except Exception as e:
        return f"Error running travel agent workflow: {str(e)}"