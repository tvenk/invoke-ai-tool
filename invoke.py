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
                # Ensure necessary keys exist
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
    # Prints a header for the AI site selection menu.
    for key, site in ai_sites.items():
        # Iterates through the key-value pairs in the 'ai_sites' dictionary.
        print(f"{key}: {site['name']} ({site['url']})")
        # Prints each AI site's number, name, and URL.
    print("\nOptions:")
    # Prints a header for the available options.
    print("add: Add a new AI site")
    # Prints the 'add' option.
    print("manage: Edit/remove AI sites")
    # Prints the 'manage' option.
    print("config_profile: Configure Browser Profile") # Option to configure browser profile
    print("config_datadir: Configure Browser Data Directories") # Option to configure browser data dirs
    print("select_datadir: Select Browser Data Directory") # Option to select browser data dir
    print("exit: Close the program")
    # Prints the 'exit' option.

    while True:
        # Starts an infinite loop to keep prompting the user for input until a valid choice is made.
        choice = input("\nSelect AI by number or option: ").strip()
        # Prompts the user to enter their choice and removes any leading or trailing whitespace.
        if choice.lower() == 'add':
            # Checks if the user entered 'add' (case-insensitive).
            return 'add'
            # Returns the string 'add' to indicate the user wants to add a new site.
        elif choice.lower() == 'manage':
            # Checks if the user entered 'manage' (case-insensitive).
            return 'manage'
            # Returns the string 'manage' to indicate the user wants to manage existing sites.
        elif choice.lower() == 'config_profile':
            # Checks if the user entered 'config_profile'.
            return 'config_profile'
        elif choice.lower() == 'config_datadir':
            # Checks if the user entered 'config_datadir'.
            return 'config_datadir'
        elif choice.lower() == 'select_datadir':
            # Checks if the user entered 'select_datadir'.
            return 'select_datadir'
        elif choice.lower() == 'exit':
            # Checks if the user entered 'exit' (case-insensitive).
            return 'exit'
            # Returns the string 'exit' to indicate the user wants to exit the program.
        elif choice in ai_sites:
            # Checks if the user's input is a valid key in the 'ai_sites' dictionary.
            return choice
            # Returns the user's choice (the number of the selected AI site).
        else:
            # Executes if the user's input is not one of the valid options.
            print("Invalid choice. Try again.")
            # Prints an error message and the loop continues to prompt for input.

def add_new_ai(ai_sites):
    """Add a new AI site to the configuration"""
    next_id = str(max([int(k) for k in ai_sites.keys()]) + 1) if ai_sites else "1"
    # Determines the next available ID for a new AI site. If there are existing sites, it finds the maximum ID and increments it. Otherwise, it starts with "1".

    name = input("Enter AI name: ").strip()
    # Prompts the user to enter the name of the new AI site and removes whitespace.
    url = input("Enter AI URL (include https://): ").strip()
    # Prompts the user to enter the URL of the new AI site and removes whitespace.
    initial_xpath = input("Enter initial XPath for input field: ").strip()
    # Prompts the user to enter the XPath for the initial input field and removes whitespace.
    subsequent_xpath = input("Enter subsequent XPath for input field: ").strip()
    # Prompts the user to enter the XPath for subsequent input fields and removes whitespace.

    ai_sites[next_id] = {
        "name": name,
        "url": url,
        "initial_xpath": initial_xpath,
        "subsequent_xpath": subsequent_xpath
    }
    # Creates a new entry in the 'ai_sites' dictionary with the generated ID and the provided details.

    return ai_sites
    # Returns the updated 'ai_sites' dictionary (saving happens in main).

