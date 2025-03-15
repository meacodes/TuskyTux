import os
import json
import requests
import time

# Constants
CONFIG_FILE = "tuskytux_config.json"  # Path to store API Key
TUSKY_API_URL = "https://api.tusky.io/api-keys"  # Tusky API endpoint for key validation
VAULTS_API_URL = "https://api.tusky.io/vaults"  # Replace with actual endpoint
LOGO_PATH = "assets/logo_ascii.txt"

def ensure_config_file():
    """Check if the config file exists, create it if not, and load the configuration."""
    if not os.path.exists(CONFIG_FILE):
        print("⚠️ Config file not found! Creating a new one...")
        config = {"api_keys": {}, "active_api": None}
        save_config(config)
        return config
    else:
        return load_config()


def load_config():
    """Load the configuration from file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        if "api_keys" not in config:
            config["api_keys"] = {}
        if "active_api" not in config:
            config["active_api"] = None

        return config

    except (json.JSONDecodeError, FileNotFoundError):
        print("❌ Error: Config file is corrupted or missing. Resetting to default.")
        config = {"api_keys": {}, "active_api": None}
        save_config(config)
        return config

def save_config(config):
    """Save the configuration to file."""
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")


def show_logo():
    """Display the ASCII logo stored in a text file."""
    if not os.path.exists(LOGO_PATH):
        print("❌ Error: ASCII logo file not found!")
        return

    with open(LOGO_PATH, "r", encoding="utf-8") as f:
        print(f.read())

def show_intro():
    """Display an introduction message about TuskyTux."""
    print("\nWelcome to TuskyTux - Your Decentralized Storage Companion!\n")
    print("TuskyTux is a Linux-based open-source tool that allows you to mount your "
          "Tusky decentralized storage as a drive on your system.")
    print("\n🔗 Don't have an API Key yet? Register here: https://app.tusky.io/account/api-keys\n")
    print("❤ Dedicated to the open source community with love: https://meacodes.com\n")

def show_loading(message="Validating API Key..."):
    """Display a loading animation while connecting to Tusky API."""
    print(message, end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

def list_api_keys(config):
    """List all stored API Keys."""
    if not config["api_keys"]:
        print("⚠️ No API Keys found.")
        return
    
    print("\n🔑 Stored API Keys:")
    for key, status in config["api_keys"].items():
        active_marker = "✅" if config["active_api"] == key else "❌"
        print(f"  {active_marker} {key} ({status})")

def add_api_key(config):
    """Add a new API Key."""
    while True:
        api_key = input("\nEnter new API Key (or type 'cancel' to go back): ").strip()
        if api_key.lower() == "cancel":
            print("❌ Operation canceled. Returning to the previous menu.")
            return

        if not api_key:
            print("⚠️ API Key cannot be empty.")
            continue

        show_loading()
        headers = {"Api-Key": api_key}
        try:
            response = requests.get(TUSKY_API_URL, headers=headers, timeout=5)
            if response.status_code == 200:
                config["api_keys"][api_key] = "inactive"
                if not config["active_api"]:
                    config["active_api"] = api_key
                    config["api_keys"][api_key] = "active"
                save_config(config)
                print("✅ API Key added successfully!")
                break
            else:
                print("❌ Invalid API Key.")
        except requests.RequestException as e:
            print(f"\n❌ API request failed: {e}")

def remove_api_key(config):
    """Remove an existing API Key."""
    if not config["api_keys"]:
        print("⚠️ No API Keys found.")
        return

    list_api_keys(config)
    while True:
        api_key = input("\nEnter API Key to remove (or type 'cancel' to go back): ").strip()
        if api_key.lower() == "cancel":
            print("❌ Operation canceled. Returning to the previous menu.")
            return

        if api_key in config["api_keys"]:
            del config["api_keys"][api_key]
            if config["active_api"] == api_key:
                config["active_api"] = None if not config["api_keys"] else next(iter(config["api_keys"]))
                if config["active_api"]:
                    config["api_keys"][config["active_api"]] = "active"
            save_config(config)
            print("✅ API Key removed successfully!")
            return
        else:
            print("⚠️ API Key not found. Please enter a valid key.")

def set_active_api_key(config):
    """Set an API Key as active."""
    if not config["api_keys"]:
        print("⚠️ No API Keys found.")
        return

    list_api_keys(config)
    while True:
        api_key = input("\nEnter API Key to set as active (or type 'cancel' to go back): ").strip()
        if api_key.lower() == "cancel":
            print("❌ Operation canceled. Returning to the previous menu.")
            return

        if api_key in config["api_keys"]:
            for key in config["api_keys"]:
                config["api_keys"][key] = "inactive"
            config["api_keys"][api_key] = "active"
            config["active_api"] = api_key
            save_config(config)
            print("✅ API Key set as active!")
            return
        else:
            print("⚠️ API Key not found. Please enter a valid key.")


def config_menu(config):
    """Submenu for managing API Keys."""
    print("\n🔧 API Key Management")
    print("Type 'config help' for available options.\n")

    while True:
        command = input("🛠️ Config Command: ").strip().lower()

        if command == "config help":
            print("\nConfig commands:")
            print("  list      - Show stored API Keys")
            print("  add       - Add a new API Key")
            print("  remove    - Remove an API Key")
            print("  set       - Set an API Key as active")
            print("  back      - Return to main menu\n")
        elif command == "list":
            list_api_keys(config)
        elif command == "add":
            add_api_key(config)
        elif command == "remove":
            remove_api_key(config)
        elif command == "set":
            set_active_api_key(config)
        elif command == "back":
            break
        else:
            print("⚠️ Invalid command. Type 'config help' for options.")

def get_active_api_key():
    """Retrieve the active API key from the configuration file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config.get("active_api")  # Return the active API key
    except (FileNotFoundError, json.JSONDecodeError):
        return None  # Return None if the config file does not exist or is invalid


