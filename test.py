import pandas as pd
from similarity import compare_incidents, equal_weight_similarity, weighted_similarity

df = pd.read_csv("burglary_incidents.csv")
df["date_time"] = pd.to_datetime(df["date_time"])

reference_case = df.iloc[1]
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
linked_cases = df[(df["offender_id"] == reference_case["offender_id"]) & (df["case_id"] != reference_case["case_id"])]

def evaluate_ranking(ranked_cases, linked_cases):
    top_10 = ranked_cases[:10]
    top_10_case_ids = []
    for case in top_10:
        top_10_case_ids.append(case["case_id"])
    top_10_set = set(top_10_case_ids)
    linked_cases_set = set(linked_cases["case_id"])
    overlap_cases = top_10_set & linked_cases_set
    precision = len(overlap_cases) / len(top_10)
    recall = len(overlap_cases) / len(linked_cases)

    return precision, recall

equal_precision, equal_recall = evaluate_ranking(equal_ranked, linked_cases)
weighted_precision, weighted_recall = evaluate_ranking(weighted_ranked, linked_cases)

print(equal_precision, equal_recall, weighted_precision, weighted_recall)