def categorical_similarity(case_1, case_2):
    if case_1 is None or case_2 is None:
        return None
    if case_1 == case_2:
        return 1.0
    return 0.0