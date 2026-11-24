import pandas as pd
from similarity import compare_incidents, equal_weight_similarity, weighted_similarity

df = pd.read_csv("burglary_incidents.csv")
df["date_time"] = pd.to_datetime(df["date_time"])

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

def calculate_f1(precision, recall):
    if precision == 0 and recall == 0:
        return 0.0
    f1 = 2 * ((precision * recall) / (precision + recall))
    return f1

counts = df["offender_id"].value_counts()
repeat_offenders = counts[counts > 1]
repeat_offender_ids = repeat_offenders.index.tolist()
reference_cases = []
for offender_id in repeat_offender_ids:
    first_case = df[df["offender_id"] == offender_id].iloc[0]
    reference_cases.append(first_case)

all_evaluations = []
for reference_case in reference_cases:
    linked_cases = df[(df["offender_id"] == reference_case["offender_id"]) & (df["case_id"] != reference_case["case_id"])]
    results = []
    for _, candidate in df.iterrows():
        if candidate["case_id"] == reference_case["case_id"]:
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
    equal_precision, equal_recall = evaluate_ranking(equal_ranked, linked_cases)
    weighted_precision, weighted_recall = evaluate_ranking(weighted_ranked, linked_cases)
    equal_f1 = calculate_f1(equal_precision, equal_recall)
    weighted_f1 = calculate_f1(weighted_precision, weighted_recall)

    top_10_equal_case_ids = [case["case_id"] for case in equal_ranked[:10]]
    top_10_weighted_case_ids = [case["case_id"] for case in weighted_ranked[:10]]
    all_evaluations.append({
        "equal_top_10": top_10_equal_case_ids,
        "weighted_top_10": top_10_weighted_case_ids,
        "reference_case_id": reference_case["case_id"],
        "reference_offender_id": reference_case["offender_id"],
        "equal_precision": equal_precision,
        "equal_recall": equal_recall,
        "equal_f1": equal_f1,
        "weighted_precision": weighted_precision,
        "weighted_recall": weighted_recall,
        "weighted_f1": weighted_f1
    })

evaluation_df = pd.DataFrame(all_evaluations)
mean_equal_precision = evaluation_df["equal_precision"].mean()
mean_equal_recall = evaluation_df["equal_recall"].mean()
mean_equal_f1 = evaluation_df["equal_f1"].mean()
mean_weighted_precision = evaluation_df["weighted_precision"].mean()
mean_weighted_recall = evaluation_df["weighted_recall"].mean()
mean_weighted_f1 = evaluation_df["weighted_f1"].mean()

evaluation_df["precision_difference"] = (
    evaluation_df["equal_precision"] - evaluation_df["weighted_precision"]
)
evaluation_df["recall_difference"] = (
    evaluation_df["equal_recall"] - evaluation_df["weighted_recall"]
)
evaluation_df["f1_difference"] = (
    evaluation_df["equal_f1"] - evaluation_df["weighted_f1"]
)

mean_f1_difference = evaluation_df["f1_difference"].mean()
std_f1_difference = evaluation_df["f1_difference"].std()

std_equal_f1 = evaluation_df["equal_f1"].std()
std_weighted_f1 = evaluation_df["weighted_f1"].std()

std_equal_precision = evaluation_df["equal_precision"].std()
std_equal_recall = evaluation_df["equal_recall"].std()

std_weighted_precision = evaluation_df["weighted_precision"].std()
std_weighted_recall = evaluation_df["weighted_recall"].std()

print("\nStandard deviations")
print("Equal-weight Precision@10:", std_equal_precision)
print("Equal-weight Recall@10:", std_equal_recall)
print("Equal-weight F1@10:", std_equal_f1)
print("Weighted Precision@10:", std_weighted_precision)
print("Weighted Recall@10:", std_weighted_recall)
print("Weighted F1@10:", std_weighted_f1)

print("\nPaired F1 difference (equal - weighted)")
print("Mean F1 difference:", mean_f1_difference)
print("Standard deviation of F1 difference:", std_f1_difference)

print("\nF1 comparison across reference cases")
equal_better_f1 = (evaluation_df["f1_difference"] > 0).sum()
weighted_better_f1 = (evaluation_df["f1_difference"] < 0).sum()
both_equal_f1 = (evaluation_df["f1_difference"] == 0).sum()

print("Equal-weight performed better:", equal_better_f1)
print("Weighted performed better:", weighted_better_f1)
print("Both performed equally:", both_equal_f1)

print("\nEvaluation overview")
print("Number of reference cases:", len(reference_cases))
print("Total incidents:", len(df))
print("Candidates per reference case:", len(df) - 1)
print("Average relevant cases per reference:", evaluation_df["reference_offender_id"].map(counts).sub(1).mean())