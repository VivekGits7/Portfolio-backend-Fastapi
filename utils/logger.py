import logging

# Configure basic logging once for the entire app
logging.basicConfig(
    level=logging.INFO,  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)

# Helper function to get a logger instance per file
def get_logger(name: str):
    return logging.getLogger(name)
