#!/usr/bin/env python3
# This line specifies that the script should be executed using the python3 interpreter.

import selenium
# Imports the main Selenium library, which provides tools for browser automation.
from selenium import webdriver
# Imports the webdriver module from Selenium, used to control web browsers.
from selenium.webdriver.chrome.options import Options
# Imports the Options class for configuring Chrome browser settings.
from selenium.webdriver.chrome.service import Service
# Imports the Service class for managing the ChromeDriver executable.
from selenium.webdriver.common.by import By
# Imports the By class, used to specify how to locate elements on a web page (e.g., by XPath).
from selenium.webdriver.common.keys import Keys
# Imports the Keys class, which provides special keys like ENTER, CONTROL, etc.
from selenium.webdriver.support.ui import WebDriverWait
# Imports the WebDriverWait class, used for waiting for specific conditions on a web page.
from selenium.webdriver.support import expected_conditions as EC
# Imports the expected_conditions module, containing predefined conditions to wait for.
from selenium.webdriver.common.action_chains import ActionChains
# Imports the ActionChains class, used for performing complex user interactions like key presses and mouse movements.
from selenium.common.exceptions import TimeoutException, WebDriverException
# Imports specific Selenium exceptions for handling timeouts and browser-related errors.
import pyperclip
# Imports the pyperclip library, used for interacting with the system clipboard (copy and paste).
import json
# Imports the json library, used for working with JSON data (for the configuration file).
import os
# Imports the os library, which provides a way of using operating system dependent functionality.
import time
# Imports the time library, used for adding delays and measuring time.
import random
# Imports the random library, used for generating random numbers (not heavily used in this script).
import string
# Imports the string library, which provides useful string constants (like lowercase letters).

# Configuration file path
CONFIG_FILE = "ai_sites_config.json"
# Defines a constant variable for the name of the JSON file that stores AI site configurations.

# Default configuration
DEFAULT_CONFIG = {
    "browser_profile": "Default",  # Default Brave profile
    "selected_user_data_dir_key": "default_apexnelbo",
    "browser_data_dirs": {
        "default_apexnelbo": "/home/apexnelbo/.config/BraveSoftware/Brave-Browser"
    },
    "ai_sites": {
        "1": {
            "name": "Kimi AI",
            "url": "https://kimi.ai/",
            "initial_xpath": "//*[@id='app']/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div[1]",
            "subsequent_xpath": "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div/div[1]"
        }
    }
}
# Defines a dictionary containing the default configuration, including browser profile, selected data dir key, data dirs, and AI sites.

def load_config():
    """Load AI site configurations from file or create with defaults if not exists"""
    if os.path.exists(CONFIG_FILE):
        # Checks if the configuration file exists.
        try:
            with open(CONFIG_FILE, 'r') as f:
                # Opens the configuration file in read mode ('r').
                config = json.load(f)
                # Loads the JSON data from the file.
                # Ensure necessary keys exist (for backward compatibility)
                if 'ai_sites' not in config:
                    config['ai_sites'] = {}
                if 'browser_profile' not in config:
                    config['browser_profile'] = "Default"
                if 'browser_data_dirs' not in config:
                    config['browser_data_dirs'] = {"default_apexnelbo": "/home/apexnelbo/.config/BraveSoftware/Brave-Browser"}
                if 'selected_user_data_dir_key' not in config:
                    config['selected_user_data_dir_key'] = "default_apexnelbo"
                return config
                # Returns the loaded configuration.
        except json.JSONDecodeError:
            # Handles the case where the configuration file exists but is not valid JSON.
            print(f"Error reading config file. Using default configuration.")
            return DEFAULT_CONFIG
            # Returns the default configuration if there's an error reading the file.
    else:
        # Executes if the configuration file does not exist.
        print(f"Config file not found. Creating '{CONFIG_FILE}' with default settings.")
        with open(CONFIG_FILE, 'w') as f:
            # Opens a new file with the name defined by CONFIG_FILE in write mode ('w').
            json.dump(DEFAULT_CONFIG, f, indent=4)
            # Writes the default configuration to the new file in JSON format with indentation.
        return DEFAULT_CONFIG
        # Returns the default configuration that was just saved.

