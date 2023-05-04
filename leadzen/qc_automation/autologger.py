import os
import logging


def Logger(filename: str):  # type: ignore
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(filename, mode="w")
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(message)s")
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger
