import pandas as pd
from similarity import compare_incidents, equal_weight_similarity, weighted_similarity

df = pd.read_csv("burglary_incidents.csv")
df["date_time"] = pd.to_datetime(df["date_time"])

reference_case = df.iloc[0]
results = []

for index, candidate in df.iterrows():
    if index == 0:
        continue
    scores = compare_incidents(reference_case, candidate)
    equal_score = equal_weight_similarity(scores)
    weighted_score = weighted_similarity(scores)
    results.append(
        {
            "case_id": candidate["case_id"],
            "equal_score": equal_score,
            "weighted_score": weighted_score
        }
    )

equal_ranked = sorted(results, key=lambda x: x["equal_score"], reverse=True)
weighted_ranked = sorted(results, key=lambda x: x["weighted_score"], reverse=True)

print(weighted_ranked[:10])