def save_config(config):
    """Save AI site configurations to file"""
    with open(CONFIG_FILE, 'w') as f:
        # Opens the configuration file in write mode ('w'). This will overwrite the existing file.
        json.dump(config, f, indent=4)
        # Writes the provided 'config' dictionary to the file in JSON format with indentation.

def configure_browser_profile(config):
    """Configure the default browser profile to use"""
    print("\nConfigure Browser Profile:")
    current_profile = config.get('browser_profile', 'Default')
    print(f"Current browser profile: {current_profile}")
    new_profile = input("Enter the name of your browser profile (e.g., Default, Profile 1): ").strip()
    if new_profile:
        config['browser_profile'] = new_profile
        save_config(config)
        print(f"Browser profile updated to: {new_profile}")
    else:
        print("Browser profile configuration unchanged.")
    return config

def configure_browser_data_dir(config):
    """Configure the browser user data directories"""
    print("\nConfigure Browser Data Directories:")
    browser_data_dirs = config.get('browser_data_dirs', {})

    while True:
        print("\nAvailable Browser Data Directories:")
        if not browser_data_dirs:
            print("No data directories configured yet.")
        else:
            for key, path in browser_data_dirs.items():
                print(f"{key}: {path}")

        print("\nOptions: add | edit | delete | back")
        action = input("Choose an action: ").strip().lower()

        if action == 'add':
            name = input("Enter a name for this data directory (e.g., chrome_user1): ").strip()
            if name and name not in browser_data_dirs:
                path = input("Enter the full path to your browser's user data directory (e.g., /home/user/snap/chromium/common/.config/chromium): ").strip()
                if path:
                    browser_data_dirs[name] = path
                    config['browser_data_dirs'] = browser_data_dirs
                    save_config(config)
                    print(f"Added '{name}' with path '{path}'.")
                else:
                    print("Path cannot be empty.")
            elif not name:
                print("Name cannot be empty.")
            else:
                print(f"Name '{name}' already exists.")
        elif action == 'edit':
            name_to_edit = input("Enter the name of the data directory to edit: ").strip()
            if name_to_edit in browser_data_dirs:
                new_path = input(f"Enter the new path for '{name_to_edit}' (leave blank to keep current): ").strip()
                if new_path:
                    browser_data_dirs[name_to_edit] = new_path
                    config['browser_data_dirs'] = browser_data_dirs
                    save_config(config)
                    print(f"Updated path for '{name_to_edit}'.")
            else:
                print(f"Data directory '{name_to_edit}' not found.")
        elif action == 'delete':
            name_to_delete = input("Enter the name of the data directory to delete: ").strip()
            if name_to_delete in browser_data_dirs:
                if name_to_delete == 'default_apexnelbo':
                    print("Cannot delete the default apexnelbo entry.")
                else:
                    confirm = input(f"Are you sure you want to delete '{name_to_delete}'? (y/n): ").strip().lower()
                    if confirm == 'y':
                        del browser_data_dirs[name_to_delete]
                        config['browser_data_dirs'] = browser_data_dirs
                        save_config(config)
                        print(f"Deleted '{name_to_delete}'.")
            else:
                print(f"Data directory '{name_to_delete}' not found.")
        elif action == 'back':
            break
        else:
            print("Invalid action.")
    return config

def select_browser_data_dir(config):
    """Select the browser user data directory to use"""
    print("\nSelect Browser Data Directory:")
    browser_data_dirs = config.get('browser_data_dirs', {})
    selected_key = config.get('selected_user_data_dir_key', 'default_apexnelbo')

    print("Available Browser Data Directories:")
    if not browser_data_dirs:
        print("No data directories configured. Using default.")
        return config
    else:
        for key, path in browser_data_dirs.items():
            print(f"{'*' if key == selected_key else ' '} {key}: {path}")

    new_selection = input("\nEnter the name of the data directory to use (leave blank to keep current): ").strip()
    if new_selection and new_selection in browser_data_dirs:
        config['selected_user_data_dir_key'] = new_selection
        save_config(config)
        print(f"Selected browser data directory: {new_selection}")
    elif new_selection:
        print("Invalid selection.")
    else:
        print("Keeping current selection.")
    return config


