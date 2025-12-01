import logging
import os
from datetime import datetime


class Logger:
    """Custom logger class for test framework"""

    _loggers = {}

    @staticmethod
    def get_logger(name: str = __name__) -> logging.Logger:
        """
        Get or create a logger instance

        Args:
            name: Logger name (typically __name__)

        Returns:
            logging.Logger: Configured logger instance
        """
        if name in Logger._loggers:
            return Logger._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        # File handler
        log_file = os.path.join(logs_dir, f'automation_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers if not already added
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        Logger._loggers[name] = logger
        return logger

    @staticmethod
    def log_step(logger: logging.Logger, step_description: str):
        """
        Log a test step with special formatting

        Args:
            logger: Logger instance
            step_description: Description of the step
        """
        logger.info(f"{'='*80}")
        logger.info(f"STEP: {step_description}")
        logger.info(f"{'='*80}")

    @staticmethod
    def log_assertion(logger: logging.Logger, assertion_description: str, result: bool):
        """
        Log an assertion result

        Args:
            logger: Logger instance
            assertion_description: Description of what is being asserted
            result: True if assertion passed, False otherwise
        """
        status = "PASSED" if result else "FAILED"
        log_level = logging.INFO if result else logging.ERROR
        logger.log(log_level, f"ASSERTION [{status}]: {assertion_description}")
