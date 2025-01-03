import logging
import os

# Logging setup
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(f"{log_dir}/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("TaskLogger")

# Define the function with logging
def task_A():
    logger.info("Starting task_A")  # Log when the function starts

    try:
        # Example: Task logic here
        logger.debug("Performing step 1 in task_A")
        result = "Result of step 1"

        logger.info(f"Step 1 completed with result: {result}")

        logger.debug("Performing step 2 in task_A")
        # Simulate potential warning or error
        if not result:
            logger.warning("Step 2 may not proceed due to missing result")
        
        logger.info("Step 2 completed successfully")
    
    except Exception as e:
        logger.error(f"An error occurred in task_A: {e}")
        raise  # Re-raise the exception after logging

    finally:
        logger.info("Finished task_A")  # Log when the function ends

# Main execution
if __name__ == "__main__":
    task_A()
