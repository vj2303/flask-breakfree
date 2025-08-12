# controllers/llm_readiness.py
from typing import List, Dict, Iterable
from groq import Groq # type: ignore
import pandas as pd # type: ignore
import google.generativeai as genai # type: ignore
import json
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

#this is the function for the generate a content for the column of the table 
def generate_readliness_analysis(analysis_dict, participant_name):
    
    groq_api = os.getenv("GROQ_API_KEY2")

    client = Groq(api_key=groq_api)
    default_instruction = """You will receive a context in the following format -
{
"Competency": [A list of multiple Competencies],
"Readiness": [A list of multiple numerical values of readiness],
"Application": [A list of multiple numerical values for application scores],
}

Your goal is to generate a "Comment" by comparing the corresponding elements in the readiness and application list.

Example input -
analysis_dict = {
    "Competency": ["Delighting Customers: Solutions & Experience Creator", "Boldly Innovate: Catalyst",
                   "Inspiring People: Talent Cultivator", "Own it: Business Leader",
                   "Prioritize: Sense Maker", "Conversing In Difficult Situations",
                   "Communicating Assertively", "Leading With Strategy"],
    "Readiness": [2, 1, 2, 3, 1, 1, 1, 1],
    "Application": [1.6, 1.1, 2.1, 1.3, 1.3, 1.7, 1.6, 1.6],
}
candidate_name = Rohit
Example output -
"Comment": ["Rohit demonstrates a relatively good level of readiness (2) but falls short in application (1.6). This indicates that he has the knowledge of what needs to be done but may struggle to effectively apply or display these behaviors in real-life interactions and situations. He may benefit from more practice and coaching in this competency.",
                "Rohit's application in the 'Boldly Innovate: Catalyst' competency is relatively lower (1.1) than his readiness (1). He may naturally demonstrate these competencies but may not be consciously aware of how he does so. This suggests the need for awareness training to help him practice these competencies with more deliberate thoughtfulness.",
                "Rohit's application level (2.1) exceeds his readiness (2) in the 'Inspiring People: Talent Cultivator' competency. This indicates that he naturally demonstrates these competencies but may benefit from developing a deeper understanding through awareness training.",
                "Rohit's readiness in the 'Own it: Business Leader' competency is high (3), but his application level is comparatively lower (1.3). This suggests that he has the knowledge of what needs to be done but may need more practice and coaching to effectively apply these behaviors in real work-related situations.",
                "Rohit's application level (1.3) is slightly higher than his readiness (1) in the 'Prioritize: Sense Maker' competency. This indicates a relatively good alignment but still room for growth in applying the competencies.",
                "Rohit's application in the 'Conversing In Difficult Situations' competency is slightly better (1.7) than his readiness (1). This suggests a need for further development in applying these competencies effectively.",
                "Rohit's application level (1.6) is slightly better than his readiness (1) in the 'Communicating Assertively' competency, indicating an alignment but still room for growth.",
                "Rohit's application in the 'Leading With Strategy' competency is slightly better (1.6) than his readiness (1). This suggests a need for further development in applying these competencies effectively."]

Generate an output for the following input context and candidate name based on the above given instructions -
{analysis_dict}{candidate_name}"""
    # for competency, avg_score, readiness_score, participant_name in zip(competencies, avg_scores, readliness_score, participant_name):
    chat_completion = client.chat.completions.create(
                messages=[
            {
                "role": "system",
                "content": default_instruction
            },
            {
                "role": "user",
                "content": f"Generate a short analysis for the given context {analysis_dict}{participant_name}",
            }
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        # max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
        )
    analysis_content = chat_completion.choices[0].message.content
    return analysis_content



#this function for calculating proper average
def safe_average(scores):
    """ Calculate average only for non-None scores. """
    valid_scores = [score for score in scores if score is not None and score != 0]
    if valid_scores:
        return sum(valid_scores) / len(valid_scores)
    return 0

#for feedback merging of same data
def merge_feedback(feedbacks):
    """ Merge feedback into two separate lines. """
    if len(feedbacks) > 1:
        return "\n".join(feedbacks[:2])  # Return the first two feedbacks as separate lines
    elif feedbacks:
        return feedbacks[0]
    return ""

#for formatting of the data which is extract from the DB
def data_for_llm(data):
    activity_categories = ['inbox_activity', 'case_study_analysis', 'group_discussion', 'role_play', 'cbi', 'case_study_presentation']
    competency_data = {}

    # Loop through each activity category and process the data
    for category in data:
        if category in activity_categories:
            for key, value in data[category].items():
                # print(data[category])
                competency, descriptor, score, feedback = value
                if competency not in competency_data:
                    competency_data[competency] = {}
                
                if descriptor not in competency_data[competency]:
                    competency_data[competency][descriptor] = {
                        'scores': [],
                        'feedbacks': [],
                        # 'activities': []  # To store activity names
                    }
                
                # Append score, feedback, and activity name
                competency_data[competency][descriptor]['scores'].append(score)
                if feedback.strip().upper() != 'NA':  # Ignore 'NA' feedback
                    competency_data[competency][descriptor]['feedbacks'].append(feedback.strip())
                # competency_data[competency][descriptor]['activities'].append(category)  # Append activity name

    # Yield each competency's data as soon as it's ready
    for competency, descriptors in competency_data.items():
        formatted_descriptors = []
        for descriptor, details in descriptors.items():
            avg_score = safe_average(details['scores'])
            merged_feedback = merge_feedback(details['feedbacks'])
            # activities = set(details['activities'])   Use set to remove duplicates
            formatted_descriptors.append({
                'descriptor': descriptor,
                'score': avg_score,
                'feedback': merged_feedback,
                # 'activities': list(activities)  # Convert set back to list for output
            })
        yield {
            competency: formatted_descriptors
        }
