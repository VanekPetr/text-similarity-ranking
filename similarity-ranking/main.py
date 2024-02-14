from data_loader import data_loader
from loguru import logger


def test_performance():
    data, data = data_loader(
        test_data_path="/data/all_extractions_train.csv",
        confirmed_data_paths=["/data/all_confirmed_mails_train.csv"],
    )
    logger.info("Data loaded successfully")


if __name__ == "__main__":
    test_performance()
