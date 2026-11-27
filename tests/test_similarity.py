import math
import pandas as pd
import pytest
from datetime import datetime

from similarity import (
    categorical_similarity,
    euclidean_distance,
    spatial_similarity,
    incident_spatial_similarity,
    temporal_similarity,
    days_between,
    date_similarity,
    circular_time_difference,
    time_of_day_similarity,
    behavioral_similarity,
    compare_incidents,
    equal_weight_similarity,
    weighted_similarity
)

def test_categorical_matching_values():
    result = categorical_similarity("window", "window")
    assert result == 1.0

def test_categorical_different_values():
    result = categorical_similarity("window", "door")
    assert result == 0.0

def test_categorical_missing_first_value():
    result = categorical_similarity(None, "window")
    assert result is None

def test_categorical_missing_second_value():
    result = categorical_similarity("window", None)
    assert result is None

def test_categorical_both_values_missing():
    result = categorical_similarity(None, None)
    assert result is None

def test_categorical_nan_value():
    result = categorical_similarity(float("nan"), "window")
    assert result is None

def test_euclidean_distance():
    result = euclidean_distance(0, 0, 3, 4)
    assert result == 5.0

def test_spatial_similarity_at_zero_distance():
    result = spatial_similarity(0)
    assert result == 1.0

def test_spatial_similarity_decreases_with_distance():
    near = spatial_similarity(10)
    far = spatial_similarity(30)
    assert near > far

def test_incident_spatial_similarity_missing_coordinates():
    case_1 = {
        "location_x": None,
        "location_y": 10
    }
    case_2 = {
        "location_x": 20,
        "location_y": 10
    }
    result = incident_spatial_similarity(case_1, case_2)
    assert result is None

def test_days_between():
    date_1 = datetime(2025, 1, 10, 12, 0)
    date_2 = datetime(2025, 1, 5, 12, 0)
    assert days_between(date_1, date_2) == 5

def test_date_similarity_same_day():
    assert date_similarity(0) == 1.0

def test_circular_time_difference_across_midnight():
    result = circular_time_difference(23 * 60, 1 * 60)
    assert result == 120

def test_time_of_day_similarity_same_time():
    assert time_of_day_similarity(0) == 1.0

def test_temporal_similarity_same_datetime():
    date_time = datetime(2025, 1, 10, 14, 30)
    assert temporal_similarity(date_time, date_time) == 1.0

def test_behavioral_similarity_all_matching():
    case_1 = {
        "property_type": "house",
        "entry_point": "window",
        "entry_method": "forced",
        "target_category": "electronics"
    }
    case_2 = case_1.copy()

    assert behavioral_similarity(case_1, case_2) == 1.0


def test_behavioral_similarity_all_different():
    case_1 = {
        "property_type": "house",
        "entry_point": "window",
        "entry_method": "forced",
        "target_category": "electronics"
    }
    case_2 = {
        "property_type": "apartment",
        "entry_point": "door",
        "entry_method": "unforced",
        "target_category": "jewelry"
    }

    assert behavioral_similarity(case_1, case_2) == 0.0


def test_behavioral_similarity_all_missing():
    case_1 = {
        "property_type": None,
        "entry_point": None,
        "entry_method": None,
        "target_category": None
    }
    case_2 = case_1.copy()

    assert behavioral_similarity(case_1, case_2) is None


def test_equal_weight_similarity():
    scores = {
        "behavioral": 1.0,
        "spatial": 0.5,
        "temporal": 0.0
    }

    assert equal_weight_similarity(scores) == 0.5


def test_weighted_similarity():
    scores = {
        "behavioral": 1.0,
        "spatial": 0.5,
        "temporal": 0.0
    }

    expected = (1.0 * 0.2 + 0.5 * 0.4 + 0.0 * 0.4)
    assert weighted_similarity(scores) == expected


def test_weighted_similarity_renormalizes_missing_scores():
    scores = {
        "behavioral": None,
        "spatial": 1.0,
        "temporal": 0.0
    }

    assert weighted_similarity(scores) == 0.5


def test_equal_weight_similarity_all_missing():
    scores = {
        "behavioral": None,
        "spatial": None,
        "temporal": None
    }

    assert equal_weight_similarity(scores) is None

def test_compare_incidents_returns_all_score_groups():
    case_1 = {
        "property_type": "house",
        "entry_point": "window",
        "entry_method": "forced",
        "target_category": "electronics",
        "location_x": 10,
        "location_y": 20,
        "date_time": datetime(2025, 1, 10, 14, 30)
    }

    case_2 = {
        "property_type": "house",
        "entry_point": "window",
        "entry_method": "forced",
        "target_category": "electronics",
        "location_x": 10,
        "location_y": 20,
        "date_time": datetime(2025, 1, 10, 14, 30)
    }

    result = compare_incidents(case_1, case_2)

    assert set(result.keys()) == {"behavioral", "spatial", "temporal"}
    assert result["behavioral"] == 1.0
    assert result["spatial"] == 1.0
    assert result["temporal"] == 1.0