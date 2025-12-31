from __future__ import annotations
from logging import Logger

from .logger import SingletonLogger


def main() -> None:
    logger: Logger = SingletonLogger.get_logger()

    logger.info("Application started.")
    logger.debug("Debug message example.")
    logger.warning("Warning example.")
    logger.error("Error example.")
    logger.critical("Critical example.")

    # Demonstrating singleton behavior
    same_logger = SingletonLogger.get_logger()
    logger.info(f"Logger objects identical? {logger is same_logger}")


if __name__ == "__main__":
    main()

