import sys
from utils import (
    show_logo, show_intro, command_loop, ensure_config_file
)

def main():
    """Main entry point of TuskyTux CLI."""
    config = ensure_config_file()  # Load or create config file
    show_logo()   # Display ASCII logo
    show_intro()  # Display introduction
    command_loop(config)  # Pass config to command loop

if __name__ == "__main__":
    main()
