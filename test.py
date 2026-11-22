import pandas as pd
from similarity import compare_incidents, equal_weight_similarity, weighted_similarity

df = pd.read_csv("burglary_incidents.csv")
df["date_time"] = pd.to_datetime(df["date_time"])

case_1 = df.iloc[0]
case_2 = df.iloc[1]

scores = compare_incidents(case_1, case_2)

equal_score = equal_weight_similarity(scores)
weighted_score = weighted_similarity(scores)

print("Feature scores:", scores)
print("Equal weight score:", equal_score)
print("Weighted score:", weighted_score)