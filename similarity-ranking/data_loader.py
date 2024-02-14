import os
from typing import List

import pandas as pd

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# load confirmed data from data/all_confirmed_mails_train.csv
def load_confirmed_data(paths: List[str]) -> pd.DataFrame:
    confirmed_extractions: pd.DataFrame = pd.DataFrame()
    for path in paths:
        confirmed_extractions_tmp: pd.DataFrame = pd.read_csv(PARENT_DIR + path)
        # delete all rows where value is empty
        confirmed_extractions_tmp = confirmed_extractions_tmp.dropna(subset=["value"])
        confirmed_extractions = pd.concat(
            [confirmed_extractions, confirmed_extractions_tmp]
        ).reset_index(drop=True)

    return confirmed_extractions


# load all extractions from data/all_extractions.csv
def load_all_extractions(path: str) -> pd.DataFrame:
    all_extractions: pd.DataFrame = pd.read_csv(PARENT_DIR + path)
    # delete all rows where value is empty
    all_extractions = all_extractions.dropna(subset=["value"])
    # create domain column from sender domain to take part of sender after @ sign
    all_extractions["domain"] = all_extractions["sender"].str.split("@").str[1]

    return all_extractions


def data_loader(
    test_data_path: str, confirmed_data_paths: List[str]
) -> (pd.DataFrame, pd.DataFrame):
    confirmed_data: pd.DataFrame = load_confirmed_data(confirmed_data_paths)
    all_extractions: pd.DataFrame = load_all_extractions(test_data_path)

    # both confirmed_data and all_extractions has column mail_envelope_id
    # create domain column in confirmed_data based on domains in all_extractions which match the envelope_ids
    confirmed_data = confirmed_data.merge(
        all_extractions[["mail_envelope_id", "domain"]],
        on="mail_envelope_id",
        how="left",
    )
    # drop duplicated rows
    confirmed_data = confirmed_data.drop_duplicates(subset=["mail_envelope_id"])
    confirmed_data = confirmed_data.dropna(subset=["domain"])

    return all_extractions, confirmed_data


if __name__ == "__main__":

    extractions, confirmations = data_loader(
        test_data_path="/data/all_extractions_train.csv",
        confirmed_data_paths=["/data/all_confirmed_mails_train.csv"],
    )

    print(extractions.head())
    print(confirmations.head())
    print("Data loaded successfully")