def manage_ai_sites(ai_sites):
    """Manage (edit/remove) existing AI sites"""
    while True:
        # Starts an infinite loop to allow for multiple management actions.
        print("\nManage AI Sites:")
        # Prints a header for the management menu.
        if not ai_sites:
            # Checks if the 'ai_sites' dictionary is empty (no sites configured).
            print("No sites configured yet.")
            input("Press Enter to return...")
            return ai_sites
            # If no sites are configured, informs the user and returns to the main menu.

        for key, site in ai_sites.items():
            # Iterates through the configured AI sites.
            print(f"{key}: {site['name']} ({site['url']})")
            # Prints the number, name, and URL of each configured site.

        choice = input("\nSelect site number to manage (or type 'back' to return): ").strip()
        # Prompts the user to select a site to manage or type 'back'.

        if choice.lower() == 'back':
            # Checks if the user wants to go back to the main menu.
            return ai_sites
            # Returns the current 'ai_sites' dictionary.
        elif choice in ai_sites:
            # Checks if the user's input is a valid key in the 'ai_sites' dictionary.
            action = input(f"Manage '{ai_sites[choice]['name']}'. Choose action (edit/remove): ").strip().lower()
            # Prompts the user to choose between editing or removing the selected site.

            if action == 'remove':
                # Executes if the user wants to remove the site.
                confirm = input(f"Are you sure you want to remove {ai_sites[choice]['name']}? (y/n): ").strip().lower()
                # Asks for confirmation before removing.
                if confirm == 'y':
                    # Proceeds with removal if the user confirms.
                    del ai_sites[choice]
                    # Deletes the selected site from the dictionary.
                    # Re-index if necessary to keep IDs sequential (optional but cleaner)
                    new_ai_sites = {}
                    for i, (old_key, site_data) in enumerate(ai_sites.items()):
                        new_ai_sites[str(i + 1)] = site_data
                    ai_sites = new_ai_sites
                    print("Site removed successfully.")
            elif action == 'edit':
                # Executes if the user wants to edit the site.
                print(f"Editing {ai_sites[choice]['name']} - press Enter to keep current values")
                # Informs the user about editing and how to keep current values.

                name = input(f"Name [{ai_sites[choice]['name']}]: ").strip()
                # Prompts for a new name, showing the current name in brackets.
                if name:
                    ai_sites[choice]['name'] = name
                    # Updates the name if the user provides a new one.

                url = input(f"URL [{ai_sites[choice]['url']}]: ").strip()
                # Prompts for a new URL, showing the current URL.
                if url:
                    ai_sites[choice]['url'] = url
                    # Updates the URL if provided.

                # Be careful editing XPaths - display current for reference
                print(f"Current Initial XPath: {ai_sites[choice]['initial_xpath']}")
                initial_xpath = input("New Initial XPath (leave blank to keep): ").strip()
                # Prompts for a new initial XPath, showing the current one.
                if initial_xpath:
                    ai_sites[choice]['initial_xpath'] = initial_xpath
                    # Updates the initial XPath if provided.

                print(f"Current Subsequent XPath: {ai_sites[choice]['subsequent_xpath']}")
                subsequent_xpath = input("New Subsequent XPath (leave blank to keep): ").strip()
                # Prompts for a new subsequent XPath, showing the current one.
                if subsequent_xpath:
                    ai_sites[choice]['subsequent_xpath'] = subsequent_xpath
                    # Updates the subsequent XPath if provided.

                print("Note: Browser profile and data directory are configured globally via the main menu options.")

            else:
                # Executes if the user enters an invalid action.
                print("Invalid action. Please choose 'edit' or 'remove'.")
        else:
            # Executes if the user enters an invalid site number.
            print("Invalid site number.")
    return ai_sites

def generate_random_string(length=8):
    """Generate a random string (kept in case needed elsewhere)"""
    letters = string.ascii_lowercase
    # Defines a string containing all lowercase letters.
    return ''.join(random.choice(letters) for i in range(length))
    # Generates a random string of the specified length using the lowercase letters.

