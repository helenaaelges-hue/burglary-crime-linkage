import math

def categorical_similarity(case_1, case_2):
    if case_1 is None or case_2 is None:
        return None
    if case_1 == case_2:
        return 1.0
    return 0.0

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt(pow((x2-x1), 2) + pow((y2-y1), 2))

def spatial_similarity(distance):
    return math.exp(- distance / 20)

def date_similarity(days_difference):
    return math.exp(-days_difference / 60)

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