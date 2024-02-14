def jaro_similarity(s1: str, s2: str) -> float:
    # Implementation of Jaro similarity
    s1_len = len(s1)
    s2_len = len(s2)

    # Matching window size
    window = max(s1_len, s2_len) // 2 - 1

    # Initialize matching counts
    match_count = 0
    transpositions = 0

    # Initialize lists to hold matching characters
    s1_matches = [False] * s1_len
    s2_matches = [False] * s2_len

    # Count matching characters
    for i in range(s1_len):
        start = max(0, i - window)
        end = min(i + window + 1, s2_len)
        for j in range(start, end):
            if not s2_matches[j] and s1[i] == s2[j]:
                match_count += 1
                s1_matches[i] = True
                s2_matches[j] = True
                break

    if match_count == 0:
        return 0.0

    # Count transpositions
    k = 0
    for i in range(s1_len):
        if s1_matches[i]:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

    transpositions //= 2

    # Calculate Jaro similarity
    jaro_similarity = (
        match_count / s1_len
        + match_count / s2_len
        + (match_count - transpositions) / match_count
    ) / 3

    return jaro_similarity


def jaro_winkler_similarity(
    s1: str, s2: str, p: float = 0.1, max_prefix_len: int = 9
) -> float:
    # Implementation of Jaro-Winkler similarity
    jaro_sim = jaro_similarity(s1, s2)

    # Calculate common prefix length
    prefix_len = 0
    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            prefix_len += 1
            if prefix_len == max_prefix_len:
                break
        else:
            break

    # Calculate Jaro-Winkler similarity
    jaro_winkler_sim = jaro_sim + (prefix_len * p * (1 - jaro_sim))

    return jaro_winkler_sim