def list_vaults():
    """Fetch and display the list of vaults using the active API key."""
    api_key = get_active_api_key()
    if not api_key:
        print("⚠️ No active API key is set.")
        return

    headers = {"api-key": api_key}  # API key is required for authentication
    try:
        response = requests.get(VAULTS_API_URL, headers=headers)  # Send GET request
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()  # Parse JSON response

        vaults = data.get("items", [])  # Extract the list of vaults
        if not vaults:
            print("🔹 No vaults found.")
            return

        print("\n🔐 Vaults List:")
        for vault in vaults:
            vault_id = vault.get("id", "N/A")  # Get vault ID
            name = vault.get("name", "Unknown")  # Get vault name
            description = vault.get("description", "No Description")  # Get vault description
            status = vault.get("status", "Unknown")  # Get vault status
            encrypted = "🔒 Encrypted" if vault.get("encrypted") else "🔓 Unencrypted"  # Check encryption status

            print(f"  📁 {name} ({status})")
            print(f"     🆔 ID: {vault_id}")
            print(f"     ℹ️  {description}")
            print(f"     {encrypted}\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching vault data: {e}")

def add_vault():
    """Prompt the user to create a new vault with optional fields."""
    
    api_key = get_active_api_key()
    if not api_key:
        print("⚠️ No active API key is set.")
        return

    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }

    # Getting initial information from the user
    name = input("🏷️ Enter Vault Name (Required): ").strip()
    while not name:
        print("❌ Name cannot be empty!")
        name = input("🏷️ Enter Vault Name (Required): ").strip()

    description = input("ℹ️ Enter Description (Optional): ").strip()
    
    tags = input("🏷️ Enter Tags (comma separated, Optional): ").strip()
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else []

    encrypted = input("🔒 Do you want to encrypt the vault? (yes/no, Default: no): ").strip().lower()
    encrypted = True if encrypted == "yes" else False

    # If the encrypted vaults requires additional keys
    keys = []
    if encrypted:
        add_keys = input("🔑 Do you want to add encryption keys? (yes/no, Default: no): ").strip().lower()
        if add_keys == "yes":
            while True:
                key = input("🔐 Enter encryption key (or press Enter to skip): ").strip()
                if not key:
                    break
                keys.append({"key": key})
    
    # Creating JSON data for sending to an API
    vault_data = {
        "name": name,
        "description": description if description else None,
        "tags": tags_list,
        "encrypted": encrypted,
        "keys": keys
    }

    # Removing None fields from JSON
    vault_data = {k: v for k, v in vault_data.items() if v}

    # Sending a Vault creation request
    try:
        response = requests.post(VAULTS_API_URL, headers=headers, json=vault_data)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Vault created successfully! 🆔 ID: {data.get('id')}")
    except requests.RequestException as e:
        print(f"❌ Failed to create vault: {e}")


def vaults_menu(config):
    """Submenu for managing Vaults."""
    print("\n🔐 Vault Management")
    print("Type 'vaults help' for available options.\n")

    while True:
        command = input("🔒 Vault Command: ").strip().lower()

        if command == "vaults help":
            print("\nVaults commands:")
            print("  list      - Show vaults list")
            print("  add       - Add a new Vault")
            print("  remove    - Remove a vault")
            print("  active    - Set a vault as active")
            print("  back      - Return to main menu\n")
        elif command == "list":
            list_vaults()  # Call the function to list vaults
        elif command == "add":
            add_vault()  # Call the function to add vaults
        elif command == "back":
            break
        else:
            print("⚠️ Invalid command. Type 'vaults help' for options.")

def command_loop(config):
    """Keep the program running and accept user commands."""
    print("\n✅ TuskyTux is ready! Type 'help' to see available commands.\n")

    while True:
        command = input("🖥️  Command: ").strip().lower()

        if command == "help":
            print("\nAvailable commands:")
            print("  config    - Manage API Key and settings")
            print("  vaults    - Manage Vaults and settings")
            print("  close     - Exit the program\n")
        elif command == "config":
            config_menu(config)
        elif command == "vaults":
            vaults_menu(config)
        elif command == "close":
            print("👋 Exiting TuskyTux. Goodbye!")
            break
        else:
            print("⚠️ Invalid command. Type 'help' to see available commands.")

if __name__ == "__main__":
    config = load_config()
    show_logo()
    show_intro()
    command_loop(config)
