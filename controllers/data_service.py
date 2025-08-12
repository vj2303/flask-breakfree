# controllers/data_service.py
from extension import db
from utils.text import clean_text, get_proper_descriptor, get_competency_for_descriptor

from models.competencies import ( InboxActivity, CBI, CaseStudyPresentation,CaseStudyAnalysis, GroupDiscussion, RolePlay)
from sqlalchemy import inspect
from models.participant import (Participants)
from typing import Dict, Tuple  # for type hinting


#for fetching all the data from DB tables
def fetch_all_data(participant_name):
    participant = Participants.query.filter_by(p_name=participant_name).first()
    if not participant:
        return {}, None
    #for fetching the data
    activities_data = {
        'Inbox Activity': InboxActivity.query.filter(InboxActivity.IA_participant_id == participant.p_id).all(),
        'CBI': CBI.query.filter(CBI.CBI_participant_id == participant.p_id).all(),
        'Case Study Presentation': CaseStudyPresentation.query.filter(CaseStudyPresentation.CSP_participant_id == participant.p_id).all(),
        'Case Study Analysis': CaseStudyAnalysis.query.filter(CaseStudyAnalysis.CSA_participant_id == participant.p_id).all(),
        'Group Discussion': GroupDiscussion.query.filter(GroupDiscussion.GD_participant_id == participant.p_id).all(),
        'Role Play': RolePlay.query.filter(RolePlay.RP_participant_id == participant.p_id).all()
    }

    result = {
        'participant_name': participant.p_name,
        'group': participant.p_group,
        'leader_name': participant.p_leader
    }

    competency_scores = {}
    #for data formatting table to proper data
    for activity_name, instances in activities_data.items():
        activity_data = {}
        for instance in instances:
            for attr in inspect(instance).attrs.keys():
                if attr.endswith('_Q'):
                    descriptor = getattr(instance, attr)
                    score = getattr(instance, attr.replace('_Q', '_v'), None)
                    comment = getattr(instance, attr.replace('_Q', '_la'), None)

                    clean_descriptor = clean_text(descriptor, remove_leading_numbers=True, remove_numbers=True)
                    clean_comment = clean_text(comment, remove_leading_numbers=True, remove_numbers=True) 
                    descriptor_mapping = get_proper_descriptor(clean_descriptor)
                    competency = get_competency_for_descriptor(attr)

                    if clean_comment.strip().upper() == 'NA':
                        score = 0
                        # continue

                    if score is None:
                        continue

                    if competency not in competency_scores:
                        competency_scores[competency] = []
                    if score is not None:
                        competency_scores[competency].append(score)

                    descriptor_key = attr[:-2]  # Remove '_Q' from the descriptor
                    if descriptor_key in activity_data:
                        existing_entry = activity_data[descriptor_key]
                        existing_score = existing_entry[2] if existing_entry[2] is not None else 0
                        new_score = (existing_score + score) / 2
                        activity_data[descriptor_key][2] = new_score

                        existing_comment = existing_entry[3]
                        activity_comment = f"{clean_comment} Activity Name: {activity_name}"  # Include activity name
                        new_comment = (existing_comment + " " + activity_comment).strip() if existing_comment else activity_comment
                        activity_data[descriptor_key][3] = new_comment
                    else:
                        activity_comment = f"{clean_comment} Activity Name: {activity_name}"  # Include activity name
                        activity_data[descriptor_key] = [competency, descriptor_mapping, score, activity_comment]

        if activity_data:
            result[activity_name.replace(' ', '_').lower()] = activity_data
 
    average_scores = {}
    for comp, scores in competency_scores.items():
        valid_scores = [s for s in scores if s is not None and s != 0]
        average_scores[comp] = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else None
   
    result['average_scores'] = average_scores 

    return result, participant

#for fetching all the data from DB tables
def fetch_all_data_for_leader(participant_name):
    participant = Participants.query.filter_by(p_name=participant_name).first()
    if not participant:
        return {}, None
    #for fetching the data
    activities_data = {
        'Inbox Activity': InboxActivity.query.filter(InboxActivity.IA_participant_id == participant.p_id).all(),
        'CBI': CBI.query.filter(CBI.CBI_participant_id == participant.p_id).all(),
        'Case Study Presentation': CaseStudyPresentation.query.filter(CaseStudyPresentation.CSP_participant_id == participant.p_id).all(),
        'Case Study Analysis': CaseStudyAnalysis.query.filter(CaseStudyAnalysis.CSA_participant_id == participant.p_id).all(),
        'Group Discussion': GroupDiscussion.query.filter(GroupDiscussion.GD_participant_id == participant.p_id).all(),
        'Role Play': RolePlay.query.filter(RolePlay.RP_participant_id == participant.p_id).all()
    }

    result = {}

    competency_scores = {}
    #for data formatting table to proper data
    for activity_name, instances in activities_data.items():
        activity_data = {}
        for instance in instances:
            for attr in inspect(instance).attrs.keys():
                if attr.endswith('_Q'):
                    descriptor = getattr(instance, attr)
                    score = getattr(instance, attr.replace('_Q', '_v'), None)
                    comment = getattr(instance, attr.replace('_Q', '_la'), None)

                    clean_descriptor = clean_text(descriptor, remove_leading_numbers=True, remove_numbers=True)
                    clean_comment = clean_text(comment, remove_leading_numbers=True, remove_numbers=True) 
                    descriptor_mapping = get_proper_descriptor(clean_descriptor)
                    competency = get_competency_for_descriptor(attr)

                    if clean_comment.strip().upper() == 'NA':
                        score = 0
                        # continue

                    if score is None:
                        continue

                    if competency not in competency_scores:
                        competency_scores[competency] = []
                    if score is not None:
                        competency_scores[competency].append(score)

                    descriptor_key = attr[:-2]  # Remove '_Q' from the descriptor
                    if descriptor_key in activity_data:
                        existing_entry = activity_data[descriptor_key]
                        existing_score = existing_entry[2] if existing_entry[2] is not None else 0
                        new_score = (existing_score + score) / 2
                        activity_data[descriptor_key][2] = new_score

                        existing_comment = existing_entry[3]
                        activity_comment = f"{clean_comment} Activity Name: {activity_name}"  # Include activity name
                        new_comment = (existing_comment + " " + activity_comment).strip() if existing_comment else activity_comment
                        activity_data[descriptor_key][3] = new_comment
                    else:
                        activity_comment = f"{clean_comment} Activity Name: {activity_name}"  # Include activity name

    average_scores = {}
    for comp, scores in competency_scores.items():
        valid_scores = [s for s in scores if s is not None and s != 0]
        average_scores[comp] = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else None
   
    result['average_scores'] = average_scores 

    return result
