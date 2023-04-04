import os
import logging



def Logger(filename):
    # create logger for "QC Automation"
    logger = logging.getLogger('QC Automation')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs debug messages
    fh = logging.FileHandler(filename, mode='w')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger