import streamlit as st 
from datetime import date
import requests

st.set_page_config(page_title="IBM TravelBuddy AI Agent", page_icon="",layout="wide")

BACKEND_URL="http://127.0.0.1:8000/api/chat"

def send_message_to_backend(prompt_text:str):
    """ Sends the user query to the FastAPI backend and gets the agent's real response."""

    try:
        payload={
            "user_input":prompt_text
        }
        response=requests.post(BACKEND_URL,json=payload)

        if response.status_code==200:
            result=response.json() 

            if result.get("status")=="success":
                return result.get("response")
            else:
                return f"Backend Error: {result.get('message')}" 
        else:
            return f"Error communicating with backend server (Status Code: {response.status_code})"
    except Exception as e:
        return f"Could not connect to the backend server. Is it running? Details: {str(e)}"
    


if "chat_history" not in st.session_state:
    st.session_state.chat_history=[
        {
            "role":"assistant",
            "content":"Hello! I am your TravelBuddy AI. Where are we traveling to? You can use the planner on the left or just type to me here!"
        } 
    ]

st.title("TravelBuddy Conversational AI Assistant")
st.caption("Frontend Preview Layout - IBM AI Internship Project")
st.divider() 


left_column,right_column=st.columns([1,2],gap="large")

with left_column:
    st.markdown("### New Trip Planner")

    with st.form("quick_form"): 

        col_air1,col_air2=st.columns(2) 
        with col_air1:
            origin=st.text_input("From (origin)",placeholder="e.g., HYD") 
        
        with col_air2:
            destination=st.text_input("To (Destination)",placeholder="e.g., GOA")

        
        col_date1,col_date2=st.columns(2) 

        with col_date1:
            start_date=st.date_input("Start Date",min_value=date.today())
        
        with col_date2:
            end_date=st.date_input("End Date", min_value=date.today())


        budget=st.number_input("Budget (INR)",min_value=0,step=5000,value=25000,help="Enter your total budget in Rupees")
        description=st.text_input("Trip Description / Preference",placeholder="e.g., Luxury honeymoon, budget solo trip, seeking adventure and seafood sports...")

    
        form_submit=st.form_submit_button("Generate Complete AI Travel Plan",use_container_width=True)

        if form_submit:
            if origin and destination:
                user_message=(
                    f"Plan a trip from {origin.upper()} to {destination.upper()}."
                    f"starting on {start_date.strftime('%Y-%m-%d')} and ending on {end_date.strftime('%Y-%m-%d')}."
                    f"My total budget is Rs.{budget:,} INR."
                    f"Additional preferences and trip details: {description if description else 'None specified.'}"
                )
                
                st.session_state.chat_history.append({
                    "role":"user",
                    "content":f"Custom Trip Request: {origin.upper()} -> {destination.upper()} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
                })

                with st.spinner("Agent is tailoring your itinerary, checking flights, and budgets...."):
                    agent_reply=send_message_to_backend(user_message)
                
                st.session_state.chat_history.append({
                    "role":"assistant",
                    "content":agent_reply
                })

                st.rerun()
            else:
                st.error("Please fill in both origin and Destination Fields.")
            
with right_column:
    st.markdown("### Conversation Log")

    chat_container=st.container(height=450,border=True)

    with chat_container:
        for message in st.session_state.chat_history:
            if message['role']=='user':
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])
    user_query=st.chat_input("Type any travel question here....")

    if user_query:
        st.session_state.chat_history.append({
            "role":"user",
            "content":user_query
        })
        chat_container.chat_message("user").write(user_query)

        with chat_container.chat_message("assistant"): 
            with st.spinner("Agent is thinking..."):
                agent_reply=send_message_to_backend(user_query)
            st.write(agent_reply)

        st.session_state.chat_history.append({
            "role":"assistant",
            "content":agent_reply
        })
        st.rerun()