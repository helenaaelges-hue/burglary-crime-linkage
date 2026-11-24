# Computational Crime Linkage Analysis for Residential Burglary

A Python-based research prototype investigating computational similarity measures for identifying and ranking potentially linked residential burglary incidents.

## Project Overview

This project explores how behavioral, spatial, and temporal characteristics can be used to calculate similarity between residential burglary incidents.

Two approaches to calculating overall similarity are implemented and compared:

- **Equal-weight similarity:** Behavioral, spatial, and temporal similarity contribute equally to the overall score.
- **Weighted similarity:** Behavioral similarity receives a weight of 0.20, while spatial and temporal similarity each receive a weight of 0.40.

The prototype ranks existing incidents according to their similarity to a reference incident and evaluates the resulting rankings against known relationships in a synthetic dataset.

## Project Status

The initial research prototype and preliminary evaluation have been implemented. Further development and evaluation are planned.

## Dataset

The project uses a synthetic dataset containing 450 residential burglary incidents, including 40 recurring offender profiles and additional single-incident cases.

The dataset contains behavioral, spatial, and temporal attributes. Artificial coordinates are used for spatial comparisons. Offender identifiers serve exclusively as ground truth for evaluation and are not used in similarity calculations.

## Methodology

The prototype compares incidents using three feature groups:

- **Behavioral:** Property type, entry point, entry method, and target category. Categorical characteristics are compared using exact matching.
- **Spatial:** Euclidean distance between incident coordinates, transformed into a similarity score using exponential decay.
- **Temporal:** Date proximity and circular time-of-day similarity, combined into a single temporal score.

Missing feature values are treated as unavailable comparisons rather than mismatches. Overall similarity scores are calculated using the available feature groups.

## Evaluation

The two scoring approaches are evaluated using 40 reference incidents. Each reference incident is compared against the remaining 449 incidents.

Performance is assessed using:

- Precision@10
- Recall@10
- F1@10

The preliminary results show a slightly higher mean F1@10 for the weighted approach (0.455) than for the equal-weight approach (0.436).

## Technologies

- Python
- pandas

## Project Structure

- `similarity.py` – Implements feature-level and overall incident similarity calculations.
- `test.py` – Performs ranking evaluation and calculates performance metrics.
- `burglary_incidents.csv` – Synthetic burglary incident dataset.
- Dataset generation and inspection scripts – Support dataset creation and examination.

## Running the Project

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Run the evaluation script:

```bash
python test.py
```

The evaluation script loads the synthetic dataset, compares reference incidents against the remaining cases, and calculates ranking performance metrics.

## Limitations

This project is an experimental research prototype using synthetic data. Its results do not establish real-world investigative effectiveness.

The system is intended as a research exploration of computational crime linkage and as a potential decision-support approach. It does not identify offenders or establish that incidents were committed by the same individual.
