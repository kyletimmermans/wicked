#!/usr/bin/env python3


'''
Kyle Timmermans
Wicked v4.0
v4.0 Released: Sep 3, 2023
Compiled in Python 3.11.4
'''


import re
import sys
import time
import getpass
from tqdm import trange
from wakepy import keep
from bs4 import BeautifulSoup
from colorama import Fore, init

# Driving Chrome (Headless) with Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as action
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    ElementClickInterceptedException
)


def print_banner():
    print(Fore.GREEN) # Make ASCII Art and Banner Green
    print("\n")
    print("       .*.                                       ")
    print("     *' + '*      ,       ,                      ")
    print("      *'|'*       |`;`;`;`|                      ")
    print("        |         |:.'.'.'|                      ")
    print("        |         |:.:.:.:|                      ")
    print("        |         |::....:|                                                    _________ _______  _        _______  ______                  ___")
    print("        |        /`   / ` \                                           |\     /|\__   __/(  ____ \| \    /\(  ____ \(  __  \    |\     /|   /   )")
    print("        |       (   .' ^ \^)                                          | )   ( |   ) (   | (    \/|  \  / /| (    \/| (  \  )   | )   ( |  / /) |")
    print("        |_.,   (    \    -/(            You're" + "                        | | _ | |   | |   | |      |  (_/ / | (__    | |   ) |   | |   | | / (_) (_")
    print("     ,~`|   `~./     )._=/  )  ,,            gonna"+ "                    | |( )| |   | |   | |      |   _ (  |  __)   | |   | |   ( (   ) )(____   _)")
    print("    {   |     (       )|   (.~`  `~,             be"+ "                   | || || |   | |   | |      |  ( \ \ | (      | |   ) |    \ \_/ /      ) (")
    print("    {   |      \   _.'  \   )       }             pop-u-lar!"+"          | () () |___) (___| (____/\|  /  \ \| (____/\| (__/  )     \   /       | |")
    print("    ;   |       ;`\      `)-`       }     _.._   "+"                     (_______)\_______/(_______/|_/    \/(_______/(______/       \_/        (_)")
    print("     '.(\,     ;   `\    / `.       }__.-'__.-'  ")
    print("      ( (/-;~~`;     `\_/    ;   .'`  _.-'       ")
    print("      `/|\/   .'\.    /o\   ,`~~`~~~~`           ")
    print("       \| ` .'   \'--'   '-`                     ")
    print("        |--',==~~`)       (`~~==,_               ")
    print("        ,=~`      `-.     /       `~=,           ")
    print("     ,=`             `-._/            `=,        ")
    print("\n")
    print("Created by: @KyleTimmermans")
    print("ASCII Art by jgs\n")
    print("See who's not following you back on Instagram!")
    print("This may take some time depending on how many people you follow / follow you")
    print(Fore.RESET)  # Reset text color


# Input insta creds
def input_creds():
    username = input("Input your Instagram Username / Email / Phone #: ")
    password = getpass.getpass("Input your password (Not Stored): ")  # getpass used to prevent shoulder surfing

    return [username, password]  # Return creds as list


# If not username, we cannot pass an email or phone #
# to a link like instagram.com/{username}/followers. 
# Instead, we have to go get real username
def username_fix(username):
    if '@' in username or username.isdigit():
        # We choose this page because it 404's and no other potential
        # usernames with the word 'Profile' can get in the way because it's blank
        driver.get("https://www.instagram.com/!!!")
        time.sleep(4)
        wait = WebDriverWait(driver, 10)
        profile_button = wait.until(EC.presence_of_element_located((By.XPATH, 
        "//span[text() = 'Profile']")))
        profile_button.click()
        time.sleep(4)
        username = driver.current_url.split('/')[-2]  # Get username from URL

    return username


