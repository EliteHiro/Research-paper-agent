import logging


def get_logger(name: str):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler = logging.StreamHandler()

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
