#!/usr/bin/env python3

'''
Kyle Timmermans
Wicked v5.0
v5.0 Released: March 18, 2024
Developed in Python 3.12.2
'''

# Base imports
import re
import sys
import json
import random
import pwinput
import requests
import threading
from time import sleep
from wakepy import keep
from tqdm import trange
from datetime import datetime
from colorama import Fore, init
from itertools import zip_longest, cycle

# Auto download & install chromedriver
from webdriver_manager.chrome import ChromeDriverManager

# Driving Chrome (Headless) with Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    ElementClickInterceptedException
)


def print_banner():
    print(green) # Make ASCII Art and Banner Green (figlet - 'epic' font)
    print("       .*.                                       ")
    print("     *' + '*      ,       ,                      ")
    print("      *'|'*       |`;`;`;`|                      ")
    print("        |         |:.'.'.'|                      ")
    print("        |         |:.:.:.:|                      ")
    print("        |         |::....:|                                                    _________ _______  _        _______  ______               _______ ")
    print("        |        /`   / ` \\                                           |\\     /|\\__   __/(  ____ \\| \\    /\\(  ____ \\(  __  \\    |\\     /|(  ____ \\")
    print("        |       (   .' ^ \\^)                                          | )   ( |   ) (   | (    \\/|  \\  / /| (    \\/| (  \\  )   | )   ( || (    \\/")
    print("        |_.,   (    \\    -/(            You're" + "                        | | _ | |   | |   | |      |  (_/ / | (__    | |   ) |   | |   | || (____  ")
    print("     ,~`|   `~./     )._=/  )  ,,            gonna"+ "                    | |( )| |   | |   | |      |   _ (  |  __)   | |   | |   ( (   ) )(_____ \\ ")
    print("    {   |     (       )|   (.~`  `~,             be"+ "                   | || || |   | |   | |      |  ( \\ \\ | (      | |   ) |    \\ \\_/ /       ) )")
    print("    {   |      \\   _.'  \\   )       }             pop-u-lar!"+"          | () () |___) (___| (____/\\|  /  \\ \\| (____/\\| (__/  )     \\   /  /\\____) )")
    print("    ;   |       ;`\\      `)-`       }     _.._   "+"                     (_______)\\_______/(_______/|_/    \\/(_______/(______/       \\_/   \\______/ ")
    print("     '.(\\,     ;   `\\    / `.       }__.-'__.-'")
    print("      ( (/-;~~`;     `\\_/    ;   .'`  _.-'      ")
    print("      `/|\\/   .'\\.    /o\\   ,`~~`~~~~`        ")
    print("       \\| ` .'   \\'--'   '-`                   ")
    print("        |--',==~~`)       (`~~==,_               ")
    print("        ,=~`      `-.     /       `~=,           ")
    print("     ,=`             `-._/            `=,      \n")
    print("Created by: @KyleTimmermans")
    print("ASCII Art by jgs\n")
    print("See who's not following you back and who you don't follow back on Instagram!")
    print("This may take some time depending on how many people you follow / follow you")
    print(f"{reset}\n")  # Reset text color


# Input instagram creds
def input_creds():
    username = input("Input your Instagram Username / Email / Phone #: ")
    # pwinput used to prevent shoulder surfing (allows masking)
    password = pwinput.pwinput(prompt="Input your password (Not Stored): ", mask='*')

    return [username, password]  # Return creds as list


def chromedriver_setup():
    # Chromedriver automatically downloaded w/ Selenium 4 & webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Get the user agent
    driver.get("https://www.instagram.com/")
    sleep(5)
    safe_user_agent = driver.execute_script("return navigator.userAgent;").replace("Headless", "")
    sleep(1)
    # Quit the first temp-run
    driver.quit()
    # Update our options with the safe user agent
    chrome_options.add_argument(f'user-agent={safe_user_agent}')
    # Driver re-initialized with safe user agent and headless
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver


