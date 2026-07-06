import logging

# Creates structured logging for the system.
def setup_logger():

 # Format each log with: timestamp, log level, actual log message
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    return logging.getLogger("job-system")