import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

NUM_INCIDENTS = 450
NUM_OFFENDERS = 40

FEATURES = [
    "case_id",
    "offender_id",
    "date_time",
    "property_type",
    "entry_point",
    "entry_method",
    "target_category",
    "location_x",
    "location_y"
]

PROPERTY_TYPES = [
    "detached_house",
    "apartment",
    "semi_detached_house",
    "terraced_house"
]

ENTRY_POINTS = [
    "front_door",
    "rear_door",
    "front_window",
    "rear_window",
    "side_window"
]

ENTRY_METHODS = [
    "forced_entry",
    "unlocked_entry",
    "lock_manipulation",
    "window_breaking"
]

TARGET_CATEGORIES = [
    "electronics",
    "jewelry",
    "cash",
    "valuables",
    "multiple_categories"
]

def generate_offender_profiles(num_offenders):
    profiles = {}

    for offender_number in range(1, num_offenders + 1):
        offender_id = f"O{offender_number:03d}"

        profiles[offender_id] = {
            "property_type": random.choice(PROPERTY_TYPES),
            "entry_point": random.choice(ENTRY_POINTS),
            "entry_method": random.choice(ENTRY_METHODS),
            "target_category": random.choice(TARGET_CATEGORIES),
            "base_x": random.uniform(0, 100),
            "base_y": random.uniform(0, 100),
            "preferred_hour": random.randint(0, 23)
        }

    return profiles

def choose_characteristic(preferred_value, possible_values, consistency=0.7):
    if random.random() < consistency:
        return preferred_value
    else:
        return random.choice(possible_values)

def generate_incident(case_id, offender_id, profile, start_date):
    incident_date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    incident_hour = int(random.gauss(profile["preferred_hour"], 2))
    incident_hour = max(0, min(23, incident_hour))

    incident_time = incident_date.replace(
        hour=incident_hour,
        minute=random.choice([0, 15, 30, 45])
    )

    return {
        "case_id": case_id,
        "offender_id": offender_id,
        "date_time": incident_time,
        "property_type": choose_characteristic(
            profile["property_type"], PROPERTY_TYPES
        ),
        "entry_point": choose_characteristic(
            profile["entry_point"], ENTRY_POINTS
        ),
        "entry_method": choose_characteristic(
            profile["entry_method"], ENTRY_METHODS
        ),
        "target_category": choose_characteristic(
            profile["target_category"], TARGET_CATEGORIES
        ),
        "location_x": round(
            max(0, min(100, random.gauss(profile["base_x"], 8))), 2
        ),
        "location_y": round(
            max(0, min(100, random.gauss(profile["base_y"], 8))), 2
        )
    }

def generate_linked_incidents(profiles, start_date):
    incidents = []
    case_number = 1

    for offender_id, profile in profiles.items():
        for _ in range(8):
            case_id = f"C{case_number:03d}"

            incident = generate_incident(
                case_id,
                offender_id,
                profile,
                start_date
            )

            incidents.append(incident)
            case_number += 1

    return incidents

def generate_unlinked_incidents(num_incidents, start_date, start_case_number):
    incidents = []

    for i in range(num_incidents):
        case_id = f"C{start_case_number + i:03d}"

        incident_date = start_date + timedelta(
            days=random.randint(0, 364)
        )

        incident_time = incident_date.replace(
            hour=random.randint(0, 23),
            minute=random.choice([0, 15, 30, 45])
        )

        incident = {
            "case_id": case_id,
            "offender_id": f"O{40 + i + 1:03d}",
            "date_time": incident_time,
            "property_type": random.choice(PROPERTY_TYPES),
            "entry_point": random.choice(ENTRY_POINTS),
            "entry_method": random.choice(ENTRY_METHODS),
            "target_category": random.choice(TARGET_CATEGORIES),
            "location_x": round(random.uniform(0, 100), 2),
            "location_y": round(random.uniform(0, 100), 2)
        }

        incidents.append(incident)

    return incidents

def generate_dataset():
    start_date = datetime(2025, 1, 1)

    profiles = generate_offender_profiles(NUM_OFFENDERS)

    linked_incidents = generate_linked_incidents(
        profiles, start_date
    )

    num_unlinked = NUM_INCIDENTS - len(linked_incidents)

    unlinked_incidents = generate_unlinked_incidents(
        num_unlinked,
        start_date,
        len(linked_incidents) + 1
    )

    incidents = linked_incidents + unlinked_incidents

    random.shuffle(incidents)

    dataset = pd.DataFrame(incidents, columns=FEATURES)
    dataset = introduce_missing_values(dataset)

    return dataset

def introduce_missing_values(dataset, missing_rate=0.05):
    dataset = dataset.copy()

    columns = [
        "property_type",
        "entry_point",
        "entry_method",
        "target_category",
        "location_x",
        "location_y"
    ]

    for column in columns:
        mask = dataset[column].apply(
            lambda value: random.random() < missing_rate
        )

        dataset.loc[mask, column] = None

    return dataset

if __name__ == "__main__":
    dataset = generate_dataset()

    assert len(dataset) == NUM_INCIDENTS
    assert dataset["case_id"].is_unique

    distribution = dataset["offender_id"].value_counts().value_counts().to_dict()
    assert distribution == {1: 130, 8: 40}

    assert dataset[["case_id", "offender_id", "date_time"]].notnull().all().all()

    assert dataset["location_x"].min() >= 0
    assert dataset["location_x"].max() <= 100
    assert dataset["location_y"].min() >= 0
    assert dataset["location_y"].max() <= 100

    print("All dataset validation checks passed!")

    dataset.to_csv("burglary_incidents.csv", index=False)

    print("Dataset generated successfully!")
    print(f"Number of incidents: {len(dataset)}")
    print(f"Number of columns: {len(dataset.columns)}")
    print(dataset.head())

    print("\nIncidents per offender:")
    print(dataset["offender_id"].value_counts().value_counts().sort_index())

    print("\nMissing values per column:")
    print(dataset.isnull().sum())

    print("\nCoordinate ranges:")
    print("X:", dataset["location_x"].min(), "to", dataset["location_x"].max())
    print("Y:", dataset["location_y"].min(), "to", dataset["location_y"].max())