def instagram_login(username, password):
    # Check if username / password is correct
    while True:
        try:
            print("\nEstablishing Connection with Instagram...\n")
            driver.get("https://www.instagram.com/accounts/login/")  # Login page
            sleep(7)
            try:  # Check internet connection
                driver.find_element(By.CSS_SELECTOR, "[aria-label='Phone number, username, or email']").send_keys(username)  # Send username
            except NoSuchElementException:
                print("\n"+red+"Error: "+reset+ "No Internet Connection!")
                driver.quit()
                quit()
              # Send password
            driver.find_elements(By.CSS_SELECTOR, "[aria-label='Password']")[0].send_keys(password)
            sleep(2) # Wait for Log in to be clickable
            driver.find_element(By.XPATH, "//div[contains(text(), 'Log in')]").click()  # Login button click
            sleep(7)  # Login Wait Grace Period
            driver.find_element(By.ID, "slfErrorAlert")
            sleep(3)
        except NoSuchElementException:  # If error not found, successful login
            break
        else:  # If error found, try new user/pwd and go back to the top
            print("Username or Password is Incorrect! Try Again (Logout of Instagram if you are already logged in)\n")
            username, password = input_creds()


# MFA Support
def mfa_check():
    while True:
        try:
            sleep(3)
            wait = WebDriverWait(driver, 10)
            mfa_check_elem = wait.until(EC.presence_of_element_located((By.ID, "verificationCodeDescription")))
        except (NoSuchElementException, TimeoutException): # No MFA enabled, break and move on
            break
        if mfa_check_elem:  # Code needed
            mfa_code = input("Input MFA code: ")
            driver.find_element(By.CSS_SELECTOR, "[aria-label='Security Code']").send_keys(mfa_code)
            sleep(2) # Wait for MFA button to be clickable
            driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]").click()
            sleep(5)
        else:  # Must be a call then, if not code
            print("Waiting for MFA call to finish successfully...")
            sleep(10)  # Wait for finished call
        try:
            driver.find_element(By.ID, "twoFactorErrorAlert")
        except NoSuchElementException:  # If no error, return
            break
        else:  # If we had no error, the error was found, go back to top
            print("\nMFA code incorrect / timed out or MFA call not successful, Try Again.\n")
            # Remove incorrect MFA code
            input_box = driver.find_element(By.CSS_SELECTOR, "[aria-label='Security Code']")
            for i in range(10):
                input_box.send_keys(Keys.BACK_SPACE)
    print("\n")


# If not username, we cannot pass an email or phone #
# to a link like instagram.com/{username}/followers. 
# Instead, we have to go get real username
def username_fix(username):
    if '@' in username or username.isdigit():
        # We choose this page because it 404's and no other potential
        # usernames with the word 'Profile' can get in the way because it's blank
        driver.get("https://www.instagram.com/!!!")
        sleep(4)
        wait = WebDriverWait(driver, 10)
        profile_button = wait.until(EC.presence_of_element_located((By.XPATH, 
        "//span[text() = 'Profile']")))
        profile_button.click()
        sleep(4)
        username = driver.current_url.split('/')[-2]  # Get username from URL

    return username


def number_convert(amount):
    msg = '''\nThis account has >= 1 Million followers / following,
    which will take a long time to iterate through.
    Continue? (Y/n): '''

    if amount.find(',') != -1:  # Handle for commas and K in number, can't have both in one number
        amount = amount.replace(',', '')  # Make into int and remove commas if present
    elif amount.find('K') != -1:  # If K (thousand) is present
        amount = amount.replace('K', '') + "000"  # Remove K and add 000 to make it a usable thousand number
    elif amount.find('M') != -1:  # If account has a million or more followers, just quit
        if 'Y' in input(msg).upper():
            amount = amount.replace('M', '') + "000000"
        else:
            print("\nQuitting...\n")
            driver.quit()
            quit()

    # int() everything, not just the above cases e.g. 0-999
    return int(amount)


