import os
import subprocess

def show_logo():
    """Convert and display the logo in the terminal with adaptive dimensions."""
    logo_path = "assets/logo.png"

    if not os.path.exists(logo_path):
        print("Error: Logo file not found!")
        return

    # Get terminal size
    terminal_size = os.get_terminal_size()
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines

    # Set dimensions based on terminal size
    width = max(terminal_width - 10, 50)  # Leave some margin
    height = max(terminal_height // 3, 10)  # Keep it proportional

    try:
        # Correct way to pass -d flag with two values
        subprocess.run(["ascii-image-converter", "-C", "-d", f"{width},{height}", logo_path])
    except Exception as e:
        print(f"Error displaying logo: {e}")