# --- MODIFIED open_in_browser ---
def open_in_browser(url, browser_profile="Default", user_data_dir=None):
    """Open the selected AI site in Brave browser using the specified profile
       and user data directory while attempting to keep the terminal in focus."""
    # ---vvv IMPORTANT: Verify these paths are correct for YOUR system vvv---
    default_user_data_dir = "/home/apexnelbo/.config/BraveSoftware/Brave-Browser"
    # Specifies the default path to the Brave Browser user data directory. **USER-SPECIFIC**
    user_data_dir_to_use = user_data_dir if user_data_dir else default_user_data_dir
    # Use the provided user_data_dir if available, otherwise use the default.
    profile_dir = browser_profile # Use the provided browser profile
    # Specifies the name of the Brave Browser profile directory to use. **USER-SPECIFIC**
    brave_path = "/usr/bin/brave-browser"
    # Specifies the path to the Brave Browser executable. **SYSTEM-SPECIFIC**
    chromedriver_path = "/usr/local/bin/chromedriver"
    # Specifies the path to the ChromeDriver executable. **SYSTEM-SPECIFIC**
    # ---^^^ IMPORTANT: Verify these paths are correct for YOUR system ^^^---

    options = Options()
    # Creates an instance of Chrome Options to configure the browser.
    options.binary_location = brave_path
    # Sets the binary location (executable path) for Brave Browser.

    # --- Point Selenium to your existing profile ---
    options.add_argument(f"--user-data-dir={user_data_dir_to_use}")
    # Adds an argument to Chrome Options to specify the user data directory.
    options.add_argument(f"--profile-directory={profile_dir}")
    # Adds an argument to Chrome Options to specify the profile directory to use.
    # --- ---

    # Keep other useful options
    # options.add_argument("--start-maximized") # Can sometimes interfere with positioning, enable if needed
    options.add_argument("--no-first-run")
    # Adds an argument to prevent Brave's first-run setup page from appearing.
    options.add_argument("--no-default-browser-check")
    # Adds an argument to disable the default browser check.

    # --- Keep the window position arguments to try and keep terminal focus ---
    options.add_argument("--window-position=2000,2000")  # Position window off-screen initially
    # Adds an argument to initially position the browser window off-screen.
    # --- ---

    service = Service(executable_path=chromedriver_path)
    # Creates a Service object for ChromeDriver, specifying its executable path.
    print(f"\nLaunching browser with profile '{profile_dir}' using data directory '{user_data_dir_to_use}' to {url}")
    # Prints a message indicating the browser launch details.

    # Add a try-except block for potential profile locking issues
    driver = None
    # Initializes the driver variable to None.
    try:
        # Detach option can sometimes help if the script ends but you want the browser open
        # options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, options=options)
        # Creates a new Chrome webdriver instance using the configured service and options.
        driver.get(url)  # Add this line to navigate to the URL
        # Navigates the browser to the specified URL.
    except WebDriverException as e:
        # Catches exceptions related to WebDriver (e.g., ChromeDriver issues, profile locking).
        print(f"Error launching WebDriver: {e}")
        # Prints the specific WebDriver exception error.
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
        # Returns None to indicate that the browser failed to launch.
    except Exception as e:
        # Catches any other unexpected exceptions during browser launch.
        print(f"An unexpected error occurred during browser launch: {e}")
        return None
        # Returns None to indicate launch failure.

    # Wait for the page to load and browser to initialize (might need slightly longer for existing profiles)
    time.sleep(3) # Adjusted sleep time
    # Pauses the script for 3 seconds to allow the page to load.

    # --- Move window to visible area but not necessarily front-center ---
    try:
        # Check if the window handle is still valid before trying to move/resize
        if driver.window_handles:
            # Checks if there are any active browser window handles.
            driver.set_window_position(100, 100)
            # Sets the position of the browser window to (100, 100) pixels.
            driver.set_window_size(1200, 800)
            # Sets the size of the browser window to 1200x800 pixels.
            print("Browser launched. Terminal should remain in focus.")
            print("If browser took focus, click back on this terminal window to continue.")
        else:
            # Executes if no browser window handles are found.
            print("Warning: Browser window handle not found after launch. Browser might have closed.")
            if driver:
                driver.quit()
                # Attempts to close the browser if the driver instance exists.
            return None # Indicates failure
            # Returns None to indicate failure.
    except WebDriverException as e:
        # Handles WebDriver exceptions that might occur during window manipulation.
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
        # Handles any other unexpected errors during window manipulation.
        print(f"An unexpected error occurred during window repositioning: {e}")
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        return None

    return driver # Returns the webdriver instance
    # Returns the WebDriver instance if the browser launched successfully.
# --- END MODIFIED open_in_browser ---