# Click on the right elements to get the follower/following lists
def get_numbers():
    # Get self page
    driver.get(f"https://www.instagram.com/{username}")
    sleep(3)

    # Use string() instead of text() here
    wait = WebDriverWait(driver, 10)
    raw_html = wait.until(EC.presence_of_all_elements_located((By.XPATH, 
    f"//div[contains(string(), ' following')]")))[2].get_attribute('innerHTML')

    # Get Followers Number, used to track javascript passes
    myAmountofFollowers = re.search(r'>([\d,]+[MK]?)</span></span>\s+followers', raw_html).group(1)
    myAmountofFollowers = number_convert(myAmountofFollowers)

    # Get Following Number
    myAmountofFollowing = re.search(r'>([\d,]+[MK]?)</span></span>\s+following', raw_html).group(1)
    myAmountofFollowing = number_convert(myAmountofFollowing)

    return [myAmountofFollowers, myAmountofFollowing]


def create_xhr_logs():
    wait = WebDriverWait(driver, 10)

    # Open 'Followers' Modal to get cookies
    driver.get(f"https://www.instagram.com/{username}/followers")
    sleep(5)

    scroll_elem = wait.until(EC.presence_of_element_located((By.XPATH, 
    "//div[contains(@style, 'height: auto; overflow: hidden auto;')]/..")))

    # Initital followers setup
    driver.execute_script("window.dispatchEvent(new Event('resize'));")
    driver.execute_script("arguments[0].scrollTop += 2000;", scroll_elem)

    sleep(2)

    # Followers w/ max_id
    driver.execute_script("window.dispatchEvent(new Event('resize'));")
    driver.execute_script("arguments[0].scrollTop += 2000;", scroll_elem)


