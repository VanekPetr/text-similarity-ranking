import time
from typing import List
import pandas as pd
import ast

from data_loader import data_loader
from jaro_winkler_vanek import compare_all
from loguru import logger


def performance_statistics(test_data_path: str):
    """Performance statistics for the similarity ranking model"""
    correct, incorrect = 0, 0
    processing_times = []

    test_data = data_loader(test_data_path)
    logger.info("✅ Data loaded successfully")
    logger.info(f"#️⃣ of unique data points: {len(test_data)}")
    save_data = pd.DataFrame(columns=["text_inputs", "to_compare_with", "the_most_similar"])

    for tested_example in test_data.iterrows():
        start = time.time()

        text_inputs: List[str] = ast.literal_eval(tested_example[1]["text_inputs"])
        to_compare_with: List[str] = ast.literal_eval(tested_example[1]["to_compare_with"])
        the_most_similar: List[str] = ast.literal_eval(tested_example[1]["the_most_similar"])

        results = compare_all(text_inputs, to_compare_with, strategy="average",)
        to_print = {res["input_word"]: res["similarity"] for res in results}

        if results[0]["input_word"] in the_most_similar:
            correct += 1
        else:
            incorrect += 1
            logger.debug(
                f"⚠️ result: {to_print}, "
                f"correct: {the_most_similar[0]}, "
                f"confirmed: {to_compare_with}"
            )

        processing_times.append(time.time() - start)

    logger.info(
        f"🕙 Average prediction time: {round(sum(processing_times) / len(processing_times), 5)}s, "
        f"Total processing time: {round(sum(processing_times), 5)}s"
    )
    logger.info(f"🏁 Correct cases: {correct}, Incorrect cases: {incorrect} out of {len(test_data)}")
    logger.info(f"💪 Accuracy: {round((correct / len(test_data)) * 100, 2)}%")


if __name__ == "__main__":
    performance_statistics(test_data_path="/data/test_data.csv")
