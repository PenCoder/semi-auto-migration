# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

import logging


def _setup_basic_logging() -> None:
    """
    Configure basic logging to console.

    In a larger application, this should be replaced by a centralized
    logging configuration. For M2, this is sufficient to understand
    failures and behaviour during hardware inventory runs.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] hardware: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
