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
def show_intro():
    """Display an introduction message about TuskyTux."""
    print("\n🚀 Welcome to TuskyTux - Your Decentralized Storage Companion! 🚀\n")
    
    print("TuskyTux is a Linux-based open-source tool that allows you to mount your "
          "Tusky decentralized storage as a drive on your system.")
    
    print("\n🔗 Don't have an API Key yet? Register here: https://app.tusky.io/account/api-keys\n")
    
    print("📌 Features & Commands Overview:")
    print("  - `help`: Show available commands and usage.")
    print("  - `mount`: Mount your Tusky storage as a drive.")
    print("  - `unmount`: Unmount the drive.")
    print("  - `status`: Check mount status.")
    print("  - `config`: Manage API Key and settings.\n")
    
    print("💡 Run `help` to see all available commands!\n")
    
    print("❤️ Dedicated to Linux & Open-Source Enthusiasts! ❤️")
    print("🌐 Visit: \033[4;34mhttps://meacodes.com\033[0m\n")