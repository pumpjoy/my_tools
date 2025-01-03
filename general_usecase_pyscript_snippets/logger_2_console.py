# This version includes console logger for a more sophisticated approach if not headless
""" Notes
FileHandler -   Logs message to file (such as app.log). 
            -   Useful for headless and long-term debugging
            -   Uses a formatter to structure w/ timestamps and other metadata by user.

StreamHandler-  Logs messages to console
             -  Useful for real-time debugging
             -  Usess separate formatter than FileHandler
             
Log Levels:
- DEBUG: Detailed diagnostic information.
- INFO: General operational messages.
- WARNING: Indications of potential issues or important runtime events.
- ERROR: Errors that prevent the program from performing a specific function.
- CRITICAL: Serious errors that likely terminate the program.

Custom Formatting:
- Adjust `format` and `datefmt`. 
"""
import logging
import os

def setup_logger():
    # Create a logger
    logger = logging.getLogger("TaskLogger")
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level for the logger

    # Create a directory for logs if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a file handler for logging to a file
    file_handler = logging.FileHandler(f"{log_dir}/app.log")
    file_handler.setLevel(logging.INFO)  # Set the logging level for file handler
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Create a console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set the logging level for console handler
    console_formatter = logging.Formatter(
        "%(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger()

# Example function with logging
def task_A():
    logger.info("Starting task_A")
    try:
        logger.debug("Performing step 1 in task_A")
        result = "Some result"
        logger.info(f"Step 1 completed: {result}")

        logger.debug("Performing step 2 in task_A")
        if not result:
            logger.warning("Step 2 may not work as expected")
        else:
            logger.info("Step 2 completed successfully")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    finally:
        logger.info("Finished task_A")

if __name__ == "__main__":
    task_A()
    