def send_to_ai(driver, mode, initial_xpath, subsequent_xpath, is_initial=True):
    """Send clipboard content with additional user input to AI chat interface"""
    wait = WebDriverWait(driver, 30) # 30 second wait time
    # Creates a WebDriverWait instance with a timeout of 30 seconds.
    try:
        xpath_to_use = initial_xpath if is_initial else subsequent_xpath
        # Determines which XPath to use based on whether it's the initial interaction.
        print(f"Attempting to find input element using XPath: {xpath_to_use}")
        # Prints the XPath being used to locate the input element.

        if mode == "1":  # Text mode
            print("\nPlease copy the text you want to send to the clipboard.")
            # Prompts the user to copy text to the clipboard.
            input("Press Enter after copying the text...")
            # Waits for the user to press Enter after copying.
            clipboard_text = pyperclip.paste()
            # Pastes the content of the clipboard into the 'clipboard_text' variable.
            if not clipboard_text:
                # Checks if the clipboard is empty.
                print("Warning: Clipboard is empty.")
                # Optionally ask user if they want to continue or retry
                # return # Or proceed cautiously

            # Store the original clipboard content
            original_clipboard_text = clipboard_text
            # Stores the initial clipboard content in a separate variable.

            print("\nClipboard content detected:")
            print("------------------------")
            print(clipboard_text if clipboard_text else "[Clipboard was empty]")
            print("------------------------")

            additional_text = input("\nType your question or additional context (press Enter when done, leave blank if none):\n").strip()
            # Prompts the user for additional text or a question.

            final_text = original_clipboard_text  # Use the original content here
            # Initializes 'final_text' with the original clipboard content.
            if additional_text:
                # Checks if the user provided any additional text.
                # Add separators for clarity when combining
                final_text = f"{original_clipboard_text}\n\n---\n\n{additional_text}"
                # Combines the original clipboard text and the additional text with separators.

            # Update clipboard ONLY if additional text was added, to avoid pasting just the prompt
            if additional_text:
                pyperclip.copy(final_text)
                # Copies the combined text to the clipboard.
                print("\nSending combined text (original clipboard + your input) to AI...")
            elif original_clipboard_text: # Use the original here as well
                # Checks if there was original clipboard text (even if no additional text).
                print("\nSending original clipboard text to AI...")
            else:
                print("\nNothing to send (Clipboard was empty and no additional text provided).")
                return # Nothing to send

            # --- Common Paste Logic for Text Mode ---
            search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_to_use)))
            # Waits until the input element is visible on the page.
            # It's often better to clear the field first, though some sites might not need it
            # search_bar.clear() # Uncomment if needed, test carefully
            search_bar.click() # Clicks on the input field to ensure focus
            time.sleep(0.2) # Small delay can help

            # Paste content from clipboard (which now contains final_text or original clipboard_text)
            actions = ActionChains(driver)
            # Creates an ActionChains object to perform a sequence of actions.
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            # Simulates pressing Ctrl+V (paste).
            time.sleep(0.3) # Give paste time to register
            input("Press Enter to send the text...")
            # Waits for the user to press Enter to send the content.
            actions.send_keys(Keys.RETURN).perform()
            # Simulates pressing the ENTER key to send the message.
            print("Content sent.")
            # Prints a confirmation message.
            # --- End Common Paste Logic ---

        elif mode == "2":  # Screenshot mode - Modified to paste after text
            print("\nPlease copy the screenshot you want to send to the clipboard.")
            input("Press Enter after copying the screenshot...")
            additional_text = input("\nType your question or additional context (press Enter when done, leave blank if none):\n").strip()

            print("\nLocating input field...")
            xpath_for_input = initial_xpath if is_initial else subsequent_xpath
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

        else:
            print("Invalid mode selected in send_to_ai function.")
            return

    except TimeoutException as e:
        print(f"Timeout Exception: {e}")
        print(f"Error: Timed out waiting for an element (XPath: {xpath_to_use}).")
        print("The page might not have loaded correctly, the XPath might be wrong, or the element is not visible.")
    except WebDriverException as e:
        print(f"WebDriver Exception: {e}")
        print("The browser window might have been closed or become unresponsive.")
    except Exception as e:
        print(f"An unexpected error occurred in send_to_ai: {e}")