def build_lists():
    followers, following = [], []

    # Need request info from dev tools 'Network' tab
    cookies = {}
    temp_headers = {}

    # https://gist.github.com/lorey/079c5e178c9c9d3c30ad87df7f70491d
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    for log in logs:
        if log["method"] != "Network.requestWillBeSentExtraInfo":
            continue

        if all(sub in log['params']['headers'][':path'] for sub in ["api/v1/friendships", "followers", "max_id"]):
            pairs = log['params']['headers']['cookie'].split("; ")
            for pair in pairs:
                key, value = pair.split("=")
                cookies[key] = value

            temp_headers = log['params']['headers']
            break

    # Remove "Headless"
    temp_headers['sec-ch-ua']=temp_headers['sec-ch-ua'].replace("HeadlessChrome", "Google Chrome")
    version_get = driver.execute_script("return navigator.userAgentData.getHighEntropyValues(['fullVersionList']).then((values) => { return values; });")
    sleep(1)
    chrome_version, nab_version = "", ""
    # Add proper version numbers to headers
    for i in version_get['fullVersionList']:
        if i['brand'] == "HeadlessChrome":
            chrome_version = i['version']
        if i['brand'] == "Not(A:Brand":
            nab_version = i['version']
    temp_headers['sec-ch-ua-full-version-list'] = f'"Chromium";v="{chrome_version}", "Not(A:Brand";v="{nab_version}", "Google Chrome";v="{chrome_version}"'

    headers = {'authority': "www.instagram.com",
               'accept': "*/*",
               'accept-language': "en-US,en;q=0.9",
               'dpr': f"{temp_headers['dpr']}",
               'referer': '',
               'sec-ch-prefers-color-scheme': "dark",
               'sec-ch-ua': f"{temp_headers['sec-ch-ua']}",
               'sec-ch-ua-full-version-list': f"{temp_headers['sec-ch-ua-full-version-list']}",
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-model': '""',
               'sec-ch-ua-platform': f"{temp_headers['sec-ch-ua-platform']}",
               'sec-ch-ua-platform-version': f"{temp_headers['sec-ch-ua-platform-version']}",
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'user-agent': f"{safe_user_agent}",
               'viewport-width': f"{random.uniform(460, 500)}",
               'x-asbd-id': f"{temp_headers['x-asbd-id']}",
               'x-csrftoken': f"{temp_headers['x-csrftoken']}",
               'x-ig-app-id': f"{temp_headers['x-ig-app-id']}",
               'x-ig-www-claim': f"{temp_headers['x-ig-www-claim']}",
               'x-requested-with': 'XMLHttpRequest'
    }

    # Build Followers List
    max_id = ""
    headers['referer'] = f"https://www.instagram.com/{username}/followers/?next=%2F"
    followers_setup_url = f"https://www.instagram.com/api/v1/friendships/{cookies['ds_user_id']}/followers/?count=12&search_surface=follow_list_page"

    # Initial
    resp = requests.get(url=followers_setup_url, headers=headers, cookies=cookies)
    data = resp.json()
    usernames = [user['username'] for user in data['users']]
    followers.extend(usernames)
    max_id = data['next_max_id']
    sleep(random.uniform(2, 3.5))

    # Normal
    print("\nPart 1/2 - Followers")
    while True:  # Go until no more 'next_max_id'
        # We need to keep initializing this f-string with the updated variables
        followers_url = f"https://www.instagram.com/api/v1/friendships/{cookies['ds_user_id']}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page"
        resp = requests.get(url=followers_url, headers=headers, cookies=cookies)
        data = resp.json()
        usernames = [user['username'] for user in data['users']]
        followers.extend([i for i in usernames if i not in followers])
        if 'next_max_id' in data:
            max_id = data['next_max_id']
        else:
            break
        sleep(random.uniform(2, 3.5))

    # Build Following List
    max_id = ""
    headers['referer'] = f"https://www.instagram.com/{username}/following/?next=%2F"
    following_setup_url = f"https://www.instagram.com/api/v1/friendships/{cookies['ds_user_id']}/following/?count=12"

    # Initial
    resp = requests.get(url=following_setup_url, headers=headers, cookies=cookies)
    data = resp.json()
    usernames = [user['username'] for user in data['users']]
    following.extend(usernames)
    max_id = data['next_max_id']
    sleep(random.uniform(2, 3.5))

    # Normal
    print("\nPart 2/2 - Following")
    while True:
        following_url = f"https://www.instagram.com/api/v1/friendships/{cookies['ds_user_id']}/following/?count=12&max_id={max_id}"
        resp = requests.get(url=following_url, headers=headers, cookies=cookies)
        data = resp.json()

        usernames = [user['username'] for user in data['users']]

        following.extend([i for i in usernames if i not in following])
        if 'next_max_id' in data:
            max_id = data['next_max_id']
        else:
            break
        sleep(random.uniform(2, 3.5))

    # differences = whoIFollow - (myFollowers - peopleIdontFollowBack)
    # People who I follow who are not my followers
    following_diff = list(set(following) - set(followers))  # Remove the people in my followers list from the following list (set logic)
    # Note to self: The results number is not necessarily just following - followers, because there are people that follow
    # me that I don't follow back. And they would be removed from the followers number. We are essentially just removing anything,
    # any dupes if we put the lists together, b/c a dupe means that we are both following each other. It's about the ones that don't follow back

    # Same logic applies here, everyone in followers who's not it
    # in following, so they follow us but we don't follow them back
    followers_diff = list(set(followers) - set(following))

    return [following_diff, followers_diff]


