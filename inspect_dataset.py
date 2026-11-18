import pandas as pd

df = pd.read_csv("burglary_incidents.csv")

dimensions = df.shape
print(dimensions)

first_rows = df.head()
print(first_rows)

df.info(verbose=True)

missing_per_column = df.isna().sum()
print(missing_per_column)

pt_values = df["property_type"].nunique()
pt_value_counts = df["property_type"].value_counts()

ep_values = df["entry_point"].nunique()
ep_value_counts = df["entry_point"].value_counts()

em_values = df["entry_method"].nunique()
em_value_counts = df["entry_method"].value_counts()

tc_values = df["target_category"].nunique()
tc_value_counts = df["target_category"].value_counts()

print(pt_values)
print(pt_value_counts)
print(ep_values)
print(ep_value_counts)
print(em_values)
print(em_value_counts)
print(tc_values)
print(tc_value_counts)

offenders = df.groupby(["offender_id"])
incidents_per_offender = offenders.size()
repeat_offenders_series = incidents_per_offender >= 2
ge2_offenders = incidents_per_offender[repeat_offenders_series]

categories = [
    "property_type",
    "entry_point",
    "entry_method",
    "target_category"
]

for category in categories:
    category_per_offender = offenders[category].nunique()
    repeat_category_per_offender = category_per_offender.loc[ge2_offenders.index].value_counts()
    print(repeat_category_per_offender)

    print(df[category].value_counts())

    offender_plus_category = df.groupby(["offender_id", category])
    incidents_per_group = offender_plus_category.size()
    print(f"\n{category}:")
    print(incidents_per_group)

df_repeat = df[df["offender_id"].isin(ge2_offenders.index)]
entry_methods = df_repeat.groupby(["entry_method"])
unique_oids = entry_methods["offender_id"].nunique() / len(ge2_offenders) * 100
print(unique_oids.map(lambda x: f"{x:.1f}%"))