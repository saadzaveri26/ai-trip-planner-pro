import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# --- 1. SET UP THE PAGE AND THE AI MODEL ---
st.set_page_config(page_title="AI Trip Planner Pro", page_icon="🚀", layout="wide")
st.title("🚀 AI Trip Planner Pro")

# Initialize the Gemini 1.5 Flash model with your API key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.8, # Increased temperature for more creative results
    google_api_key="YOUR_API_KEY_HERE"  # 👈 PASTE YOUR KEY HERE
)

# --- 2. THE NEW "SUPER-PROMPT" ---
json_parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
    You are an expert travel agent AI. Your task is to create a highly detailed, personalized travel itinerary.
    The user's request is for a trip to: {destination} for {days} days, with a {budget} budget, and interests in {interests}.
    
    You must provide the following:
    - A creative and catchy "tripName".
    - A "destination" name.
    - The "duration" in days.
    - The "budget" level.
    - A list of the user's "interests".
    - A day-by-day "itinerary".

    For each day in the itinerary, provide:
    - The "day" number.
    - A "theme" for the day.
    - A list of "activities".

    For each activity, you MUST provide:
    1. "name": The activity name.
    2. "description": A compelling 2-sentence description.
    3. "latitude": The precise latitude coordinate.
    4. "longitude": The precise longitude coordinate.
    5. "estimated_cost_usd": A numeric estimated cost in USD. Do not use ranges, just a single number.

    \n{format_instructions}\n
    """,
    input_variables=["destination", "days", "budget", "interests"],
    partial_variables={"format_instructions": json_parser.get_format_instructions()}
)

chain = prompt | llm | json_parser

# --- 3. BUILD THE USER INTERFACE WITH STREAMLIT ---
st.header("Tell us about your dream trip!")

with st.form("trip_form"):
    destination = st.text_input("Destination:")
    days = st.number_input("Number of Days:", min_value=1, max_value=30, value=7)
    budget = st.select_slider("Budget:", options=["💰 Budget-Friendly", "💰💰 Moderate", "💰💰💰 Luxury"])
    interests = st.multiselect("Interests:", ["History", "Food", "Nightlife", "Nature", "Art", "Adventure", "Shopping", "Relaxation"])
    
    submitted = st.form_submit_button("Plan My Trip!")

if submitted:
    if destination and interests:
        with st.spinner("Generating your personalized itinerary... This may take a moment."):
            try:
                result = chain.invoke({
                    "destination": destination, "days": str(days),
                    "budget": budget, "interests": ", ".join(interests)
                })

                # --- 4. DATA PROCESSING FOR MAP & BUDGET ---
                all_activities = []
                daily_costs = {}
                total_cost = 0

                for day_data in result.get("itinerary", []):
                    day_num = day_data.get("day")
                    daily_cost = 0
                    for activity in day_data.get("activities", []):
                        activity['day'] = day_num # Add day number to activity
                        all_activities.append(activity)
                        cost = activity.get("estimated_cost_usd", 0)
                        daily_cost += cost
                        total_cost += cost
                    daily_costs[f"Day {day_num}"] = daily_cost
                
                # Create DataFrames for charts
                map_df = pd.DataFrame(all_activities)
                cost_df = pd.DataFrame(list(daily_costs.items()), columns=['Day', 'Estimated Cost (USD)'])

                # --- 5. DISPLAY THE RESULTS ---
                st.header(result.get("tripName", "Your Custom Itinerary"))
                
                tab1, tab2 = st.tabs(["✈️ Itinerary & Map", "📊 Budget Breakdown"])

                with tab1:
                    col1, col2 = st.columns([0.6, 0.4]) # 60% for itinerary, 40% for map
                    
                    with col1:
                        for day_data in result.get("itinerary", []):
                            with st.expander(f"**Day {day_data.get('day')}: {day_data.get('theme', '')}**"):
                                for activity in day_data.get("activities", []):
                                    st.markdown(f"**{activity.get('name')}**")
                                    st.caption(activity.get('description'))
                                    st.markdown(f"_*Estimated Cost: ${activity.get('estimated_cost_usd', 0)}*_")
                                    st.write("")

                    with col2:
                        st.subheader("Trip Hotspots")
                        st.map(map_df, latitude='latitude', longitude='longitude', size=20)

                with tab2:
                    st.subheader("Estimated Budget Analysis")
                    st.metric(label="Total Estimated Trip Cost", value=f"${total_cost:.2f} USD")
                    st.bar_chart(cost_df.set_index('Day'))
                    with st.expander("View Raw Cost Data"):
                        st.dataframe(cost_df)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error("The AI may have returned a response in an unexpected format. Please try again with a slightly different query.")
    else:
        st.warning("Please fill in all the fields.")