# --- MODIFIED main ---
def main():
    config = load_config()
    # Loads the AI site configurations.
    driver = None # Initialize driver to None
    # Initializes the 'driver' variable to None at the start of the main function.

    while True:
        # Starts the main program loop.
        # If returning from a browser session, ensure driver is quit
        if driver:
            # Checks if a WebDriver instance exists (meaning a browser session was active).
            try:
                print("Cleaning up previous browser session...")
                driver.quit()
                # Closes the browser window and ends the WebDriver session.
            except Exception as e:
                print(f"Note: Error quitting previous driver session: {e}")
            finally:
                driver = None # Reset driver
                # Ensures the 'driver' variable is reset to None, regardless of whether quitting was successful.

        choice = select_ai(config)
        # Displays the AI selection menu and gets the user's choice.

        if choice == 'add':
            # Checks if the user wants to add a new AI site.
            config['ai_sites'] = add_new_ai(config.get('ai_sites', {}))
            # Calls the function to add a new AI site and updates the 'ai_sites' dictionary in the config.
            save_config(config) # Save after adding
            continue # Go back to selection
            # Skips to the next iteration of the main loop to show the updated selection menu.
        elif choice == 'manage':
            # Checks if the user wants to manage existing AI sites.
            config['ai_sites'] = manage_ai_sites(config.get('ai_sites', {}))
            # Calls the function to manage AI sites and updates the 'ai_sites' dictionary in the config.
            save_config(config) # Save after managing
            continue # Go back to selection
            # Skips to the next iteration of the main loop.
        elif choice == 'config_profile':
            # Checks if the user wants to configure the browser profile.
            config = configure_browser_profile(config)
            # Calls the function to configure the browser profile and updates the config.
            continue # Go back to selection
            # Skips to the next iteration of the main loop.
        elif choice == 'config_datadir':
            # Checks if the user wants to configure browser data directories.
            config = configure_browser_data_dir(config)
            # Calls the function to configure browser data directories and updates the config.
            continue # Go back to selection
        elif choice == 'select_datadir':
            # Checks if the user wants to select a browser data directory.
            config = select_browser_data_dir(config)
            # Calls the function to select a browser data directory and updates the config.
            continue # Go back to selection
        elif choice == 'exit':
            # Checks if the user wants to exit the program.
            print("\nExiting program...")
            return # Exit the main function, which will end the program

        # --- Open selected AI in browser ---
        site = config['ai_sites'][choice]
        # Retrieves the details of the selected AI site from the 'ai_sites' dictionary in the config.
        browser_profile = config.get('browser_profile', 'Default') # Get global profile
        # Retrieves the global browser profile from the config, defaulting to 'Default'.
        selected_data_dir_key = config.get('selected_user_data_dir_key', 'default_apexnelbo')
        user_data_dir = config.get('browser_data_dirs', {}).get(selected_data_dir_key)
        # Retrieves the user data directory path based on the selected key.
        driver = open_in_browser(site['url'], browser_profile, user_data_dir)
        # Calls the function to open the selected AI site in the browser, passing the URL, browser profile, and user data directory.

        # --- Check if driver launched successfully ---
        if driver is None:
            # Checks if the browser failed to launch (open_in_browser returns None on failure).
            print("\nFailed to launch the browser. Please check error messages above.")
            input("Press Enter to return to AI selection...") # Pause for user to read errors
            continue # Go back to the start of the loop (AI selection)
        # --- End check ---

        is_initial = True # Use initial XPath for the first interaction in this session
        # Sets a flag to indicate that the initial XPath should be used for the first interaction with the selected AI site.

        # --- Main interaction loop for the selected AI ---
        while True:
            # Starts an inner loop for interacting with the chosen AI site.
            print("\n-------------------------------------")
            print(f"Interacting with: {site['name']}")
            print("-------------------------------------")
            try:
                mode = input("\nChoose input method:\n"
                             "1: Send clipboard text (+ optional prompt)\n"
                             "2: Send clipboard screenshot (+ optional prompt)\n"
                             "3: Return to AI selection\n"
                             "4: Exit\n"
                             "Choice (1/2/3/4): ").strip()
                # Prompts the user to choose an input method.

                if mode not in ["1", "2", "3", "4"]:
                    # Checks if the user's input is one of the valid mode options.
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")
                    continue # Continues to the next iteration of the inner loop

            except ValueError:
                print(f"Invalid input. Please enter a number.")
                continue
            except EOFError: # Handle Ctrl+D or unexpected end of input
                print("\nInput interrupted. Exiting.")
                mode = "4" # Treat as exit

            # --- Handle user choice ---
            if mode == "3":
                # Checks if the user wants to return to the AI selection menu.
                print("\nReturning to AI selection...")
                # Cleanup happens at the start of the outer loop
                break # Break inner loop to go back to AI selection

            elif mode == "4":
                # Checks if the user wants to exit the program.
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
                    # Checks if the WebDriver instance is valid and if there are any open browser windows.
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

                # --- Send content ---
                send_to_ai(driver, mode, site['initial_xpath'], site['subsequent_xpath'], is_initial)
                # Calls the function to send content to the AI interface.
                is_initial = False # Use subsequent XPath for next interactions
                # Sets the flag to False after the first interaction, so subsequent interactions use the 'subsequent_xpath'.
        # --- End of inner interaction loop ---
    # --- End of outer main loop ---

if __name__ == "__main__":
    # This block ensures that the code inside it only runs when the script is executed directly (not when imported as a module).
    print("Starting AI Interaction Script...")
    # Prints a message indicating the script has started.
    # Optional: Check Selenium version
    print(f"Using Selenium version: {selenium.__version__}")
    # Prints the version of the Selenium library being used.
    main()
    # Calls the main function to start the program's execution.
    print("\nScript finished.")
    # Prints a message indicating that the script has finished.
