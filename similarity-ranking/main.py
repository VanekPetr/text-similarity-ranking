import time
from typing import List

from data_loader import data_loader
from jaro_winkler_vanek import compare_all
from loguru import logger


def performance_statistics(test_data_path: str, confirmed_data_paths: List[str]):
    """Performance statistics for the similarity ranking model"""
    correct_confirmed, incorrect_confirmed, correct_other, incorrect_other = 0, 0, 0, 0
    processing_times = []

    extraction_alternatives_df, confirmed_extractions_df = data_loader(
        test_data_path, confirmed_data_paths
    )
    logger.info("✅ Data loaded successfully")

    unique_mail_envelope_ids: List[str] = extraction_alternatives_df[
        "mail_envelope_id"
    ].unique()
    number_of_tested_mail_envelope_ids: int = len(unique_mail_envelope_ids)
    logger.info(f"#️⃣ of unique mail envelope ids: {number_of_tested_mail_envelope_ids}")

    for mail_envelope_id in unique_mail_envelope_ids:
        extraction_alternatives: List[str] = (
            extraction_alternatives_df[
                extraction_alternatives_df["mail_envelope_id"] == mail_envelope_id
            ]["value"]
            .unique()
            .tolist()
        )

        domain: str = (
            extraction_alternatives_df[
                extraction_alternatives_df["mail_envelope_id"] == mail_envelope_id
            ]["domain"]
            .unique()
            .tolist()[0]
        )

        confirmed_extractions_for_domain: List[str] = confirmed_extractions_df[
            (confirmed_extractions_df["domain"] == domain)
            & (confirmed_extractions_df["mail_envelope_id"] != mail_envelope_id)
        ]["value"].tolist()

        correct_extraction: List[str] = confirmed_extractions_df[
            confirmed_extractions_df["mail_envelope_id"] == mail_envelope_id
        ]["value"].tolist()

        if len(correct_extraction) > 0:
            start = time.time()

            if len(confirmed_extractions_for_domain) > 0:
                results = compare_all(
                    extraction_alternatives,
                    confirmed_extractions_for_domain,
                    strategy="max",
                )
                if results[0]["input_word"] in correct_extraction[0]:
                    correct_confirmed += 1
                else:
                    incorrect_confirmed += 1
                    logger.debug(
                        f"results: {results}, correct: {correct_extraction[0]}, "
                        f"predicted: {results[0]['input_word']}, "
                        f"confirmed: {confirmed_extractions_for_domain}"
                    )

            else:
                number_of_tested_mail_envelope_ids -= 1
                confirmed_extractions: List[str] = confirmed_extractions_df[
                    confirmed_extractions_df["mail_envelope_id"] != mail_envelope_id
                    ]["value"].tolist()
                results = compare_all(
                    extraction_alternatives,
                    confirmed_extractions,
                    strategy="max",
                )
                if results[0]["input_word"] in correct_extraction[0]:
                    correct_other += 1
                else:
                    incorrect_other += 1
                    logger.debug(
                        f"results: {results}, correct: {correct_extraction[0]}, "
                        f"predicted: {results[0]['input_word']}, "
                        f"confirmed: {confirmed_extractions_for_domain}"
                    )

            processing_times.append(time.time() - start)

        else:
            logger.exception(
                f"No confirmed extractions for mail envelope id: {mail_envelope_id}"
            )
    logger.warning(f"🚫 Domains without confirmed cases other than correct extraction: "
                   f"{len(unique_mail_envelope_ids) - number_of_tested_mail_envelope_ids}")
    logger.info(
        f"🕙 Average prediction time: {round(sum(processing_times) / len(processing_times), 5)}s, "
        f"Total processing time: {round(sum(processing_times), 5)}s"
    )
    logger.info(
        f"🏁 Correct for cases with confirmed examples: {correct_confirmed}, "
        f"Incorrect: {incorrect_confirmed} out of {number_of_tested_mail_envelope_ids}"
    )
    logger.info(
        f"🏁 Correct for cases with confirmed examples: {correct_other},"
        f" Incorrect: {incorrect_other} out of {len(unique_mail_envelope_ids) - number_of_tested_mail_envelope_ids}"
    )
    logger.info(
        f"💪 Accuracy for cases with confirmed examples: "
        f"{round((correct_confirmed / number_of_tested_mail_envelope_ids) * 100, 2)}%"
    )
    logger.info(
        f"💪 Accuracy for cases without confirmed examples: "
        f"{round((correct_other / (len(unique_mail_envelope_ids) - number_of_tested_mail_envelope_ids)) * 100, 2)}%"
    )
    logger.info(
        f"💪 Total accuracy: "
        f"{round(((correct_confirmed + correct_other) / len(unique_mail_envelope_ids)) * 100, 2)}%"
    )


if __name__ == "__main__":
    performance_statistics(
        test_data_path="/data/all_extractions_train.csv",
        confirmed_data_paths=["/data/all_confirmed_mails_train.csv"],
    )
