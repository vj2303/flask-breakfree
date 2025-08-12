# utils/excel.py
import pandas as pd

# this function return the the data for table columns
def read_scores_from_excel(participant_name,file_path):
    # Load the data
    # Create an ExcelFile object
    xls = pd.ExcelFile(file_path)
    # Read data from Sheet1
    df = pd.read_excel(xls, 'Sheet1')

    df2 = df.loc[:, ~df.columns.isin(['Grand Total', 'Grand Total.1'])]
    # Filter the row for the given participant
    participant_scores = df2[df2['Row Labels'] == participant_name]

    return participant_scores

def read_scores_from_excel_for_leader(participant_name, file_path):
    # Load the data
    xls = pd.ExcelFile(file_path)
    # Read data from Sheet1
    df = pd.read_excel(xls, 'Sheet1')

    df2 = df.loc[:, ~df.columns.isin(['Grand Total', 'Grand Total.1'])]
    # Filter the row for the given participant
    participant_scores = df2[df2['Row Labels'] == participant_name]

    # Assuming the scores are in the required columns
    participant_scores_dict = participant_scores.drop(columns=['Row Labels']).mean().to_dict()
    
    return participant_scores_dict