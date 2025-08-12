import re
from typing import List, Optional   

import json

def get_proper_descriptor(clean_descriptor):
    competency_mapping = {
        # mapping for IA fields
        'Shares  Translates Market Insights':'Shares & Translates Market Insights',
        'Sets up an engagement plan collaborates with stakeholders and aligns with their expectations to meet their needs': 'Sets up an engagement plan, collaborates with stakeholders, and aligns with their expectations to meet their needs.',
        #this is extra field which getting repeated due to extra space at end
        'Sets up an engagement plan collaborates with stakeholders and aligns with their expectations to meet their needs ':'Sets up an engagement plan, collaborates with stakeholders, and aligns with their expectations to meet their needs.',
        'Displays Positive Authenticity  Courage ':'Positive Authenticity & Courage',
        'Talent Planning  Diverse Strong Pipelines  Identifies talent within and outside the organisation leveraging strong networks  ' :'Talent Planning & Diverse, Strong Pipelines',
        'Fosters Learning  Healthy Work Climate. ':'Fosters Learning & Healthy Work Climate.',
        'Talent Planning  Diverse Strong Pipelines  Nurtures and develops talent within and outside the team e.g. at the college institute level.':'Talent Planning & Diverse, Strong Pipelines',
        'Collaborates  Connects ':'Collaborates & Connects',
        'Brings Perspective  Teaches Proficiently.': 'Brings Perspective & Teaches',
        'Stands up for own rights  expressing thoughts feelings and beliefs directly honestly and appropriately.': 'Stands up for own rights', 
        'Says no courageously agrees and disagrees gracefully validates other peoples ideas and stands up for others': 'Courageously says no and handles agreements and disagreements gracefully.',
        'Possesses welldefined ideas and opinions rooted in experience and demonstrates the ability to articulate and confidently advocate for them':'Possesses well-defined, experience-based ideas and articulates them confidently.',
        'Uses several persuasion techniques depending on the personality of the individual on the other side of the table':'Adapts persuasion techniques based on the individuals personality.',
        #mapping of CBI fields
        'Describe a situation where you successfully gathered market insights to understand customer needs and preferences. How did you translate these insights into actionable strategies to improve customer experiences' : 'Shares & Translates Market Insights',
        'Give an example of a time when you effectively addressed a direct indirect customer complaint or concern. How did you turn the customers feedback into actionable insights for internal teams and what impact did it have' : 'Creates Plans to Deliver Differentiated Customer Experiences',
        'Can you share an example of a time when you proactively anticipated a customers future needs and designed a solution to meet those needs How did you ensure that the solution was aligned with the customers expectations' : 'Sets up an engagement plan, collaborates with stakeholders, and aligns with their expectations to meet their needs.',
        'Share an example of a time when you identified talent within or outside the organization using your networks. How did you leverage these networks to attract and engage potential candidates' : 'Identifies talent within and outside the organization leveraging strong networks.',
        'Can you describe an instance where you nurtured and developed talent within your team or organization How did you tailor your approach for individuals growth and development needs' :'Nurtures and develops talent within and outside the team e.g. at the college institute level.',
        'Give an example of a time when you collaborated across different teams to create a healthy work climate. How did your efforts contribute to a positive and productive work environment' : 'Fosters Learning & Healthy Work Climate.',
        'Can you provide an example of a time when you brought fresh perspectives to a challenging problem How did you effectively share these perspectives with your team and what impact did it have': 'Brings Perspective & Teaches',
        'Describe a situation where you successfully gathered input from multiple unique sources to solve a complex problem in product development. How did you ensure that all relevant insights were considered and what was the outcome': 'Multiple Sources of Input',
        'Give an example of a time when you demonstrated courageous conversations within a team or organizational context. How did you handle potential conflicts and disagreements and what positive outcomes resulted from these conversations': 'Courageous Conversations.',
        'Courageous Conversations.':'Courageous Conversations.',
        'Can you provide an example of a time when your deep understanding of business operations and financials influenced a significant decision How did this understanding contribute to the success of the decision and its impact on the organization': 'Deep Business Knowledge - understanding key business drivers such as cost optimization, market priorities etc.',
        'Share an example of a time when you demonstrated calculated risktaking. How did you balance the risks and rewards and what was the outcome of the decision': 'Calculated Risk Taking.',
        'Can you provide an example of a proactive decision you made to address a potential challenge or opportunity How did your proactive approach impact the outcome and what did you learn from the experience': 'Proactive Decision Making',
        'Describe a situation where you enabled decisionmaking closest to the work. How did you ensure that decisions were made by those with the most relevant knowledge and what benefits did this approach bring to the team and organization': 'Enables decision making',
        #mapping of CSP fields
        'Correctly identifies and articulates potential difficult situations.': 'Correctly identifies when and why a conversation is difficult and what role opinions, emotions, and stakes are at play in such situations.',
        'Recognizes when observations are challenged and responds effectively.': 'Able to turn difficult conversations into action and results',
        'Delivers presentations with clarity and confidence': 'Able to translate technical and functional complexities into plans and execution.',
        'Maintains composure and confident demeanor during presentations.': 'Deescalates emotionally charged situations through effective use of communication.',
        'Able to share opinions and acknowledgecounter other peoples views using facts and evidence.': 'Shares opinions and acknowledges others views',
        'Possesses welldefined ideas and opinions rooted in experience and demonstrates the ability to articulate and confidently advocate for them using facts and evidence.': 'Possesses well-defined, experience-based ideas and articulates them confidently.',
        'Able to bring people around to ones way of thinking about a certain topic without force or coercion whilst acknowledgingcounteracting their opinions with facts and evidence': 'Influences others perspectives effectively without force or coercion, while respecting their opinions.',
        'Balances shortterm and longterm aspects effectively.': 'Able to fulfil short-term expectations and focus deeply on defining the future agenda.',
        'Identifies emerging trends and allocates presentation time wisely': 'Recognizes Emerging Patterns and Trends.',
        #to solev error of the repeation
        'Recognizes emerging patterns and trends':'Recognizes Emerging Patterns and Trends.',
        'Executes presentations with high impact and maintains composure.': 'Identify drivers of the strategy and ensure execution effectiveness',
        #mapping of CSA fields
        'Brings Perspective  Teaches Brings diverse perspectives and multiple sources of input into the case study analysis.' : 'Brings Perspective & Teaches',
        'Strategically resolves everyday business challenges within the context of the case study.' :'Strategically resolves everyday business challenges',
        'Iterates for the best outcomes by leveraging internal data and external market insights.': 'Iterates for Best Outcomes',
        #this mapping is created to overcome the issue of the repetative work
        'Iterates for Best Outcomes ':'Iterates for Best Outcomes',
        'Addresses complex issues and proposes innovative solutions.' : 'Courageous Conversations.',
        'Shares and translates market insights effectively within the case study analysis' :'Shares & Translates Market Insights',
        'Creates comprehensive plans to deliver differentiated customer experiences based on the case study context.': 'Creates Plans to Deliver Differentiated Customer Experiences',
        'Connects various teams involved in the case study with shared customer goals to deliver outstanding solutions.' :'Connects Teams with Shared Customer Goals to Deliver', 
        'Develops an engagement plan collaborates with stakeholders and aligns with their expectations to meet customer needs as depicted in the case study.' : 'Sets up an engagement plan, collaborates with stakeholders, and aligns with their expectations to meet their needs.',
        'Demonstrates deep business knowledge understanding key business drivers relevant to the case study such as cost optimization market priorities and more.': 'Deep Business Knowledge - understanding key business drivers such as cost optimization, market priorities etc.',
        #create this for competency mapping
        'Deep Business Knowledge  understanding key business drivers suc as cost optimisation market prioritise etc.':'Deep Business Knowledge - understanding key business drivers such as cost optimization, market priorities etc.',
        'Shows calculated risktaking in decisionmaking within the case study context': 'Calculated Risk Taking.',
        'Exhibits an enterprise mindset by considering the broader organizational context in the case study analysis.' : 'Enterprise Mindset ',
        'Engages in proactive decisionmaking and enables decisionmaking closest to the work aligning with the case studys requirements.' : 'Proactive Decision Making',
        'Clearly explains the purpose and why certain actions or decisions are taken within the case study analysis' :'Explains Purpose & Why',
        'Sets specific team objectives that align with the case studys goals and requirements' : 'Sets Team Objectives',
        'Demonstrates effective priority management by allocating resources and attention to critical aspects highlighted in the case study' : 'Priority Management',
        'Ensures crossfunctional alignment in the case study analysis fostering collaboration and synergy among different teams and stakeholders.':'Cross-Functional Alignment',
        #mapping of GD
        'Explains Purpose  Why Articulates project purpose and connects decisions to customer preferences' : 'Explains Purpose & Why',
        'Sets Team Objectives':	'Sets Team Objectives',
        'CrossFunctional Alignment Develops crossfunctional alignment fostering effective communication and collaboration among team members from various departments to ensure customer preferences are met.' : 'Cross-Functional Alignment',
        'Identifies Difficult Conversations.': 'Correctly identifies when and why a conversation is difficult and what role opinions, emotions, and stakes are at play in such situations.',
        'Turns Difficult Conversations into Action' : 'Able to turn difficult conversations into action and results',
        'Balances Shortterm and Longterm Focus' : 'Able to fulfil short-term expectations and focus deeply on defining the future agenda.',
        'Uses Persuasion Techniques':'Adapts persuasion techniques based on the individuals personality.',
        'Says No Courageously.': 'Courageously says no and handles agreements and disagreements gracefully.',
        'Acknowledges Others Views' : 'Shares opinions and acknowledges others views',
        'Expresses Thoughts and Feelings Directly' : 'Expresses thoughts, feelings, and beliefs directly and appropriately',
        'Deescalates Emotionally Charged Situations.' : 'Deescalates emotionally charged situations through effective use of communication.',
        'Translates Complexities into Plans.' : 'Able to translate technical and functional complexities into plans and execution.',
        # mapping of the RP fields
        'Positive Authenticity  Courage': 'Positive Authenticity & Courage',
        'Talent Planning  Diverse Strong Pipelines' :'Talent Planning & Diverse, Strong Pipelines',
        'Collaborates  Connects' : 'Collaborates & Connects',
        '. Enables Decision Making' : 'Enables decision making closest to the work', 
        'Able to maintain composure in difficult situations' : 'Deescalates emotionally charged situations through effective use of communication.',
        }
    return competency_mapping.get(clean_descriptor, clean_descriptor)

