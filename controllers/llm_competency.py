import json
from groq import Groq # type: ignore
import pandas as pd # type: ignore
import google.generativeai as genai # type: ignore
import json
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

# #this is function for the generate the 
def generate_competency_report(input_context,candidate_name):
    # Get API key
    groq_api = os.getenv("GROQ_API_KEY1")
    client = Groq(api_key=groq_api)

    default_instruction = """You are the lead assessor for a candidate evaluation event. You will receive context data in following format -
[{{‘name_of_competency’: [{{‘name_of_descriptor’, ‘score_of_descriptor’, ‘feedback_of_descriptor’}}]}}] and the name of the participant/ candidate.

Your goal is to generate a professional report for a candidate.
Use a professional and simple tone and be objective in your reporting.
Remember - The language of the report should be impersonal, report like language, as objective as possible.

Instructions -
Follow this process to generate a detailed report.
Step 1 - Extract the ‘name_of_competency’, all the 'name_of_descriptor' values, 'score_of_descriptor' values and 'feedback_of_descriptor' values for the given information.
Output these extracted values.
Step 2 - In the 'feedback_of_descriptor' the name of the activity will be mentioned at the end. Infer the every single name activity name, even if it is repeated and output it.
Step 3 - - Categorize the each of the ‘name_of_descriptor’ either as ‘Strengths’ or ‘Areas of Opportunities’ based on the following condition -
IF VALUE of ‘score_of_descriptor’ > 2.0, ‘name_of_descriptor’ belongs to ‘Strengths’
IF VALUE of ‘score_of_descriptor’ <= 2.0, ‘name_of_descriptor’ belongs to ‘Areas of Opportunities’
Print the categorization.
Ensure that descriptors are categorized strictly based on the provided scoring criteria.
If the score of a descriptor is greater than 2.0, categorize it as a 'Strength'; if the score is 2.0 or lower, categorize it as an 'Area of Opportunity'.
Step 4 - Use the ‘feedback_of_descriptor’ to write a few points about the candidate. Create an evaluation report with the heading 'Evaluation Report:' using the points written by you.
The format of the evaluation report is in form of JSON format as follows :
```json
{
  name of competency
  {
    "Strengths": 
    {
      "Descriptor Name": " Write a point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report Write one more point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report",
      "Descriptor Name": "Write a point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report Write one more point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report"
    },
    "Areas of Opportunity": 
    {
      "Descriptor Name": "Write a point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report Write one more point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report.",
      "Descriptor Name": "Write a point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report Write one more point to explain why ‘name_of_descriptor’ belongs to ‘Strengths’. Use the ‘feedback_of_descriptor’ to write your point and the activity name
      derived in Step 2. Do not copy the ‘feedback_of_descriptor’ as it is, rephrase it to make it sound more professional and like a report.
      Do not forget to mention examples of actions and the activities in which these actions were seen. Make the point more enhanced using your own points derived from the ‘feedback_of_descriptor’.
      Always use the candidate’s name in each point of the report."
    }
  }
}
Always use the candidate’s name in each point of the report.
There should be multiple sub bullet points which show and explain why ‘name_of_descriptor’ is a strength of the candidate.

Try to pick up examples of actions from the feedback which support if the descriptor is a strength or an area of opportunity. Try to include the name of the
activity in which the example was seen and the candidate_name as much as possible.

Based on the above given instructions, create a report for the following input_context -
{input_context}
Candidate name is - {candidate_name}"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": default_instruction
            },
            {
                "role": "user",
                "content": f"Generate a report for the given context {input_context}{candidate_name}",
            }
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        response_format={"type": "json_object"},
        top_p=1,
        stop=None,
        stream=False,
    )
    llm_output = chat_completion.choices[0].message.content
    llm_output = llm_output.replace("**", "")
    llm_output = llm_output.replace("*", "")
    llm_output = llm_output.replace("```json", "")
    
    final_output = llm_output.split('Evaluation Report:')[-1]
    return final_output

