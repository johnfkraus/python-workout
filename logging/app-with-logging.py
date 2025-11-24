import logging
import os
from pathlib import Path
import ct_logging
from typing import Generator

LOG_FILE_NAME = Path(f"log/{os.path.basename(__file__).split('.')[0]}.log")


logger = ct_logging.get_logger(
    "app-with-logging",
    LOG_FILE_NAME,
    log_level=logging.DEBUG)


def make_an_error_and_yield() -> Generator[str, None, None]:
    yield "hey 1"
    try:
        print(1/0)
    except ZeroDivisionError as e:
        logger.error("An error occurred")  #, e)
    yield "hey 2"


def main() -> None:
    logger.debug("a debug message")
    logger.error("Error message")
    logger.debug("Debug message")
    logger.info("Info message")

    logger.info(f"The current file name is: {os.path.basename(__file__)=}")
    logger.info(f"{__name__=}")
    print(list(make_an_error_and_yield()))


if __name__ == "__main__":
    main()
