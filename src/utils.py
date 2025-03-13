import os
import subprocess

def show_logo():
    """Display the ASCII logo stored in a text file."""
    logo_path = "assets/logo_ascii.txt"

    if not os.path.exists(logo_path):
        print("Error: ASCII logo file not found!")
        return

    with open(logo_path, "r", encoding="utf-8") as f:
        print(f.read())
        
def show_intro():
    """Display an introduction message about TuskyTux."""
    print("\n Welcome to TuskyTux - Your Decentralized Storage Companion! \n")
    
    print("TuskyTux is a Linux-based open-source tool that allows you to mount your "
          "Tusky decentralized storage as a drive on your system.")
    
    print("\n🔗 Don't have an API Key yet? Register here: https://app.tusky.io/account/api-keys\n")
    
    print("Features & Commands Overview:")
    print("  - `help`: Show available commands and usage.")
    print("  - `mount`: Mount your Tusky storage as a drive.")
    print("  - `unmount`: Unmount the drive.")
    print("  - `status`: Check mount status.")
    print("  - `config`: Manage API Key and settings.\n")
    
    print("💡 Run `help` to see all available commands!\n")
    
    print(" Dedicated to Linux & Open-Source Enthusiasts! ")
    print(" https://meacodes.com/tuskytux\n")