# Print Results to Console & Write Results File
def print_results(differences, username):
    following_diff = differences[0]
    followers_diff = differences[1]

    # Create file for writing results
    # Don't want to overwrite other result files so
    # add a (1), (2), (3) ...  to file name if need be
    f = None  # Want to use outside of the while-loop scope
    counter = 0
    while True:
        try:
            # if filename not taken
            if counter == 0:
                f = open("wicked_results.txt", "x")
            else:
                f = open(f"wicked_results ({counter}).txt", "x")
            # If no error, break loop
            break
        except FileExistsError:
            counter += 1

    # Header Variables
    following_results_string = f"Not Following You Back ({len(following_diff):,}):"
    followers_results_string = f"You Don't Follow Back ({len(followers_diff):,}):"
    following_len_string = len(following_results_string)*'-'
    followers_len_string = len(followers_results_string)*'-'

    # Write Results File
    f.write(f"Wicked v{version} Results File\n")
    f.write(f"Username: {username}\n")
    f.write(f"Date: {datetime.now().strftime('%b-%d-%Y %H:%M:%S')}\n\n")

    f.write(f"{following_results_string}\n")
    f.write(f"{following_len_string}\n")
    for i in following_diff:
        f.write(f"{i}\n")

    f.write("\n\n")

    f.write(f"{followers_results_string}\n")
    f.write(f"{followers_len_string}\n")
    for i in followers_diff:
        f.write(f"{i}\n")

    f.close()

    # Print Results to stdout
    print(green, " ")  # Newline before "Results: "

    # Lists Header
    print(f' {following_results_string:<50} {followers_results_string:<50}')
    print(f' {following_len_string:<50} {followers_len_string:<50}{reset}')

    # Lists Content
    for following, followers in zip_longest(following_diff, followers_diff, fillvalue=""):
        print(f' {following:<50} {followers:<50}')


def spinner_task(stop_event):
    spinner = cycle(['\\', '|', '/', '-'])
    while not stop_event.is_set():
        sleep(0.15)
        sys.stdout.write(f"[{next(spinner)}] Collecting Initial Info ...\x1b[?25l")
        sys.stdout.flush()
        sys.stdout.write('\b'*40)



if __name__ == "__main__":

    version = "5.0"

    if '--version' in sys.argv or '-v' in sys.argv:
        print(f"\nWicked v{version}\n")
        quit()

    if any(arg in sys.argv for arg in ['-h', '-u', '--help', '--usage']):
        print(f"\nWicked v{version}")
        print("-----------\n")
        print("See who's not following you back and who you don't follow back on Instagram!\n")
        print("Usage: This program does not take any flags, simply run this script with Python3")
        print("       You'll be prompted to put in your Instagram username & password, and MFA code")
        print("       if applicable\n")
        print("Nervous about giving this script your password? No worries! Take a look at the code")
        print("and you'll see that this program just passes it along to Instagram and nothing else.")
        print("It's also using TLS to send all the data.\n")
        quit()

    # Initialize colorama
    init()
    green, red, reset = Fore.GREEN, Fore.RED, Fore.RESET

    print_banner()

    username, password = input_creds()  # Enter and store creds

    # Driver initialization and argument setting
    chrome_options = Options()  # Initialize options
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")  # Do not use mobile template
    chrome_options.add_argument("--no-sandbox")  # Helping argument
    chrome_options.add_argument("--tls1.3")  # Encrypt info using TLS v1.3
    chrome_options.add_argument("--lang=en-US")  # Force English language so we can find the right elements
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"}) # Capture XHR

    # Init vars that chromedriver_setup will edit
    safe_user_agent = ""
    # Top level scope, all functions can access this variable
    driver = chromedriver_setup()

    instagram_login(username, password)

    mfa_check()

    # Start spinner thread
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_task, args=(stop_event,))
    spinner_thread.start()

    # Info collection
    username = username_fix(username)
    myAmountofFollowers, myAmountofFollowing = get_numbers()
    create_xhr_logs()

    # End spinner thread
    stop_event.set()
    spinner_thread.join()
    print(f"[+] Collecting Initial Info - {green}Done!{reset}\x1b[?25h\n")  # Show cursor again

    print(f"\nNumber of Followers: {myAmountofFollowers}")
    print(f"Number of Following: {myAmountofFollowing}\n")

    # Prevent from sleeping
    with keep.presenting() as k:
        differences = build_lists()

    driver.quit()

    print_results(differences, username)
