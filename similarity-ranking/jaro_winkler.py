import time
from typing import List

from loguru import logger


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


def jaro_winkler_similarity(s1: str, s2: str, p: float = 0.1) -> float:
    # Implementation of Jaro-Winkler similarity
    jaro_sim = jaro_similarity(s1, s2)

    # Calculate common prefix length
    prefix_len = 0
    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break

    # Calculate Jaro-Winkler similarity
    jaro_winkler_sim = jaro_sim + (prefix_len * p * (1 - jaro_sim))

    return jaro_winkler_sim


def compare_all(input_words: List[str], set_words: List[str]) -> List[dict]:
    start = time.time()

    results = []
    for input_word in input_words:
        for set_word in set_words:
            similarity = jaro_winkler_similarity(input_word, set_word)
            results.append(
                {
                    "input_word": input_word,
                    "set_word": set_word,
                    "similarity": similarity,
                }
            )

    logger.info(f"The ranking algorithm took {time.time() - start} seconds.")
    return results


if __name__ == "__main__":
    # Example usage
    input_words_test = ["LBL 34566", "9475632", "34566"]
    set_words_test = ["LBL 345532", "LBB 234545"]

    all_comparisons = compare_all(input_words_test, set_words_test)

    for comparison in all_comparisons:
        print(
            f"Input: {comparison['input_word']}, Set: {comparison['set_word']}, Similarity: {comparison['similarity']}"
        )
