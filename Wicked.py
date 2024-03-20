#!/usr/bin/env python3

'''
Kyle Timmermans
Wicked v6.0
March 20, 2024
Python 3.12.2
'''

# Base imports
import re
import sys
import json
import random
import pwinput
import requests
import urllib.parse
from math import ceil
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
    NoSuchElementException
)


def print_banner():
    print(green) # Make ASCII Art and Banner Green (figlet - 'epic' font)
    print("       .*.                                       ")
    print("     *' + '*      ,       ,                      ")
    print("      *'|'*       |`;`;`;`|                      ")
    print("        |         |:.'.'.'|                      ")
    print("        |         |:.:.:.:|                      ")
    print("        |         |::....:|                                                    _________ _______  _        _______  ______                ______")
    print("        |        /`   / ` \\                                           |\\     /|\\__   __/(  ____ \\| \\    /\\(  ____ \\(  __  \\    |\\     /| / ____ \\")
    print("        |       (   .' ^ \\^)                                          | )   ( |   ) (   | (    \\/|  \\  / /| (    \\/| (  \\  )   | )   ( |( (    \\/")
    print("        |_.,   (    \\    -/(            You're" + "                        | | _ | |   | |   | |      |  (_/ / | (__    | |   ) |   | |   | || (____  ")
    print("     ,~`|   `~./     )._=/  )  ,,            gonna"+ "                    | |( )| |   | |   | |      |   _ (  |  __)   | |   | |   ( (   ) )|  ___ \\ ")
    print("    {   |     (       )|   (.~`  `~,             be"+ "                   | || || |   | |   | |      |  ( \\ \\ | (      | |   ) |    \\ \\_/ / | (   ) )")
    print("    {   |      \\   _.'  \\   )       }             pop-u-lar!"+"          | () () |___) (___| (____/\\|  /  \\ \\| (____/\\| (__/  )     \\   /  ( (___) )")
    print("    ;   |       ;`\\      `)-`       }     _.._   "+"                     (_______)\\_______/(_______/|_/    \\/(_______/(______/       \\_/    \\_____/")
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
    chrome_options.add_argument(f'--user-agent={safe_user_agent}')
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


def create_headers():
    sleep(5)  # Allow headers to build up

    temp_headers = {}

    safe_user_agent = driver.execute_script("return navigator.userAgent;")

    # https://gist.github.com/lorey/079c5e178c9c9d3c30ad87df7f70491d
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    # Keep going and save the last one
    for log in logs:
        if log["method"] != "Network.requestWillBeSentExtraInfo":
            continue

        if "api/graphql" in log['params']['headers'][':path']:
            try:
                if log['params']['headers']['cookie']:
                    temp_headers = log['params']['headers']
                    break
            except KeyError:
                continue

    headers = {
           'authority': "www.instagram.com",
           'accept': "*/*",
           'accept-language': "en-US,en;q=0.9",
           'cookie': f"{temp_headers['cookie']}",
           'dpr': f"{temp_headers['dpr']}",
           'referer': f"https://www.instagram.com/{username}/",
           'sec-ch-prefers-color-scheme': "dark",
           'sec-ch-ua': f"{temp_headers['sec-ch-ua']}",
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-model': '""',
           'sec-ch-ua-platform': f"{temp_headers['sec-ch-ua-platform']}",
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-origin',
           'user-agent': f"{safe_user_agent}",
           'viewport-width': f"{random.uniform(460, 500)}"
    }

    return headers


def build_lists():
    followers, following = [], []

    user_id = re.search(r'ds_user_id=(\d+)', headers['cookie']).group(1)

    print("Part 1/2 - Followers")
    # Init
    followers_init_url = f'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%2C%22after%22%3Anull%7D'
    resp = requests.get(url=followers_init_url, headers=headers)
    data = resp.json()
    followers.extend([i['node']['username'] for i in data['data']['user']['edge_followed_by']['edges']])
    num_followers = int(data['data']['user']['edge_followed_by']['count'])
    after_val = urllib.parse.quote(data['data']['user']['edge_followed_by']['page_info']['end_cursor'])
    sleep(random.uniform(2, 3.5))

    # Normal
    for i in trange(ceil(num_followers/50)):
        followers_norm_url = f'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%2C%22after%22%3A%22{after_val}%22%7D'
        resp = requests.get(url=followers_norm_url, headers=headers)
        data = resp.json()
        followers.extend([i['node']['username'] for i in data['data']['user']['edge_followed_by']['edges']])
        after_val = urllib.parse.quote(data['data']['user']['edge_followed_by']['page_info']['end_cursor'])
        sleep(random.uniform(2, 3.5))
    

    print("\nPart 2/2 - Following")
    following_init_url = f'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{user_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%2C%22after%22%3Anull%7D'
    resp = requests.get(url=following_init_url, headers=headers)
    data = resp.json()
    following.extend([i['node']['username'] for i in data['data']['user']['edge_follow']['edges']])
    num_following = int(data['data']['user']['edge_follow']['count'])
    after_val = urllib.parse.quote(data['data']['user']['edge_follow']['page_info']['end_cursor'])
    sleep(random.uniform(2, 3.5))

    for i in trange(ceil(num_following/50)):
        following_norm_url = f'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{user_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%2C%22after%22%3A%22{after_val}%22%7D'
        resp = requests.get(url=following_norm_url, headers=headers)
        data = resp.json()
        following.extend([i['node']['username'] for i in data['data']['user']['edge_follow']['edges']])
        after_val = after_val = urllib.parse.quote(data['data']['user']['edge_follow']['page_info']['end_cursor'])
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
    print(green, "\n")  # Newline before "Results: "

    # Lists Header
    print(f' {following_results_string:<50} {followers_results_string:<50}')
    print(f' {following_len_string:<50} {followers_len_string:<50}{reset}')

    # Lists Content
    for following, followers in zip_longest(following_diff, followers_diff, fillvalue=""):
        print(f' {following:<50} {followers:<50}')



if __name__ == "__main__":

    version = "6.0"

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

    # Driver initialization and argument settings
    chrome_options = Options()  # Initialize options
    chrome_options.add_argument("--headless=new")  # =new is better option
    chrome_options.add_argument("--window-size=1920,1080")  # Do not use mobile template
    chrome_options.add_argument("--no-sandbox")  # Helping argument
    chrome_options.add_argument("--tls1.3")  # Encrypt info using TLS v1.3
    chrome_options.add_argument("--lang=en-US")  # Force English language so we can find the right elements
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Turn off stdout logs on Windows
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Capture XHR

    # Top level scope, all functions can access this variable
    driver = chromedriver_setup()

    instagram_login(username, password)

    mfa_check()

    username = username_fix(username)

    headers = create_headers()

    # Prevent from sleeping
    with keep.presenting() as k:
        differences = build_lists()

    driver.quit()

    print_results(differences, username)