# Remove hosts addition if it was made, needed for everytime an exception interrupts program
# So we can remove it even when it fails, e.g. is an exception also does quit()
def hosts_removal(alreadyThere):
    if alreadyThere == False:
        if sys.platform in ("darwin", "linux", "linux2"):  # OSX and Linux have same instructions
            readFile = open("/etc/hosts")
            lines = readFile.readlines()
            readFile.close()
            w = open("/etc/hosts", 'w')
            w.writelines([item for item in lines[:-1]])
            w.close()
        elif sys.platform == "win32":  # Windows
            readFile = open("C:\\Windows\\System32\\drivers\\etc\\hosts")
            lines = readFile.readlines()
            readFile.close()
            w = open("C:\\Windows\\System32\\drivers\\etc\\hosts", 'w')
            w.writelines([item for item in lines[:-1]])
            w.close()


def line_check(file, string):  # Check if hosts file is in normal spot, if not, show steps to fix
    try:
        with open(file, 'r') as hostsFile: #Open file in read-only
            for line in hostsFile:  # Check every line
                if string in line:  # If in the line, return True, else False
                    return True
        return False
    except FileNotFoundError:
        print("\n"+Fore.RED+"Error: "+Fore.RESET+"Hosts file not found! Make sure hosts file is in", end=' ')  # append error handling to this string
        if sys.platform in ("darwin", "linux", "linux2"):
            print("/etc/ and that the file is not hidden")
        elif sys.platform == "win32":
            print("C:\\Windows\\System32\\drivers\\etc\\ and that the file is not hidden")
        quit()


