# This version includes console logger for a more sophisticated approach if not headless
# Implement rotating only changes FileHandler to RotatingHandler
""" Notes 
Child log:
- Use child loggers for module-specific logging.
- Modularity:   Each module or class has its own logger.
- Hierarchy:    Child loggers inherit the configuration of the parent logger.
- Clarity:      Log message includes the hierarchy.
- logger.getChild('submodule')
"""

import logging
import os

# Logger setup
def setup_logger():
    logger = logging.getLogger("MainLogger")
    logger.setLevel(logging.DEBUG)

    # Create log directory
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # File handler
    file_handler = logging.FileHandler(f"{log_dir}/app.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Main logger
main_logger = setup_logger()

# Class 1: Using a child logger
class ModuleA:
    def __init__(self):
        self.logger = main_logger.getChild("ModuleA")

    def perform_task(self):
        self.logger.info("Starting task in ModuleA.")
        try:
            # Simulated logic
            self.logger.debug("Performing step 1 in ModuleA.")
            result = "Step 1 result"
            self.logger.info(f"Step 1 completed with result: {result}")

            self.logger.debug("Performing step 2 in ModuleA.")
            self.logger.info("Step 2 completed successfully.")
        except Exception as e:
            self.logger.error(f"An error occurred in ModuleA: {e}")
        finally:
            self.logger.info("Task in ModuleA completed.")

# Class 2: Using another child logger
class ModuleB:
    def __init__(self):
        self.logger = main_logger.getChild("ModuleB")

    def perform_task(self):
        self.logger.info("Starting task in ModuleB.")
        try:
            # Simulated logic
            self.logger.debug("Performing step 1 in ModuleB.")
            result = "Step 1 result in ModuleB"
            self.logger.info(f"Step 1 completed with result: {result}")

            self.logger.debug("Performing step 2 in ModuleB.")
            self.logger.warning("Step 2 in ModuleB encountered a potential issue.")
        except Exception as e:
            self.logger.error(f"An error occurred in ModuleB: {e}")
        finally:
            self.logger.info("Task in ModuleB completed.")

# Main execution
if __name__ == "__main__":
    module_a = ModuleA()
    module_b = ModuleB()

    module_a.perform_task()
    module_b.perform_task()


    
""" Example Output 
2025-01-03 15:30:00 - MainLogger.ModuleA - INFO - Starting task in ModuleA.
2025-01-03 15:30:01 - MainLogger.ModuleA - INFO - Step 1 completed with result: Step 1 result
2025-01-03 15:30:02 - MainLogger.ModuleA - INFO - Step 2 completed successfully.
2025-01-03 15:30:03 - MainLogger.ModuleA - INFO - Task in ModuleA completed.
2025-01-03 15:30:04 - MainLogger.ModuleB - INFO - Starting task in ModuleB.
2025-01-03 15:30:05 - MainLogger.ModuleB - INFO - Step 1 completed with result: Step 1 result in ModuleB
2025-01-03 15:30:06 - MainLogger.ModuleB - WARNING - Step 2 in ModuleB encountered a potential issue.
2025-01-03 15:30:07 - MainLogger.ModuleB - INFO - Task in ModuleB completed.
"""