🌍 Travel Buddy Agent
An intelligent, interactive AI-powered travel assistant built to help users seamlessly plan their perfect vacations. Combining a structured planning interface with a smart conversational AI agent, Travel Buddy Agent delivers personalized itineraries, budget breakdowns, and real-time contextual feedback (such as weather and seasonal warnings) to enhance the travel planning experience.

🚀 Features
Dual-Interface Design: * Structured Inputs (Left Sidebar): Allows users to lock down destination preferences, trip duration, accommodation types, and budget levels.

Conversational AI (Main Panel): An intuitive chat interface for dynamic queries, custom requests, and itinerary fine-tuning.

Context-Aware Guardrails: The agent evaluates user preferences against real-world data, proactively warning users about seasonal mismatches (e.g., correcting misconceptions about weather or monsoon seasons).

Automated Budget Breakdown: Instantly calculates estimated expenses split by flights, accommodation, food, and sightseeing.

Day-by-Day Itinerary Generation: Delivers structured daily plans optimized for the user's travel style.

🛠️ Tech Stack
Frontend: Streamlit (Running locally on port 8501)

AI Engine & Framework: LangChain / IBM watsonx.ai (or specify your chosen LLM, e.g., OpenAI GPT-4o / Llama 3)

Language: Python 3.9+

📦 Installation & Setup
Follow these steps to get the project running locally:

1. Clone the Repository
Bash
git clone https://github.com/your-username/travel-buddy-agent.git
cd travel-buddy-agent
2. Set Up a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Make sure you have a requirements.txt file ready. Install the packages using:

Bash
pip install -r requirements.txt
(Your requirements.txt should at minimum include: streamlit, langchain, openai or ibm-watsonx-ai, and python-dotenv)

4. Environment Variables
Create a .env file in the root directory and add your API keys:

Code snippet
# Example for OpenAI or IBM Watsonx
API_KEY=your_api_key_here
PROJECT_ID=your_project_id_here
5. Run the Application
Start the Streamlit server:

Bash
streamlit run app.py
Once executed, the application will automatically open in your browser at http://localhost:8501/.

💡 How It Works (Architecture)
User Input: The user sets trip constraints in the sidebar and submits a prompt via the chat interface.

Prompt Engineering & Context Injection: The system bundles the sidebar constraints with the user prompt into a structured template.

LLM Processing: The LLM evaluates the request, applies built-in guardrails (e.g., verifying weather feasibility), and returns a structured response.

UI Rendering: Streamlit dynamically renders the markdown response, displaying the chat history, budget tables, and recommended activities.


Application Preview
<img width="1920" height="807" alt="Screenshot 2026-06-22 224621" src="https://github.com/user-attachments/assets/450c6e79-c777-4b16-97c3-d05ab00f6000" />
