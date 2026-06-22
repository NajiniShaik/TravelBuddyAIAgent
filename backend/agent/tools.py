import os  
from langchain.tools import tool 
from langchain_tavily import TavilySearch 
from serpapi import GoogleSearch 


def get_tavily_tool():
    tavily_api_key=os.getenv('TAVILY_API_KEY')
    return TavilySearch(
        max_resulsts=5,
        search_depth="advanced",
        tavily_api_key=tavily_api_key
    )

@tool 
def search_flights(origin:str,destination:str,date:str)->list:
    """Search for flights using SerAPI Google Flights. Date should be in YYYY-MM-DD format like 2026-12-15."""

    print(f"\n[Tool Call] Searching flights from {origin} to {destination} on {date}")

    serpapi_key=os.getenv("SERPAPI_KEY")

    params={
        "api_key":serpapi_key,
        "engine":"google_flights",
        "departure_id":origin,
        "arrival_id":destination,
        "outbound_date":date,
        "currency":"INR",
        "type":"2"
    }

    search=GoogleSearch(params)

    results=search.get_dict() 

    best_flights=results.get("best_flights","No flights found for the specified criteria")

    return best_flights