def chromedriver_setup():
    # Check OS type for correct path format and if hosts file needs to be changed
    if sys.platform in ("darwin", "linux", "linux2"):  # OSX and Linux have the same instructions
        # Go through each line, if not "127.0.0.1 localhost" go to next, if found, skip next step and set alreadyThere = True
        if line_check("/etc/hosts", "127.0.0.1 localhost"):  # If its there already
            alreadyThere = True
        else:
            host_file = open("/etc/hosts", "a")
            host_file.write("127.0.0.1 localhost #Wicked" + "\n")
            host_file.close()
        try:
            service = Service(executable_path="./chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)  # ./ indicates this folder for OSX/Linux
            user_agent = driver.execute_script("return navigator.userAgent;").replace("Headless", "")  # Get the user agent and remove the word "Headless"
            driver.quit()
            chrome_options.add_argument(f'user-agent={user_agent}')  # Update our options with the safe user agent
            driver = webdriver.Chrome(service=service, options=chrome_options)  # Driver re-initialized with safe user agent
        except WebDriverException:
            print("\n"+Fore.RED+"Error: "+Fore.RESET+"Correct chromedriver version file not found in working directory!")
            print("Try updating your current version of Chrome, and place an "
                  "updated version of chromedriver in the 'Wicked.py' directory\n")
            hosts_removal(alreadyThere)
            quit()
    elif sys.platform == "win32":  # Windows
        if line_check("C:\\Windows\\System32\\drivers\\etc\\hosts", "127.0.0.1 localhost"):
            alreadyThere = True
        else:
            host_file = open("C:\\Windows\\System32\\drivers\\etc\\hosts", "a")
            host_file.write("127.0.0.1 localhost #Wicked" + "\n")
            host_file.close()
        try:
            service = Service(executable_path="chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=chrome_options)  # No need for path, using current working directory
            user_agent = driver.execute_script("return navigator.userAgent;").replace("Headless", "")  # Get the user agent and remove the word "Headless"
            driver.quit()
            chrome_options.add_argument(f'user-agent={user_agent}')  # Update our options with the safe user agent
            driver = webdriver.Chrome(service=service, options=chrome_options)  # Driver re-initialized with safe user agent
        except WebDriverException:
            print("\n"+Fore.RED+"Error: "+Fore.RESET+"Chromedriver not found in working directory!")
            print("Try updating your current version of Chrome, and place an "
                  "updated version of chromedriver in the 'Wicked.py' directory\n")
            hosts_removal(alreadyThere)
            quit()

    return driver


def instagram_login(creds):
    # Check if username / password is correct
    while True:
        try:
            print("\nEstablishing Connection with Instagram...\n")
            driver.get("https://www.instagram.com/accounts/login/")  # Login page
            time.sleep(7)
            try:  # Check internet connection
                driver.find_element(By.CSS_SELECTOR, "[aria-label='Phone number, username, or email']").send_keys(creds[0])  # Send username
            except NoSuchElementException:
                print("\n"+Fore.RED+"Error: "+Fore.RESET+ "No Internet Connection!")
                driver.quit()
                hosts_removal(alreadyThere)
                quit()
              # Send password
            driver.find_elements(By.CSS_SELECTOR, "[aria-label='Password']")[0].send_keys(creds[1])
            time.sleep(2) # Wait for Log in to be clickable
            driver.find_element(By.XPATH, "//div[contains(text(), 'Log in')]").click()  # Login button click
            time.sleep(7)  # Login Wait Grace Period
            driver.find_element(By.ID, "slfErrorAlert")
            time.sleep(3)
        except NoSuchElementException:  # If error not found, successful login
            break
        else:  # If error found, try new user/pwd and go back to the top
            print("Username or Password is Incorrect! Try Again (Logout of Instagram if you are already logged in)\n")
            creds = input_creds()


# MFA Support
def mfa_check():
    while True:
        try:
            time.sleep(3)
            wait = WebDriverWait(driver, 10)
            mfa_check = wait.until(EC.presence_of_element_located((By.ID, "verificationCodeDescription")))
        except (NoSuchElementException, TimeoutException): # No MFA enabled, break and move on
            break
        if mfa_check:  # Code needed
            mfa_code = input("Input MFA code: ")
            driver.find_element(By.CSS_SELECTOR, "[aria-label='Security Code']").send_keys(mfa_code)
            time.sleep(2) # Wait for MFA button to be clickable
            driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]").click()
            time.sleep(5)
        else:  # Must be a call then, if not code
            print("Waiting for MFA call to finish successfully...")
            time.sleep(10)  # Wait for finished call
        try:
            driver.find_element(By.ID, "twoFactorErrorAlert")
        except NoSuchElementException:  # If no error, return
            break
        else:  # If we had no error, the error was found, go back to top
            print("MFA code incorrect or MFA call not successful, Try Again.\n")


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
            hosts_removal(alreadyThere)
            quit()

    # int() everything, not just the above cases e.g. 0-999
    return int(amount)


# Click on the right elements to get the follower/following lists
def open_elements():
    # Get self page
    # Change once, always fixed (If email or phone #), otherwise no change
    creds[0] = username_fix(creds[0])
    driver.get(f"https://www.instagram.com/{creds[0]}")
    time.sleep(3)

    # Use string() instead of text() here
    wait = WebDriverWait(driver, 10)
    raw_html = wait.until(EC.presence_of_all_elements_located((By.XPATH, 
    f"//div[contains(string(), ' following')]")))[2].get_attribute('innerHTML')

    # Get Followers Number, used to track javascript passes
    myAmountofFollowers = re.search(r'<span>([\d,]+[MK]?)</span></span>\s+followers', raw_html).group(1)
    myAmountofFollowers = number_convert(myAmountofFollowers)

    # Get Following Number
    myAmountofFollowing = re.search(r'<span>([\d,]+[MK]?)</span></span>\s+following', raw_html).group(1)
    myAmountofFollowing = number_convert(myAmountofFollowing)

    return [myAmountofFollowers, myAmountofFollowing]


# Send scrolls to load usernames in modal and into HTML of page
def scroll_loop(size):
    wait = WebDriverWait(driver, 10)
    try:
        # Get searchable child and parent (scrollable) all in one line
        scroll_elem = wait.until(EC.presence_of_element_located((By.XPATH, 
        "//div[contains(@style, 'height: auto; overflow: hidden auto;')]/..")))
    except TimeoutException:
        print("\n"+Fore.RED+"Timeout Error: "+Fore.RESET+"Instagram might be timing you out, try using this program later\n")
        driver.quit()
        hosts_removal(alreadyThere)
        quit()

    # total follow count / 2.7 = sufficient loops to get everything, trange prints progressbar
    for i in trange(int(size / 2.7)):
        driver.execute_script("arguments[0].scrollTop += 2000;", scroll_elem)
        time.sleep(0.5)


# Used to get list of following and followers
def get_list():
    tempList = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # In case "Suggested for you" pops up in following modal
    # Remove the extra accounts they suggest, we do not follow them
    if suggested_check := soup.find(text="Suggested for you"):
        for sibling in suggested_check.find_all_next(True):
            sibling.extract()

    # Make HTML selector small so changes to tree don't affect selection (not too specific)
    # Less to break
    username_list = soup.select("a > div > div > span")  # Line to usernames in the HTML (End of XPATH)
    for i in username_list:
        # Don't append whitespace, don't print just "1" randomly
        if i.text.strip() and i.text != "1":
            tempList.append(i.text)
    return tempList


# Run through following and followers lists and append as we go
def collect_and_finish(myAmountofFollowers, myAmountofFollowing):
    time.sleep(2)
    driver.get(f"https://www.instagram.com/{creds[0]}/followers")  # Open 'Followers' Modal
    print("\nPart 1/2")
    time.sleep(5)
    # Handle 0 followers
    if myAmountofFollowers != 0:
        scroll_loop(myAmountofFollowers)
        followers = get_list()  # Followers List
    else:
        followers = []
    time.sleep(2)
    driver.get(f"https://www.instagram.com/{creds[0]}/following")  # Open 'Following' Modal
    time.sleep(5)
    print("\nPart 2/2")
    # Handle 0 following
    if myAmountofFollowing != 0:
        scroll_loop(myAmountofFollowing)
        following = get_list()  # Following List
    else:
        following = []
    driver.quit()  # DON'T DELETE THIS
    hosts_removal(alreadyThere) # Final chance to remove it

    # differences = whoIFollow - (myFollowers - peopleIdontFollowBack)
    # People who I follow who are not my followers
    differences = list(set(following) - set(followers))  # Remove the people in my followers list from the following list (set logic)
    # Note to self: The results number is not necessarily just following - followers, because there are people that follow
    # me that I don't follow back. And they would be removed from the followers number. We are essentially just removing anything,
    # any dupes if we put the lists together, b/c a dupe means that we are both following each other. It's about the ones that don't follow back

    return differences


# Print Results to Console
def print_results(differences):
    print(Fore.GREEN, " ")  # Space before "Results: "
    print(f"Results ({len(differences):,}):{Fore.RESET}")  # Number of people noted as well
    for i in differences:
        print(i)
    print("")  # Formatting space away from next prompt line


if __name__ == "__main__":

    if '--version' in sys.argv or '-v' in sys.argv:
        print("\nWicked v4.0\n")
        quit()

    init()  # Initialize colorama
    
    print_banner()

    creds = input_creds()  # Enter and store creds

    # Driver initialization and argument setting
    chrome_options = Options()  # Initialize options
    chrome_options.add_argument("--headless")  # Headless option and Headed option return different HTML sometimes
    chrome_options.add_argument("--window-size=1920,1080")  # Do not use mobile template
    chrome_options.add_argument("--no-sandbox")  # Helping argument
    chrome_options.add_argument("--tls1.2")  # Encrypt info using TLS v1.2
    chrome_options.add_argument("--lang=en-US")  # Force English language so we can find the right elements
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Turn off logs in windows

    alreadyThere = False  # if localhost line is already present, we don't want to mess with it

    # Top level scope, all functions can access this variable
    driver = chromedriver_setup()

    instagram_login(creds)

    mfa_check()

    myAmountofFollowers, myAmountofFollowing = open_elements()

    # wakepy prevent screenlock / sleep which causes Selenium crash
    with keep.presenting() as k:
        differences = collect_and_finish(myAmountofFollowers, myAmountofFollowing)

    print_results(differences)