def select_ai(config):
    """Display and select from available AI sites"""
    ai_sites = config.get('ai_sites', {})
    print("\nChoose your AI destination:")
    for key, site in ai_sites.items():
        print(f"{key}: {site['name']} ({site['url']})")
    print("\nOptions:")
    print("add: Add a new AI site")
    print("manage: Edit/remove AI sites")
    print("config_profile: Configure Browser Profile")
    print("config_datadir: Configure Browser Data Directories")
    print("select_datadir: Select Browser Data Directory")
    print("exit: Close the program")

    while True:
        choice = input("\nSelect AI by number or option: ").strip()
        if choice.lower() == 'add':
            return 'add'
        elif choice.lower() == 'manage':
            return 'manage'
        elif choice.lower() == 'config_profile':
            return 'config_profile'
        elif choice.lower() == 'config_datadir':
            return 'config_datadir'
        elif choice.lower() == 'select_datadir':
            return 'select_datadir'
        elif choice.lower() == 'exit':
            return 'exit'
        elif choice in ai_sites:
            return choice
        else:
            print("Invalid choice. Try again.")

def add_new_ai(ai_sites):
    """Add a new AI site to the configuration"""
    next_id = str(max([int(k) for k in ai_sites.keys()]) + 1) if ai_sites else "1"

    name = input("Enter AI name: ").strip()
    url = input("Enter AI URL (include https://): ").strip()
    initial_xpath = input("Enter initial XPath for input field: ").strip()
    subsequent_xpath = input("Enter subsequent XPath for input field: ").strip()

    ai_sites[next_id] = {
        "name": name,
        "url": url,
        "initial_xpath": initial_xpath,
        "subsequent_xpath": subsequent_xpath
    }

    return ai_sites

def manage_ai_sites(ai_sites):
    """Manage (edit/remove) existing AI sites"""
    while True:
        print("\nManage AI Sites:")
        if not ai_sites:
            print("No sites configured yet.")
            input("Press Enter to return...")
            return ai_sites

        for key, site in ai_sites.items():
            print(f"{key}: {site['name']} ({site['url']})")

        choice = input("\nSelect site number to manage (or type 'back' to return): ").strip()

        if choice.lower() == 'back':
            return ai_sites
        elif choice in ai_sites:
            action = input(f"Manage '{ai_sites[choice]['name']}'. Choose action (edit/remove): ").strip().lower()

            if action == 'remove':
                confirm = input(f"Are you sure you want to remove {ai_sites[choice]['name']}? (y/n): ").strip().lower()
                if confirm == 'y':
                    del ai_sites[choice]
                    # Re-index if necessary to keep IDs sequential (optional but cleaner)
                    new_ai_sites = {}
                    for i, (old_key, site_data) in enumerate(ai_sites.items()):
                        new_ai_sites[str(i + 1)] = site_data
                    ai_sites = new_ai_sites
                    print("Site removed successfully.")
            elif action == 'edit':
                print(f"Editing {ai_sites[choice]['name']} - press Enter to keep current values")

                name = input(f"Name [{ai_sites[choice]['name']}]: ").strip()
                if name:
                    ai_sites[choice]['name'] = name

                url = input(f"URL [{ai_sites[choice]['url']}]: ").strip()
                if url:
                    ai_sites[choice]['url'] = url

                # Be careful editing XPaths - display current for reference
                print(f"Current Initial XPath: {ai_sites[choice]['initial_xpath']}")
                initial_xpath = input("New Initial XPath (leave blank to keep): ").strip()
                if initial_xpath:
                    ai_sites[choice]['initial_xpath'] = initial_xpath

                print(f"Current Subsequent XPath: {ai_sites[choice]['subsequent_xpath']}")
                subsequent_xpath = input("New Subsequent XPath (leave blank to keep): ").strip()
                if subsequent_xpath:
                    ai_sites[choice]['subsequent_xpath'] = subsequent_xpath

                print("Note: Browser profile and data directory are configured globally via the main menu options.")

            else:
                print("Invalid action. Please choose 'edit' or 'remove'.")
        else:
            print("Invalid site number.")
    return ai_sites

