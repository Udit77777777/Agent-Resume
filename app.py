#==========LOAD MODULES===========

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np


st.set_page_config(layout="wide")
st.title("AI RESUME GENERATOR")
st.write("""This app helps user to build customized Professional Resume with latest Job apply links""")

st.image("bg.png")

st.sidebar.title("Fill Important Details")
st.sidebar.image("bg.png")
#2
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API",type = "password")
GOOGLE_API_KEY = st.sidebar.text_input("Groq-API",type = "password")
GROQ_API_KEY = st.sidebar.text_input("Gemini-API",type = "password")

all_API = [TAVILY_API_KEY,GROQ_API_KEY,GOOGLE_API_KEY]
if not all(all_API)
    st.error("Must Give API Keys")
    st.stop()
elif all(all_API)
    st.success("API Keys Loaded Successfully")
else:
    st.info("PASS ALL API-KEYS")
        
#3
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY
)

#response = model.invoke("Hello Buddy!")
#response.content[-1]['text']
#4
def search_latest_news_jobs(query):
    """
    This function helps to fetch latest
    news or jobs related article using
    tavily
    """

    client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    response = client.search(query)
    return response
#5
#Agent Creation  
agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs])

#agent
#6
def main_agent(agent, query):
  """This is main agent, or leader agent orchestrate sub agents"""

  prompt = """You are ai assistant and and below given is a prompt your task is to
give detailed prompt for this.
you are a professional Resume generator where user will give there personal info, you have
to create detailed Resume for students or professional one, It must be with dynamic UI and UX
and, with advance CSS Professional Designing Make sure to give output in HTML format only
no markdown allowed"""

  response = agent.invoke({'messages':[{'role':'user',
                                        'content':prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']

  # SAVE PROMPT using File Handling
  with open("prompt.txt", "w") as f:
      f.write(detailed_prompt)

  user_details = f"""
Below Given is a user details
generate Resume based on that, if not
given keep: Default Resume: Python Developer
user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details

  # CODE GENERATION
  response = agent.invoke(
      {
          "messages": [
              {
                  "role": "user",
                  "content": final_prompt
              }
          ]
      }
  )

  code = response["messages"][-1].content[-1]["text"]

  return code

 #7
# code = main_agent(agent, "UDIT, GEN AI EXPERT")
# from IPython import display as DISPLAY
# DISPLAY.HTML(code)
#8
#from IPython.display import HTML, display

def get_jobs(
    agent,
    Location="Noida, Delhi",
    Profile="Data Analyst, AI Engineer"
):

    prompt = f"""
Based on the user-given job profile, fetch the latest jobs or job application articles
from Naukri, LinkedIn, Indeed, or other popular job platforms.

Requirements:
- Job Profile: {Profile}
- Location: {Location}
- Show only jobs matching the given profile.
- Display:
    • Job Title
    • Company Name
    • Location
    • Salary (if available)
    • Experience
    • Direct Apply Link
- Return 10-20 latest jobs.
- Format the output as professional HTML cards with a modern Naukri-style UI.
"""

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    code = response["messages"][-1].content[-1]["text"]
    return code

   #code = get_jobs(agent)
   #DISPLAY.HTML(code)


