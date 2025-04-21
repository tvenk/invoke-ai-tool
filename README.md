# invoke-ai-tool
# AI Interaction Tool

This tool automates interactions with various AI websites using a web browser (specifically designed for Brave but can be adapted). It allows you to send text or screenshots from your clipboard to the AI chat interface.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Configuration](#configuration)
    * [Browser Profile](#browser-profile)
    * [Browser Data Directories](#browser-data-directories)
    * [AI Sites](#ai-sites)
* [Usage](#usage)
* [Finding Browser Data Directories on Ubuntu](#finding-browser-data-directories-on-ubuntu)
* [Contributing](#contributing)

## Prerequisites

Before using this tool, you need to have the following installed on your Ubuntu system:

* **Python 3:** If you don't have it, you can install it using:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    ```
* **Brave Browser:** The script is primarily designed to work with Brave Browser. You can download it from [https://brave.com/download/](https://brave.com/download/).
* **ChromeDriver:** This is a separate executable that Selenium uses to control Brave Browser. You need to download the ChromeDriver version that matches your Brave Browser version. You can check your Brave version by going to `brave://version` in your browser. Download ChromeDriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) and place the `chromedriver` executable in a directory that is in your system's PATH (e.g., `/usr/local/bin`). You might need to make it executable:
    ```bash
    sudo chmod +x /usr/local/bin/chromedriver
    ```
* **Python Libraries (if not installing via .deb):** If you choose to run the Python script directly, you will need these libraries. If you install via the `.deb` file, these dependencies should be handled automatically:
    ```bash
    pip3 install selenium pyperclip
    ```

## Installation

You have two options for installing this tool: running the Python script directly or installing the provided `.deb` package.

**Option 1: Running the Python Script Directly**

1.  **Download the Script:** You can download the `invoke.py` file from this GitHub repository.
2.  **Place the Script:** Save the `invoke.py` file to a directory on your computer.
3.  **Install Dependencies:** Make sure you have the necessary Python libraries installed as mentioned in the [Prerequisites](#prerequisites) section.
4.  **Use a Virtual Environment (Recommended):** It's highly recommended to use a Python virtual environment to manage dependencies for this tool separately from your system's Python installation.
    * **Create a Virtual Environment:** Navigate to the directory where you saved `invoke.py` and create a virtual environment (replace `myvenv` with your desired name):
        ```bash
        python3 -m venv myvenv
        ```
    * **Activate the Virtual Environment:** Activate the environment in your terminal before running the script:
        ```bash
        source myvenv/bin/activate
        ```
        Your terminal prompt should change to indicate the virtual environment is active (e.g., `(myvenv) your_username@your_computer:~/$`).

**Option 2: Installing via the `.deb` Package**

1.  **Download the `.deb` File:** Download the `invoke-ai-tool.deb` file from the releases section of this GitHub repository.
2.  **Install the `.deb` Package:** Open your terminal, navigate to the directory where you downloaded the `.deb` file, and run the following command:
    ```bash
    sudo dpkg -i invoke-ai-tool.deb
    ```
3.  **Fix Dependency Issues (if any):** If you encounter any dependency errors during the installation, you can try to resolve them by running:
    ```bash
    sudo apt --fix-broken install
    ```
4.  **Run the Installed Tool:** The tool will be installed and you can run it from your terminal using the command `invoke`. You will see output similar to this:
    ```
    **apexnelbo@ancient-HP-ENVY-TS-17-Notebook-PC:~$ invoke**
    Starting AI Interaction Script...
    Using Selenium version: 4.18.1 # (Version number may vary)

    Choose your AI destination:
    1: Kimi AI ([https://kimi.ai/](https://kimi.ai/)) # (Configured sites will appear here)

    Options:
    add: Add a new AI site
    manage: Edit/remove AI sites
    config_profile: Configure Browser Profile
    config_datadir: Configure Browser Data Directories
    select_datadir: Select Browser Data Directory
    exit: Close the program

    Select AI by number or option:
    ```

## Configuration

The tool uses a configuration file named `ai_sites_config.json` to store information about the AI websites you want to interact with and your browser settings. This file will be created automatically the first time you run the tool (either directly or via the installed `.deb` package). You can also manually configure it through the tool's menu.

### Browser Profile

The tool is designed to use a specific browser profile in Brave. By default, it's set to "Default". You can change this:

1.  **Run the tool from the terminal** (see the [Usage](#usage) section for instructions on how to run it).
2.  In the main menu, select `config_profile: Configure Browser Profile`.
3.  Enter the name of your desired Brave profile (e.g., `Default`, `Profile 1`).

### Browser Data Directories

This tool allows you to manage and select different Brave browser user data directories. This is useful if you have multiple separate Brave profiles with distinct settings and data.

1.  **Run the tool from the terminal**.
2.  In the main menu, you have the following options:
    * `config_datadir: Configure Browser Data Directories`: This allows you to add, edit, and delete browser data directory configurations.
        * **add:** Enter a name for the directory (e.g., `brave_work`) and then the full path to the directory.
        * **edit:** Enter the name of the directory you want to edit and then the new path (leave blank to keep the current path).
        * **delete:** Enter the name of the directory you want to delete (you cannot delete the `default_apexnelbo` entry).
        * **back:** Return to the main menu.
    * `select_datadir: Select Browser Data Directory`: This lets you choose which configured browser data directory to use for the current session. The currently selected directory is marked with an asterisk (`*`).

By default, the tool includes your specific Brave data directory (`/home/apexnelbo/.config/BraveSoftware/Brave-Browser`) with the name `default_apexnelbo`. You can add more for different profiles or even different Brave installations.

### AI Sites

You can add, edit, and remove the AI websites that the tool interacts with:

1.  **Run the tool from the terminal**.
2.  In the main menu:
    * To add a new AI site, select `add: Add a new AI site` and follow the prompts for the name, URL, and the XPath for the input field.
    * To manage existing sites, select `manage: Edit/remove AI sites`. You can then choose a site by number to edit (name, URL, XPaths) or remove.

The tool requires two XPath expressions for each AI site:
* **Initial XPath:** The XPath of the input field when you first load the AI website.
* **Subsequent XPath:** The XPath of the input field after you have sent a message (as the page structure might change).

You might need to inspect the AI website's HTML source code using your browser's developer tools to find these XPaths. Right-click on the input field and select "Inspect" or "Inspect Element". Then, you can usually right-click on the highlighted HTML and choose "Copy" -> "XPath".

## Usage

1.  **Open your terminal.**
2.  **Run the Tool:**
    * **If you installed by running the Python script directly:** Navigate to the directory where you saved `invoke.py`, activate your virtual environment, and run:
        ```bash
        # Activate your virtual environment (replace myvenv with your name)
        source myvenv/bin/activate
        # Run the script
        python3 invoke.py
        ```
    * **If you installed using the `.deb` package:** Simply run:
        ```bash
        invoke
        ```
3.  **Select an AI Destination:** The tool will display a numbered list of the AI sites you have configured. Enter the number corresponding to the AI you want to use and press Enter.
4.  **Select Browser Data Directory:** If you have configured multiple browser data directories, you will be prompted to select which one to use for this session. Enter the name of the desired directory.
5.  **The Browser Opens:** The script will attempt to open Brave Browser with your selected profile and navigate to the URL of the chosen AI site. The browser window will be positioned slightly off-screen initially to try and keep the terminal in focus. Click back on the terminal if the browser takes focus.
6.  **Interact with the AI:** Once the page has loaded, you will see the following options in the terminal:
    ```
    Choose input method:
    1: Send clipboard text (+ optional prompt)
    2: Send clipboard screenshot (+ optional prompt)
    3: Return to AI selection
    4: Exit
    Choice (1/2/3/4):
    ```
    * **1: Send clipboard text (+ optional prompt):**
        * Copy the text you want to send to the AI to your clipboard.
        * Press Enter in the terminal.
        * You will be prompted to type an optional question or additional context. Press Enter when done (leave blank if none).
        * The combined text (or just the clipboard content) will be pasted into the AI's input field.
        * Press Enter again in the terminal to send the message.
    * **2: Send clipboard screenshot (+ optional prompt):**
        * Copy a screenshot to your clipboard (you can usually do this with tools like `gnome-screenshot` and selecting "Copy to Clipboard").
        * Press Enter in the terminal.
        * You will be prompted to type an optional question or additional context. Press Enter when done (leave blank if none).
        * The script will attempt to paste the screenshot into the AI's input field. If you provided text, the text will be typed first, then the screenshot will be pasted. This might take a few seconds.
        * Press Enter again in the terminal to send the screenshot (and optional text).
    * **After sending the message (using option 1 or 2), you will be prompted whether you want to continue the conversation (y/n).**
    * **3: Return to AI selection:** This will close the current browser window (if it was opened by the script) and take you back to the main menu to choose a different AI site.
    * **4: Exit:** This will close the browser (if open) and terminate the script.
7.  **Subsequent Interactions:** After sending a message, the script will try to use the "subsequent XPath" for the input field for the next interaction.

## Finding Browser Data Directories on Ubuntu

Here's how to find the user data directory for common browsers on Ubuntu:

* **Brave Browser:** Typically located at `/home/[your_username]/.config/BraveSoftware/Brave-Browser/`. Replace `[your_username]` with your actual username.
* **Google Chrome:** Usually found at `/home/[your_username]/.config/google-chrome/`.
* **Chromium:** Typically located at `/home/[your_username]/.config/chromium/`.
* **Mozilla Firefox:** Firefox stores profile data differently. The main directory is usually `/home/[your_username]/.mozilla/firefox/`. Inside this, you'll find one or more folders with names like `xxxxxxxx.default-release`. For Firefox, you would likely configure the main Firefox directory in the tool and rely on the browser profile setting.

**Note:** For snap installations of browsers, the data directory might be in a different location, for example, under `/home/[your_username]/snap/[browser-name]/common/.config/[browser-name]/.`

## Contributing

If you'd like to contribute to this tool, feel free to fork the repository on GitHub, make your changes, and submit a pull request. Please credit tvenk thank you, best wishes!