def generate_random_string(length=8):
    """Generate a random string (kept in case needed elsewhere)"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# --- MODIFIED open_in_browser ---
def open_in_browser(url, browser_profile="Default", user_data_dir=None):
    """Open the selected AI site in Brave browser using the specified profile
       and user data directory while attempting to keep the terminal in focus."""
    # ---vvv IMPORTANT: Verify these paths are correct for YOUR system vvv---
    default_user_data_dir = "/home/apexnelbo/.config/BraveSoftware/Brave-Browser"
    user_data_dir_to_use = user_data_dir if user_data_dir else default_user_data_dir
    profile_dir = browser_profile # Use the provided browser profile
    brave_path = "/usr/bin/brave-browser"
    chromedriver_path = "/usr/local/bin/chromedriver"
    # ---^^^ IMPORTANT: Verify these paths are correct for YOUR system ^^^---

    options = Options()
    options.binary_location = brave_path

    # --- Point Selenium to your existing profile ---
    options.add_argument(f"--user-data-dir={user_data_dir_to_use}")
    options.add_argument(f"--profile-directory={profile_dir}")
    # --- ---

    # Keep other useful options
    # options.add_argument("--start-maximized") # Can sometimes interfere with positioning, enable if needed
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    # --- Keep the window position arguments to try and keep terminal focus ---
    options.add_argument("--window-position=2000,2000")  # Position window off-screen initially
    # --- ---

    service = Service(executable_path=chromedriver_path)
    print(f"\nLaunching browser with profile '{profile_dir}' using data directory '{user_data_dir_to_use}' to {url}")

    # Add a try-except block for potential profile locking issues
    driver = None
    try:
        # Detach option can sometimes help if the script ends but you want the browser open
        # options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)  # Add this line to navigate to the URL
    except WebDriverException as e:
        print(f"Error launching WebDriver: {e}")
        print("-------------------------------------------------------------")
        print("Potential Causes & Solutions:")
        print("1. Brave browser might already be running and locking the profile.")
        print("   => Close ALL Brave windows/processes manually and try again.")
        print("2. ChromeDriver version might not match your Brave version.")
        print(f"   => Check Brave version (brave://version) and update ChromeDriver from https://chromedriver.chromium.org/downloads")
        print(f"3. Profile path incorrect? User Data Dir: '{user_data_dir_to_use}', Profile: '{profile_dir}'")
        print("   => Verify these paths exist and '{profile_dir}' is the correct folder name for your desired profile.")
        print(f"4. Chromedriver path incorrect or not executable? Path: '{chromedriver_path}'")
        print("   => Run 'ls -l /usr/local/bin/chromedriver' and 'chmod +x /usr/local/bin/chromedriver' if needed.")
        print("-------------------------------------------------------------")
        return None # Indicate failure to launch
    except Exception as e:
        print(f"An unexpected error occurred during browser launch: {e}")
        return None

    # Wait for the page to load and browser to initialize (might need slightly longer for existing profiles)
    time.sleep(3) # Adjusted sleep time

    # --- Move window to visible area but not necessarily front-center ---
    try:
        # Check if the window handle is still valid before trying to move/resize
        if driver.window_handles:
            driver.set_window_position(100, 100)
            driver.set_window_size(1200, 800)
            print("Browser launched. Terminal should remain in focus.")
            print("If browser took focus, click back on this terminal window to continue.")
        else:
            print("Warning: Browser window handle not found after launch. Browser might have closed.")
            if driver:
                driver.quit()
            return None # Indicates failure
    except WebDriverException as e:
        # Handle cases where the browser might close unexpectedly during setup
        print(f"Warning: Could not reposition/resize browser window: {e}")
        print("The browser might have closed or failed to initialize correctly.")
        # Attempt to quit cleanly if driver exists
        if driver:
            try:
                driver.quit()
            except Exception:
                pass # Ignore errors during cleanup quit
        return None
    except Exception as e:
        print(f"An unexpected error occurred during window repositioning: {e}")
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        return None

    return driver # Returns the webdriver instance
# --- END MODIFIED open_in_browser ---

# Added 'wait' as a parameter
def send_to_ai(driver, mode, initial_xpath, subsequent_xpath, is_initial, wait):
    """Send clipboard content with additional user input to AI chat interface"""
    # Removed wait initialization from here
    # wait = WebDriverWait(driver, 30) # 30 second wait time
    try:
        xpath_to_use = initial_xpath if is_initial else subsequent_xpath
        print(f"Attempting to find input element using XPath: {xpath_to_use}")

        if mode == "1":  # Text mode
            print("\nPlease copy the text you want to send to the clipboard.")
            input("Press Enter after copying the text...")
            clipboard_text = pyperclip.paste()
            if not clipboard_text:
                print("Warning: Clipboard is empty.")
                # Optionally ask user if they want to continue or retry
                # return False # Or proceed cautiously

            # Store the original clipboard content
            original_clipboard_text = clipboard_text

            print("\nClipboard content detected:")
            print("------------------------")
            print(clipboard_text if clipboard_text else "[Clipboard was empty]")
            print("------------------------")

            additional_text = input("\nType your question or additional context (press Enter when done, leave blank if none):\n").strip()

            final_text = original_clipboard_text  # Use the original content here
            if additional_text:
                # Add separators for clarity when combining
                final_text = f"{original_clipboard_text}\n\n---\n\n{additional_text}"

            # Update clipboard ONLY if additional text was added, to avoid pasting just the prompt
            if additional_text:
                pyperclip.copy(final_text)
                print("\nSending combined text (original clipboard + your input) to AI...")
            elif original_clipboard_text: # Use the original here as well
                print("\nSending original clipboard text to AI...")
            else:
                print("\nNothing to send (Clipboard was empty and no additional text provided).")
                return False # Nothing to send, return False for continue

            # --- Common Paste Logic for Text Mode ---
            # Use the 'wait' object passed as a parameter
            search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_to_use)))
            # It's often better to clear the field first, though some sites might not need it
            # search_bar.clear() # Uncomment if needed, test carefully
            search_bar.click() # Ensure focus
            time.sleep(0.2) # Small delay can help

            # Paste content from clipboard (which now contains final_text or original clipboard_text)
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(0.3) # Give paste time to register
            input("Press Enter to send the text...")
            actions.send_keys(Keys.RETURN).perform()
            print("Content sent.")
            # --- End Common Paste Logic ---

            # Ask if the user wants to continue the conversation
            while True:
                continue_choice = input("Continue conversation? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    return True # Indicate continue
                elif continue_choice in ['n', 'no']:
                    return False # Indicate return to menu
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

        elif mode == "2":  # Screenshot mode - Modified to paste after text
            print("\nPlease copy the screenshot you want to send to the clipboard.")
            input("Press Enter after copying the screenshot...")
            additional_text = input("\nType your question or additional context (press Enter when done, leave blank if none):\n").strip()

            print("\nLocating input field...")
            xpath_for_input = initial_xpath if is_initial else subsequent_xpath
            # Use the 'wait' object passed as a parameter
            search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_for_input)))
            search_bar.click()
            time.sleep(0.2)

            if additional_text:
                print("Typing your text...")
                search_bar.send_keys(additional_text)
                time.sleep(0.5)

            print("Pasting screenshot after text...")
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(5)  # Wait for paste/upload

            input("Press Enter to send the screenshot (and optional text)...")
            actions.send_keys(Keys.RETURN).perform()
            print("Content sent.")

            # Ask if the user wants to continue the conversation
            while True:
                continue_choice = input("Continue conversation? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    return True # Indicate continue
                elif continue_choice in ['n', 'no']:
                    return False # Indicate return to menu
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")


        else:
            print("Invalid mode selected in send_to_ai function.")
            return False # Indicate no continuation for invalid mode

    except TimeoutException as e:
        print(f"Timeout Exception: {e}")
        print(f"Error: Timed out waiting for an element (XPath: {xpath_to_use}).")
        print("The page might not have loaded correctly, the XPath might be wrong, or the element is not visible.")
        return False # Indicate no continuation on error
    except WebDriverException as e:
        print(f"WebDriver Exception: {e}")
        print("The browser window might have been closed or become unresponsive.")
        return False # Indicate no continuation on error
    except Exception as e:
        print(f"An unexpected error occurred in send_to_ai: {e}")
        return False # Indicate no continuation on error

# --- MODIFIED main ---
def main():
    config = load_config()
    driver = None # Initialize driver to None

    while True: # Starts the main program loop (AI selection menu)
        # If returning from a browser session, ensure driver is quit
        if driver:
            try:
                print("Cleaning up previous browser session...")
                driver.quit()
            except Exception as e:
                print(f"Note: Error quitting previous driver session: {e}")
            finally:
                driver = None # Reset driver

        choice = select_ai(config)

        if choice == 'add':
            config['ai_sites'] = add_new_ai(config.get('ai_sites', {}))
            save_config(config) # Save after adding
            continue # Go back to selection
        elif choice == 'manage':
            config['ai_sites'] = manage_ai_sites(config.get('ai_sites', {}))
            save_config(config) # Save after managing
            continue # Go back to selection
        elif choice == 'config_profile':
            config = configure_browser_profile(config)
            continue # Go back to selection
        elif choice == 'config_datadir':
            config = configure_browser_data_dir(config)
            continue # Go back to selection
        elif choice == 'select_datadir':
            config = select_browser_data_dir(config)
            continue # Go back to selection
        elif choice == 'exit': # Handle the new exit option
            print("\nExiting program...")
            return # Exit the main function, which will end the program

        # --- Open selected AI in browser ---
        site = config['ai_sites'][choice]
        browser_profile = config.get('browser_profile', 'Default') # Get global profile
        selected_data_dir_key = config.get('selected_user_data_dir_key', 'default_apexnelbo')
        user_data_dir = config.get('browser_data_dirs', {}).get(selected_data_dir_key)
        driver = open_in_browser(site['url'], browser_profile, user_data_dir)

        # --- Check if driver launched successfully ---
        if driver is None:
            print("\nFailed to launch the browser. Please check error messages above.")
            input("Press Enter to return to AI selection...")
            continue # Go back to the start of the loop (AI selection)
        # --- End check ---

        # Initialize WebDriverWait after driver is successfully launched
        wait = WebDriverWait(driver, 30) # Initialize wait here

        is_initial = True # Use initial XPath for the first interaction in this browser session

        # --- Main interaction loop for the selected AI ---
        while True: # Starts the loop for interacting with the selected AI
            print("\n-------------------------------------")
            print(f"Interacting with: {site['name']}")
            print("-------------------------------------")
            try:
                # Prompt for the initial message type (text or screenshot) or return/exit
                mode = input("\nChoose input method:\n"
                             "1: Send clipboard text (+ optional prompt)\n"
                             "2: Send clipboard screenshot (+ optional prompt)\n"
                             "3: Return to AI selection\n"
                             "4: Exit\n"
                             "Choice (1/2/3/4): ").strip()

                if mode not in ["1", "2", "3", "4"]:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")
                    continue

                # --- Handle user choice ---
                if mode == "3":
                    print("\nReturning to AI selection...")
                    # Cleanup happens at the start of the outer loop
                    break # Break inner loop to go back to AI selection

                elif mode == "4":
                    print("\nExiting program...")
                    if driver:
                        try:
                            driver.quit()
                        except Exception as e:
                            print(f"Note: Error quitting driver during exit: {e}")
                    return # Exit program completely

                else: # Mode 1 or 2
                    # --- Check if driver is still valid before sending ---
                    if not driver or not driver.window_handles:
                        print("\nError: Browser window seems to be closed or unresponsive.")
                        input("Press Enter to return to AI selection...")
                        break # Break inner loop

                    try:
                        # A quick check to see if interaction is possible
                        _ = driver.current_url
                    except WebDriverException as e:
                        print(f"\nError: Browser seems unresponsive ({e}).")
                        input("Press Enter to return to AI selection...")
                        break # Break inner loop
                    except Exception as e:
                         print(f"\nAn unexpected error occurred during browser check ({e}).")
                         input("Press Enter to return to AI selection...")
                         break # Break inner loop


                    # --- Send the initial message and check if user wants to continue ---
                    # Pass the wait object to send_to_ai
                    continue_conversation = send_to_ai(driver, mode, site['initial_xpath'], site['subsequent_xpath'], is_initial, wait)
                    is_initial = False # After the first message, subsequent messages will use the subsequent XPath

                    # --- Start Continue Conversation Loop if user chose to continue ---
                    if continue_conversation:
                        print("\nEntering continue conversation mode. Type your message and press Enter to send.")
                        print("Type 'menu' to return to the main AI selection.")

                        while True: # Loop for continuous text input
                            try: # Inner try block for continue mode messages
                                next_message = input(">> ").strip()

                                if next_message.lower() == 'menu':
                                    print("Returning to AI selection...")
                                    break # Exit the continue conversation loop

                                elif not next_message:
                                     print("Empty message. Type 'menu' to exit continue mode.")
                                     continue # Skip sending if the message is empty

                                # Locate and send the next message using the subsequent XPath
                                # Use the subsequent XPath for all messages within the continue mode
                                xpath_for_continue = site['subsequent_xpath']
                                print(f"Attempting to find input element using XPath: {xpath_for_continue}")

                                # Use the 'wait' object from the main function
                                search_bar_continue = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_for_continue)))
                                search_bar_continue.click() # Ensure focus
                                time.sleep(0.2) # Small delay
                                search_bar_continue.send_keys(next_message)
                                time.sleep(0.3) # Small delay

                                actions = ActionChains(driver)
                                # No need for manual Enter here as the user already pressed Enter after typing
                                actions.send_keys(Keys.RETURN).perform()
                                print("Message sent.")

                            except TimeoutException:
                                print(f"Error: Timed out waiting for the input element (XPath: {xpath_for_continue}) in continue mode.")
                                print("Returning to AI selection.")
                                break # Exit the continue conversation loop
                            except WebDriverException as e:
                                print(f"Error interacting with the browser in continue mode: {e}")
                                print("Returning to AI selection.")
                                break # Exit the continue conversation loop
                            except EOFError:
                                print("\nInput interrupted in continue mode. Returning to AI selection.")
                                break # Exit the continue conversation loop
                            except Exception as e:
                                print(f"An unexpected error occurred in continue mode: {e}")
                                print("Returning to AI selection.")
                                break # Exit the continue conversation loop
                # If continue_conversation was False (user chose not to continue) or the continue loop broke,
                # execution continues here, still within the OUTER try block.

            # These except clauses are for the OUTER try block that started before the mode input.
            except TimeoutException as e:
                print(f"Timeout Exception: {e}")
                print(f"Error: Timed out during interaction. Returning to AI selection.")
                break # Break the outer interaction loop
            except WebDriverException as e:
                print(f"WebDriver Exception: {e}")
                print("The browser window might have been closed or become unresponsive. Returning to AI selection.")
                break # Break the outer interaction loop
            except EOFError:
                 print("\nInput interrupted. Returning to AI selection.")
                 break # Break the outer interaction loop
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Returning to AI selection.")
                break # Break the outer interaction loop

        # If the inner interaction loop breaks, the outer loop continues, returning to AI selection.
        # The driver is quit at the beginning of the outer loop if it exists.


if __name__ == "__main__":
    print("Starting AI Interaction Script...")
    # Optional: Check Selenium version
    print(f"Using Selenium version: {selenium.__version__}")
    main()
    print("\nScript finished.")