# for mapping of descriptor to competency 
def get_competency_for_descriptor(descriptor):
    # Mapping of descriptors to their respective competencies
    competency_mapping = {
        # mapping for IA fields
        'IA_ShareAndTranslateMarketInsights_Q' : 'Delighting Customers: Solutions & Experience Creator',
        'IA_CreatesPlanstoDeliverDifferentiatedCustomerExperiences_Q' : 'Delighting Customers: Solutions & Experience Creator',
        'IA_ConnectsTeamswithSharedCustomerGoalstoDeliver_Q' : 'Delighting Customers: Solutions & Experience Creator',
        'IA_Setsupanengagementplancollaborateswithstakeholders_Q' : 'Delighting Customers: Solutions & Experience Creator',
        'IA_PositiveAuthenticityCourage_Q' : 'Inspiring People: Talent Cultivator',
        'IA_TalentPlanningGroomingAndDiverseStrongPipelines_Q' : 'Inspiring People: Talent Cultivator',
        'IA_FostersLearningAndHealthyWorkClimate_Q' : 'Inspiring People: Talent Cultivator',
        'IA_TalentPlanningDiverseStrongPipelinesOutside_Q' : 'Inspiring People: Talent Cultivator',
        #adding this to the another competency as per instructions
        'IA_CollaboratesAndConnects_Q' : 'Inspiring People: Talent Cultivator',
        'IA_BringPerspectiveandTeachesProfiecinet_Q' : 'Boldly Innovate: Catalyst',
        'IA_MultipleSourceOfInput_Q' : 'Boldly Innovate: Catalyst',
        'IA_IteratesForBestOutcomes_Q' : 'Boldly Innovate: Catalyst',
        'IA_CourageousConversation_Q' : 'Boldly Innovate: Catalyst',
        'IA_StandsUpForOwnRights_Q' : 'Communicating Assertively',
        'IA_AbelToShareOpinionsAndViews_Q' : 'Communicating Assertively',
        'IA_SaysNoCourageouslyAgreeandDisagrees_Q' : 'Communicating Assertively',
        'IA_PossessesWellDefinedIdeasAndOpinions_Q' : 'Communicating Assertively',
        'IA_UseseveralTechndependonPersonality_Q' : 'Communicating Assertively',
        #mapping of the CBI fields
        'CBI_Gather_Market_Insights_Action_Q'  : 'Delighting Customers: Solutions & Experience Creator',
        'CBI_Address_Customer_Complaint_Action_Q'  : 'Delighting Customers: Solutions & Experience Creator',
        'CBI_Anticipate_Customer_Needs_Solution_Q'  : 'Delighting Customers: Solutions & Experience Creator',
        'CBI_Identify_Talent_Networks_Use_Q'  : 'Inspiring People: Talent Cultivator',
        'CBI_Nurture_Develop_Talent_Approach_Q'  : 'Inspiring People: Talent Cultivator',
        'CBI_Collaborate_Create_Work_Climate_Q'  : 'Inspiring People: Talent Cultivator',
        'CBI_Bring_Perspectives_Challenging_Problem_Q'  : 'Boldly Innovate: Catalyst',
        'CBI_Gather_Input_Solve_Problem_Q'  : 'Boldly Innovate: Catalyst',
        'CBI_Courageous_Conversations_Outcomes_Q'  : 'Boldly Innovate: Catalyst',
        'CBI_Business_Understanding_Influence_Decision_Q'  : 'Own it: Business Leader',
        'CBI_Calculated_Risk_Taking_Outcome_Q'  : 'Own it: Business Leader',
        'CBI_Proactive_Decision_Impact_Q'  : 'Own it: Business Leader',
        'CBI_Enable_Close_Decision_Making_Q' : 'Own it: Business Leader',
        #mapping of CSP fields
        'CSP_difficult_situations_articulation_Q' : 'Conversing In Difficult Situations',
        'CSP_effective_response_to_challenges_Q' : 'Conversing In Difficult Situations',
        'CSP_presentation_clarity_confidence_Q' : 'Conversing In Difficult Situations',
        'CSP_composure_during_presentations_Q' : 'Conversing In Difficult Situations',
        'CSP_opinions_sharing_with_evidence_Q' : 'Communicating Assertively',
        'CSP_well_defined_ideas_advocacy_Q' : 'Communicating Assertively',
        'CSP_persuasion_without_coercion_Q' : 'Communicating Assertively',
        'CSP_balance_of_time_aspects_Q' : 'Leading With Strategy',
        'CSP_trend_identification_time_allocation_Q' : 'Leading With Strategy',
        'CSP_high_impact_presentation_execution_Q' : 'Leading With Strategy',
        #mapping of CSA fields
        'CSA_BringsPerspectiveAndTeaches_Q' :'Boldly Innovate: Catalyst',
        'CSA_Resolve_Business_Challenges_Q' :'Boldly Innovate: Catalyst',
        'CSA_Iterate_For_Outcomes_Q' :'Boldly Innovate: Catalyst',
        'CSA_Address_Complex_Issues_Q' :'Boldly Innovate: Catalyst',
        'CSA_Share_Market_Insights_Q' :'Delighting Customers: Solutions & Experience Creator',
        'CSA_Create_Customer_Experience_Plans_Q' :'Delighting Customers: Solutions & Experience Creator',
        'CSA_Connect_Teams_For_Solutions_Q' :'Delighting Customers: Solutions & Experience Creator',
        'CSA_Develop_Engagement_Plan_Q' :'Delighting Customers: Solutions & Experience Creator',
        'CSA_Demonstrate_Business_Knowledge_Q' :'Own it: Business Leader',
        'CSA_Calculated_Risk_Taking_Q' :'Own it: Business Leader',
        'CSA_Enterprise_Mindset_Q' :'Own it: Business Leader',
        'CSA_Proactive_Decision_Making_Q' :'Own it: Business Leader',
        'CSA_Explain_Purpose_And_Actions_Q' :'Prioritize: Sense Maker',
        'CSA_Set_Specific_Team_Objectives_Q' :'Prioritize: Sense Maker',
        'CSA_Priority_Management_Q' :'Prioritize: Sense Maker',
        'CSA_Ensure_Cross_Functional_Alignment_Q' :'Prioritize: Sense Maker',
        #mapping of the GD fields
        # 1st page of GD
        'GD_ExplainsPurposeandWhy_Q': 'Prioritize: Sense Maker',
        'GD_SetsTeamObjectives_Q': 'Prioritize: Sense Maker',
        'GD_PriorityManagement_Q': 'Prioritize: Sense Maker',
        'GD_CrossFunctionalAlignment_Q': 'Prioritize: Sense Maker',
        # 2nd page  of GD
        'GD_DifficultEmotionalConversations_Q': 'Conversing In Difficult Situations',
        'GD_TurnDifficultConversationsintoAction_Q': 'Conversing In Difficult Situations',
        'GD_TranslateintoFunctionalPlans_Q': 'Conversing In Difficult Situations',
        'GD_UtilizesEffectiveCommunicationtoDeescalateEmotionally_Q': 'Conversing In Difficult Situations',
        # 3rd page of GD 
        'GD_StandsupforOwnRights_Q': 'Communicating Assertively',
        'GD_ProactiveConversationPlanning_Q': 'Communicating Assertively',
        'GD_OpenCommunicationEnvironment_Q': 'Communicating Assertively',
        'GD_AssertivenessGraceandValidation_Q': 'Communicating Assertively',
        # 4th page of GD 
        'GD_MeetingImmediatewithStrategy_Q': 'Leading With Strategy',
        'GD_ForwardThinkingAgenda_Q': 'Leading With Strategy',
        'GD_EnsuringActionsStrategyAlignment_Q': 'Leading With Strategy',
        #mapping of the RP fields
        'RP_PositiveAuthenticityAndCourage_Q' : 'Inspiring People: Talent Cultivator',
        'RP_TalentPlanningAndDiverseStrongPipelines_Q' : 'Inspiring People: Talent Cultivator',
        'RP_CollaboratesAndConnects_Q' : 'Inspiring People: Talent Cultivator',
        'RP_DeepBusinessKnowledge_Q' : 'Own it: Business Leader',
        'RP_CalculatedRiskTaking_Q' : 'Own it: Business Leader',
        'RP_EnterpriseMindset_Q' : 'Own it: Business Leader',
        'RP_ProactiveDecisionMaking_Q' : 'Own it: Business Leader',
        'RP_EnablesDecisionMaking_Q' : 'Own it: Business Leader',
        'RP_Recognizesthroleofopinionsandstakes_Q' : 'Conversing In Difficult Situations',
        'RP_Abletoturndifficultconversationintoaction_Q' : 'Conversing In Difficult Situations',
        'RP_maintaincomposureindifficultsituations_Q' : 'Conversing In Difficult Situations',
        'RP_BalancingShorttermandLongtermGoals_Q' : 'Leading With Strategy',
        'RP_RecognizePatternandTrends_Q' : 'Leading With Strategy',
        'RP_StrategicAlignment_Q' : 'Leading With Strategy',
        'RP_AbletoAllocateRes_Q' : 'Leading With Strategy',
    }
    # Return the competency for the given descriptor, or 'Unknown Competency' if not found
    return competency_mapping.get(descriptor, 'Unknown Competency')

def instance_to_dict(instance):
    """Utility function to convert a model instance to a dictionary."""
    return {attr: getattr(instance, attr) for attr in inspect(instance).attrs.keys()} # type: ignore


# for preprocssing of text before LLM 
def clean_text(text, remove_leading_numbers=False, remove_no=False, remove_numbers=False):
    """Remove leading numbers followed by a period at the start of the text, the word 'no', and numbers from the given text based on flags."""
    if text != 'N/A':
        if remove_leading_numbers:
            # Updated to target only leading numbers followed by a period and optional space at the start of the string
            cleaned_text = re.sub(r'^\d+\.\s?', '', text)
        else:
            cleaned_text = text

        if remove_no:
            # Remove 'no' (case-insensitive)
            cleaned_text = re.sub(r'\bno\b', '', cleaned_text, flags=re.IGNORECASE)

        if remove_numbers:
            # Remove all numbers
            cleaned_text = re.sub(r'\d+', '', cleaned_text)
        
        # Remove punctuation (keeping periods and numbers if not removed by previous conditions)
        cleaned_text = re.sub(r'[^\w\s.]+', '', cleaned_text)
        return cleaned_text
    else:
        return text

