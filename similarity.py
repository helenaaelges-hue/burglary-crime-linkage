import math
import pandas as pd

def categorical_similarity(case_1, case_2):
    if pd.isna(case_1) or pd.isna(case_2):
        return None
    if case_1 == case_2:
        return 1.0
    return 0.0

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt(pow((x2-x1), 2) + pow((y2-y1), 2))

def spatial_similarity(distance):
    return math.exp(- distance / 20)

def days_between(date_time_1, date_time_2):
    diff = date_time_1.date() - date_time_2.date()
    days = diff.days
    return abs(days)

def date_similarity(days_difference):
    return math.exp(-days_difference / 60)

def extract_time(date_time):
    return date_time.time().strftime("%H:%M")

def time_to_minutes(time):
    h_min = time.split(":")
    for i in range(len(h_min)):
        h_min[i] = int(h_min[i])
    total_mins = (h_min[0] * 60) + h_min[1]
    return total_mins

def circular_time_difference(time_1, time_2):
    diff = time_1 - time_2
    abs_diff = abs(diff)
    return min(abs_diff, 1440 - abs_diff)

def time_of_day_similarity(circ_time_diff):
    return 1 - (circ_time_diff/720)

def combined_temporal_similarity(date_score, time_score):
    return (date_score + time_score) / 2

def temporal_similarity(date_time_1, date_time_2):
    days_difference = days_between(date_time_1, date_time_2)
    date_score = date_similarity(days_difference)
    timestamp_1 = extract_time(date_time_1)
    time_1 = time_to_minutes(timestamp_1)
    timestamp_2 = extract_time(date_time_2)
    time_2 = time_to_minutes(timestamp_2)
    circ_time_diff = circular_time_difference(time_1, time_2)
    time_score = time_of_day_similarity(circ_time_diff)
    final_score = combined_temporal_similarity(date_score, time_score)
    return final_score

def behavioral_similarity(case_1, case_2):
    pt = categorical_similarity(case_1["property_type"], case_2["property_type"])
    ep = categorical_similarity(case_1["entry_point"], case_2["entry_point"])
    em = categorical_similarity(case_1["entry_method"], case_2["entry_method"])
    tc = categorical_similarity(case_1["target_category"], case_2["target_category"])

    category_scores = [
        pt,
        ep,
        em,
        tc
    ]

    filtered_category_scores = [x for x in category_scores if x is not None]

    if filtered_category_scores:
        avg = sum(filtered_category_scores) / len(filtered_category_scores)
        return avg
    else:
        return None

def incident_spatial_similarity(case_1, case_2):
    if pd.isna(case_1["location_x"]) or pd.isna(case_1["location_y"]) or pd.isna(case_2["location_x"]) or pd.isna(case_2["location_y"]):
        return None
    distance = euclidean_distance(case_1["location_x"], case_1["location_y"], case_2["location_x"], case_2["location_y"])
    return spatial_similarity(distance)

def compare_incidents(case_1, case_2):
    behavioral = behavioral_similarity(case_1, case_2)
    spatial = incident_spatial_similarity(case_1, case_2)
    temporal = temporal_similarity(case_1["date_time"], case_2["date_time"])

    scores = {
        "behavioral": behavioral,
        "spatial": spatial,
        "temporal": temporal
    }

    return scores

def equal_weight_similarity(scores):
    filtered_scores = [x for x in scores.values() if x is not None]
    if filtered_scores:
        return sum(filtered_scores) / len(filtered_scores)
    return None

def weighted_similarity(scores):
    weights = {
        "behavioral": 0.20,
        "spatial": 0.40,
        "temporal": 0.40
    }
    filtered_scores = {key: val for key, val in scores.items() if val is not None}
    if filtered_scores:
        weighted_total = 0
        available_weight = 0
        for key, val in filtered_scores.items():
            weighted_total += val * weights[key]
            available_weight += weights[key]
        return weighted_total / available_weight
    return None

