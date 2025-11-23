import logging
import logging.handlers as handlers
import time

# Create a logger
logger = logging.getLogger('my_timed_app')
logger.setLevel(logging.INFO)

# Create a TimedRotatingFileHandler
# Arguments:
# - filename: The base name of the log file (e.g., 'app.log')
# - when: The interval type for rotation ('h' for hourly, 'midnight' for daily, 'w0' for weekly starting Monday, etc.)
# - interval: The number of 'when' intervals before rotation (e.g., 1 for daily at midnight)
# - backupCount: The number of old log files to keep (0 means keep all)
# - encoding: The encoding for the log file
# - utc: Whether to use UTC time for rotation
# - atTime: A datetime.time object specifying the time of day to rotate when 'when' is 'midnight' or 'd'
logHandler = handlers.TimedRotatingFileHandler(
    'app.log',
    # when='midnight',
    when='m',
    interval=1,
    backupCount=7,  # Keep 7 days of logs
    encoding='utf-8'
)

# Set the level for the handler
logHandler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(logHandler)

# Example logging messages
def main():
    while True:
        logger.info("This is a sample log message.")
        time.sleep(20) # Log every 5 seconds

if __name__ == "__main__":
    main()