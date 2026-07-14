import logging

# creates logging for the system.
def setup_logger():

 # format each log with: timestamp, log level, acutal log message
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    return logging.getLogger("job-system")