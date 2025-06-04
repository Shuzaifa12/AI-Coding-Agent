from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig
from openai import AsyncOpenAI
import os, asyncio
from dotenv import load_dotenv
import streamlit as st

st.set_page_config(layout = "wide", page_title = "Coding Agent")
st.title("✍ Hello From Your Expert Coding Agent 🤖")

load_dotenv()

gemini_key = os.getenv("Gemini_Key")

if not gemini_key:
    raise ValueError("API key is missing. Please ensure that it must be present in your .env file")

client = AsyncOpenAI(
    api_key = gemini_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = client
)

config = RunConfig(
    model = model,
    model_provider = client,    # type: ignore
    tracing_disabled = True
)

coding_agent = Agent(
    name = "Coding Agent",
    instructions = "You are a coding expert agent. Your task is to write the code/logic for the user according to their instructions. Before that you should ask the user in what language the code/logic should be written."
)
user_prompt = st.text_area("**Write your instructions** + **Language name** : ")

if st.button("Generate Code") and user_prompt:
    with st.spinner("Generating Code...."):
        async def main():
            response = await Runner.run(
                coding_agent,
                input = user_prompt,
                run_config = config 
            )

            result = response.final_output
        

            st.write(result)

        asyncio.run(main())
