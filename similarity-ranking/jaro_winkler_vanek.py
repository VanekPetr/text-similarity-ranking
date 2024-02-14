from typing import List

from jaro_winkler import jaro_winkler_similarity


def jaro_winkler_vanek_similarity(s1: str, s2: str, p_num_words: float = 0.1) -> float:
    # Implementation of Jaro-Winkler similarity
    jaro_winkler_sim = jaro_winkler_similarity(s1, s2)

    if len(s1.split()) == len(s2.split()):
        if len(s1.split()) > 1:
            number_of_words = min(len(s1.split()), 5)
            # Calculate Jaro-Winkler-Vanek similarity
            jaro_winkler_vanek_sim = jaro_winkler_sim + (
                number_of_words * p_num_words * (1 - jaro_winkler_sim)
            )
        else:
            if len(s1) == len(s2):
                number_of_chars = min(len(s1), 5)
                # Calculate Jaro-Winkler-Vanek similarity
                jaro_winkler_vanek_sim = jaro_winkler_sim + (
                    number_of_chars * p_num_words * (1 - jaro_winkler_sim)
                )
            else:
                jaro_winkler_vanek_sim = jaro_winkler_sim
    else:
        jaro_winkler_vanek_sim = jaro_winkler_sim

    return jaro_winkler_vanek_sim


def compare_all(
    input_words: List[str], set_words: List[str], strategy: str = "max"
) -> List[dict]:
    results = []
    for input_word in input_words:
        for set_word in set_words:
            similarity = jaro_winkler_vanek_similarity(input_word, set_word)
            results.append(
                {
                    "input_word": input_word,
                    "set_word": set_word,
                    "similarity": similarity,
                }
            )

    if strategy == "max":
        # take predictions just with max similarity for each input word
        results = [
            max(
                (item for item in results if item["input_word"] == input_word),
                key=lambda x: x["similarity"],
            )
            for input_word in input_words
        ]
    elif strategy == "average":
        # take average similarity for each input word
        results = [
            {
                "input_word": input_word,
                "similarity": sum(
                    item["similarity"]
                    for item in results
                    if item["input_word"] == input_word
                )
                / len(
                    [
                        item["similarity"]
                        for item in results
                        if item["input_word"] == input_word
                    ]
                ),
            }
            for input_word in input_words
        ]

    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results


if __name__ == "__main__":
    # Example usage
    input_words_test = ["LBL 34566", "9475632", "34566"]
    set_words_test = ["LBL 345532", "LBB 234545"]

    all_comparisons = compare_all(input_words_test, set_words_test)

    for comparison in all_comparisons:
        print(
            f"Input: {comparison['input_word']}, Similarity: {comparison['similarity']}"
        )
