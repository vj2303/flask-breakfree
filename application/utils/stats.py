# utils/stats.py
from typing import List, Dict
from collections import defaultdict
import numpy as np
import pandas as pd

def calculate_overall_average(all_scores):
    """
    Average numeric values for matching keys across multiple dicts.
    """
     
    overall_average = {}
    count_valid = {}
    
    if not all_scores:
        return overall_average
    
    # Initialize overall_average and count_valid with keys from the first dictionary
    for key in all_scores[0].keys():
        overall_average[key] = 0
        count_valid[key] = 0
    
    # Sum up all scores for each key, ignoring NaNs
    for scores in all_scores:
        for key, value in scores.items():
            if not pd.isna(value):
                overall_average[key] += value
                count_valid[key] += 1
    
    # Calculate the average for each key
    for key in overall_average.keys():
        if count_valid[key] > 0:
            overall_average[key] /= count_valid[key]
        else:
            overall_average[key] = np.nan  # or some other value to indicate no valid data
    
    return overall_average
