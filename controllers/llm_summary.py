# controllers/llm_summary.py
import json
import pandas as pd # type: ignore
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()


#sample function made for the summary of the data
# GOOGLE_API_KEY="AIzaSyDTW941mGo1Yucpretu4bwbSOWtXIay7rE"
# gemini_api = GOOGLE_API_KEY
gemini_api = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=gemini_api)

def generate_summary(final_report, candidate_name):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=[
            """You will receive an input context in the form of a dictionary. Perform the following steps:
step 1: Your goal is to identify the top 5 and lowest 5 descriptors based on the scores. Reconfirm if only the top 5 and lowest 5 descriptors are selected.
step 2: Write a one-line summary for each of the top 5 descriptors and the lowest 5 descriptors based on the respective given feedback without mentioning the score. Score should not be displayed in the final output. Use the candidate name in each summary. Do not copy the feedback as it is, rephrase the feedback.
step 3: The heading for the top 5 descriptors should be "Strengths", and the heading for the lowest 5 descriptors should be "Areas of Opportunities (AOIs)". Include the name of the descriptor as the subheading for each summarized point.
step 4: Include the name of participant also 
step 5: do not repeat the descriptors.

step 6: return the content in form of valid JSON string in output do not write json in output.
The output should be in the following JSON format:
{
  "Strengths": {
    "Descriptor Name": "Summary of the descriptor in 1 line.",
    "Descriptor Name": "Summary of the descriptor in 1 line."
  },
  "Areas of Opportunity": {
    "Descriptor Name": "Summary of the descriptor in 1 line.",
    "Descriptor Name": "Summary of the descriptor in 1 line."
  }
}
...

"""
        ],
    )

    # Convert the list input to a suitable string format for the prompt
    prompt = f"Generate a summary for the given context: {json.dumps(final_report)}"
    contents = [prompt, candidate_name]

    response = model.generate_content(contents)
    return response.text

