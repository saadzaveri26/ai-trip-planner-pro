# 🚀 AI Trip Planner Pro

](https://ai-trip-planner-pro-clzjkmhnrkzo5jtldh8ehj.streamlit.app/))

An advanced, AI-powered web application that creates dynamic, personalized, and interactive travel itineraries. Built for the Google Gen AI Exchange Hackathon.



## ✨ About The Project

My solution, the AI Trip Planner Pro, is a sophisticated web application I built that leverages Generative AI to create dynamic, personalized travel itineraries.

It goes beyond simple text generation by prompting the AI to return a rich, structured dataset, including GPS coordinates and cost estimates for each activity. I then use this data to power a modern, interactive dashboard with several key features.

## 🎯 Key Features

* **Hyper-Personalization:** Creates a truly unique itinerary from scratch based on a user's specific destination, dates, budget, travel pace, and interests.
* **Interactive Dashboard:** A professional, multi-tab dashboard with a sidebar for inputs, keeping the results clean and easy to navigate.
* **Vertical Itinerary Timeline:** Displays the day-by-day plan in a visually engaging and modern timeline format.
* **Automated Budget Analysis:** A dedicated tab provides a bar chart of estimated daily expenses and a metric for the total trip cost.

## 🛠️ Built With

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Orchestration:** [LangChain](https://www.langchain.com/)
* **Core AI Model:** [Google Gemini 1.5 Flash](https://deepmind.google/technologies/gemini/)
* **Data Handling:** [Pandas](https://pandas.pydata.org/)

## ⚙️ How to Run Locally

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.9+
* A Google AI API Key

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO.git](https://github.com/YOUR_USERNAME/YOUR_REPO.git)
    cd YOUR_REPO
    ```
2.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
3.  **Set up your API Key:**
    * Add your Google AI API key to the `app.py` file where it says `YOUR_API_KEY_HERE`.

4.  **Run the application:**
    ```sh
    streamlit run app.py
    ```
