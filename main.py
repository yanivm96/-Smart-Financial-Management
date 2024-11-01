import logging
from UI.console_ui import start_app_ui
from src.config import configure_logging

configure_logging() # Initialize logging

def main() -> None:
    logging.info("Strting main function")
    start_app_ui()


if __name__ == "__main__":
    main()

