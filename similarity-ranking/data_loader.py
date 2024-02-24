import os

import pandas as pd

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def data_loader(test_data_path: str) -> pd.DataFrame:
    """Load test data from csv file"""

    data: pd.DataFrame = pd.read_csv(PARENT_DIR + test_data_path)
    # delete all rows where text_inputs is empty
    data = data.dropna(subset=["text_inputs"])
    # drop duplicated rows
    data = data.drop_duplicates()

    return data


if __name__ == "__main__":

    test_data = data_loader(
        test_data_path="/data/test_data.csv",
    )

    print(test_data.head())
    print("Data loaded successfully")
