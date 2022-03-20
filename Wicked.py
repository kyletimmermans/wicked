#!/usr/bin/env python3

'''
Kyle Timmermans
Wicked v3.1
v3.1 Released: Feb 11, 2022
Compiled in Python 3.9.7
'''

# Driving Chrome (Headless) with Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as action
from bs4 import BeautifulSoup
from colorama import Fore
from tqdm import trange
import getpass
import time
import re
import sys


def print_banner():
    print(Fore.GREEN) # Make ASCII Art and Banner Green
    print("\n")
    print("       .*.                                       ")
    print("     *' + '*      ,       ,                      ")
    print("      *'|'*       |`;`;`;`|                      ")
    print("        |         |:.'.'.'|                      ")
    print("        |         |:.:.:.:|                      ")
    print("        |         |::....:|                                                    _________ _______  _        _______  ______               ______")
    print("        |        /`   / ` \                                           |\     /|\__   __/(  ____ \| \    /\(  ____ \(  __  \    |\     /|/ ___  \ ")
    print("        |       (   .' ^ \^)                                          | )   ( |   ) (   | (    \/|  \  / /| (    \/| (  \  )   | )   ( |\/   \  \\")
    print("        |_.,   (    \    -/(            You're" + "                        | | _ | |   | |   | |      |  (_/ / | (__    | |   ) |   | |   | |   ___) /")
    print("     ,~`|   `~./     )._=/  )  ,,            gonna"+ "                    | |( )| |   | |   | |      |   _ (  |  __)   | |   | |   ( (   ) )  (___ (")
    print("    {   |     (       )|   (.~`  `~,             be"+ "                   | || || |   | |   | |      |  ( \ \ | (      | |   ) |    \ \_/ /       ) \\")
    print("    {   |      \   _.'  \   )       }             pop-u-lar!"+"          | () () |___) (___| (____/\|  /  \ \| (____/\| (__/  )     \   /  /\___/  /")
    print("    ;   |       ;`\      `)-`       }     _.._   "+"                     (_______)\_______/(_______/|_/    \/(_______/(______/       \_/   \______/ ")
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
def inputCreds():
    username = input("Input your Instagram username: ")
    password = getpass.getpass("Input your password (Not Stored): ")  # getpass used to prevent shoulder surfing
    return [username, password]  # Return creds as list


# Remove hosts addition if it was made, needed for everytime an exception interrupts program
# So we can remove it even when it fails, e.g. is an exception also does quit()
def hostsRemoval(alreadyThere):
    if alreadyThere == False:
        if sys.platform == "darwin" or sys.platform == "linux" or sys.platform == "linux2":  # OSX and Linux have same instructions
            readFile = open("/etc/hosts")
            lines = readFile.readlines()
            readFile.close()
            w = open("/etc/hosts", 'w')
            w.writelines([item for item in lines[:-1]])
            w.close()
        elif sys.platform == "win32":  # Windows
            readFile = open("C:\Windows\System32\drivers\etc\hosts")
            lines = readFile.readlines()
            readFile.close()
            w = open("C:\Windows\System32\drivers\etc\hosts", 'w')
            w.writelines([item for item in lines[:-1]])
            w.close()


def lineCheck(file, string):  # Check if hosts file is in normal spot, if not, show steps to fix
    try:
        with open(file, 'r') as hostsFile: #Open file in read-only
            for line in hostsFile:  # Check every line
                if string in line:  # If in the line, return True, else False
                    return True
        return False
    except FileNotFoundError:
        print(Fore.RED+"Error: "+Fore.RESET+"Hosts file not found! Make sure hosts file is in", end=' ')  # append error handling to this string
        if sys.platform == "darwin" or sys.platform == "linux" or sys.platform == "linux2":
            print("/etc/ and that the file is not hidden")
        elif sys.platform == "win32":
            print("C:\Windows\System32\drivers\etc\ and that the file is not hidden")
        quit()


def chromedriver_setup():
    # Check OS type for correct path format and if hosts file needs to be changed
    if sys.platform == "darwin" or sys.platform == "linux" or sys.platform == "linux2":  # OSX and Linux have the same instructions
        # Go through each line, if not "127.0.0.1 localhost" go to next, if found, skip next step and set alreadyThere = True
        if lineCheck("/etc/hosts", "127.0.0.1 localhost"):  # If its there already
            alreadyThere = True
        else:
            host_file = open("/etc/hosts", "a")
            host_file.write("127.0.0.1 localhost #Wicked" + "\n")
            host_file.close()
        try:
            driver = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")  # ./ indicates this folder for OSX/Linux
            user_agent = driver.execute_script("return navigator.userAgent;").replace("Headless", "")  # Get the user agent and remove the word "Headless"
            chrome_options.add_argument(f'user-agent={user_agent}')  # Update our options with the safe user agent
            driver = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")  # Driver re-initialized with safe user agent
        except WebDriverException:
            print(Fore.RED+"Error: "+Fore.RESET+"Correct chromedriver version file not found in working directory!")
            print("Try updating your current version of Chrome, and place an updated version of chromedriver in the 'Wicked.py' directory")
            hostsRemoval(alreadyThere)
            quit()
    elif sys.platform == "win32":  # Windows
        if lineCheck("C:\Windows\System32\drivers\etc\hosts", "127.0.0.1 localhost"):
            alreadyThere = True
        else:
            host_file = open("C:\Windows\System32\drivers\etc\hosts", "a")
            host_file.write("127.0.0.1 localhost #Wicked" + "\n")
            host_file.close()
        try:
            driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")  # No need for path, using current working directory
            user_agent = driver.execute_script("return navigator.userAgent;").replace("Headless", "")  # Get the user agent and remove the word "Headless"
            chrome_options.add_argument(f'user-agent={user_agent}')  # Update our options with the safe user agent
            driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver.exe")  # Driver re-initialized with safe user agent
        except WebDriverException:
            print(Fore.RED+"Error: "+Fore.RESET+"Chromedriver not found in working directory!")
            print("Try updating your current version of Chrome, and place an updated version of chromedriver in the 'Wicked.py' directory")
            hostsRemoval(alreadyThere)
            quit()

    return driver


def instagram_login(creds):
    # Check if username / password is correct
    while True:
        try:
            print("\nEstablishing Connection with Instagram...\n")
            driver.get("https://www.instagram.com/accounts/login/")  # Login page
            time.sleep(5)
            try:  # Check internet connection
                driver.find_element_by_css_selector("[aria-label='Phone number, username, or email']").send_keys(creds[0])  # Send username
            except NoSuchElementException:
                print(Fore.RED+"Error: "+Fore.RESET+ "No Internet Connection!")
                hostsRemoval(alreadyThere)
                quit()
            driver.find_elements_by_css_selector("[aria-label='Password']")[0].send_keys(creds[1])  # Send password
            driver.find_element_by_xpath("//div[contains(text(), 'Log In')]").click()  # Login button click
            time.sleep(7)  # Login Wait Grace Period
            driver.find_element_by_id("slfErrorAlert")
            time.sleep(3)
        except NoSuchElementException:  # If error not found, successful login
            break
        else:  # If error found, try new user/pwd and go back to the top
            print("Username or Password is Incorrect! Try Again (Logout of Instagram if you are already logged in)\n")
            creds = inputCreds()


# MFA Support
def mfa_check():
    while True:
        try:
            time.sleep(3)
            mfa_check = driver.find_elements_by_id("verificationCodeDescription")
        except NoSuchElementException:
            break
        if mfa_check:  # Code needed
            mfa_code = input("Input MFA code: ")
            driver.find_element_by_css_selector("[aria-label='Security Code']").send_keys(mfa_code)
            time.sleep(2)
            driver.find_element_by_xpath("//button[contains(text(), 'Confirm')]").click()
            time.sleep(5)
        else:  # Must be a call then, if not code
            print("Waiting for MFA call to finish successfully...")
            time.sleep(10)  # Wait for finished call
        try:
            driver.find_element_by_id("twoFactorErrorAlert")
        except NoSuchElementException:  # If no error, return
            break
        else:  # If we had no error, the error was found, go back to top
            print("MFA code incorrect or MFA call not successful, Try Again.\n")


# Click on the right elements to get the follower/following lists
def open_elements(creds):
    # Get self page
    driver.get(f"https://www.instagram.com/{creds[0]}")
    time.sleep(3)

    # Get Following Number, used to track javascript passes
    # Use string() over text() here
    myAmountofFollowing = driver.find_elements_by_xpath("//div[contains(string(), ' following')]")[2].get_attribute('innerHTML')
    myAmountofFollowing = re.search('(?<=">)(.*)(?=</span)', myAmountofFollowing).group(0)  # Match object needs group()
    if myAmountofFollowing.find(',') != -1:  # Handle for commas and K in number, can't have both in one number
        myAmountofFollowing = int(myAmountofFollowing.replace(',', ''))  # Make into int and remove commas if present
    elif myAmountofFollowing.find('K') != -1:  # If K (thousand) is present
        myAmountofFollowing = int(myAmountofFollowing.replace('K', '') + "000")  # Remove K and add 000 to make it a usable thousand number
    elif myAmountofFollowing.find('M') != -1:  # If account has a million or more followers, just quit
        print("\nThis account has >= 1 Million followers, you don't want to do that to your computer")
        hostsRemoval(alreadyThere)
        quit()

    # Get Followers Number
    myAmountofFollowers = driver.find_elements_by_xpath("//div[contains(string(), ' followers')]")[2].get_attribute('innerHTML')
    myAmountofFollowers = re.search('(?<=">)(.*)(?=</span)', myAmountofFollowers).group(0)
    if myAmountofFollowers.find(',') != -1:  # Handle for commas and K in number, can't have both in one number
        myAmountofFollowers = int(myAmountofFollowers.replace(',', ''))  # Make into int and remove commas if present
    elif myAmountofFollowers.find('K') != -1:  # If K (thousand) is present
        myAmountofFollowers = int(myAmountofFollowers.replace('K', '') + "000")  # Remove K and add 000 to make it a usable thousand number
    elif myAmountofFollowers.find('M') != -1:  # If account has a million or more followers, just quit
        print("\nThis account follows >= 1 Million people, you don't want to do that to your computer")
        hostsRemoval(alreadyThere)
        quit()

    return [myAmountofFollowing, myAmountofFollowers]


# Send scrolls (Elements begin top left of rectangle, use Chrome devtools to show)
def scroll_loop(size, type):
    if type == "followers":
        followers_modal = driver.find_element_by_xpath("//h1[contains(text(), 'Followers')]")
        action(driver).move_by_offset(followers_modal.location['x']+232,followers_modal.location['y']+100).perform()
        time.sleep(0.5)
        action(driver).context_click().perform()  # One right click to start the scrolls
        time.sleep(2)
    elif type == "following":  # Set one cursor offset, works for both modals. Otherwise double moves makes out of bounds
        following_modal = driver.find_element_by_xpath("//div[contains(text(), 'People')]")  # 'Following' used everywhere, do not use
        time.sleep(0.5)
        action(driver).context_click().perform()  # Right click, not left. Prevents redirecting but allows scrolling
        time.sleep(2)
    for i in trange(int(size / 2.7)):  # total follow count / 2.7 = sufficient loops to get everything, trange prints progressbar
        action(driver).context_click().perform()
        action(driver).send_keys(Keys.PAGE_DOWN).perform();
        time.sleep(0.5)


# Used to get list of following and followers
def getList():
    tempList = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    x = soup.select("li > div > div > div > div > span > a > span")  # Line to usernames in the HTML (End of XPATH)
    for i in x:
        if i.text.strip() and i.text != "1":  # Don't append whitespace, don't print just "1" randomly
            tempList.append(i.text)
    return tempList


# Run through following and followers lists and append as we go
def collect_and_finish(myAmountofFollowing, myAmountofFollowers):
    time.sleep(2)
    driver.find_elements_by_xpath("//div[contains(string(), ' followers')]")[2].click()  # Open 'Followers' Modal
    print("\nPart 1/2")
    time.sleep(2)
    scroll_loop(myAmountofFollowers, "followers")
    followers = getList()  # Followers List
    time.sleep(2)
    driver.execute_script("window.history.go(-1)")  # Close out of 'Followers' Modal
    time.sleep(2)
    driver.find_elements_by_xpath("//div[contains(string(), ' following')]")[2].click()  # Open 'Following' Modal
    time.sleep(2)
    print("Part 2/2")
    scroll_loop(myAmountofFollowing, "following")
    following = getList()  # Following List
    driver.quit()  # DON'T DELETE THIS
    hostsRemoval(alreadyThere) # Final chance to remove it

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
    print("Results (" + str(len(differences)) + "): " + Fore.RESET)  # Number of people noted as well
    for i in differences:
        print(i)
    print("")  # Formatting space away from next prompt line


if __name__ == "__main__":

    if '--version' in sys.argv or '-v' in sys.argv:
        print("\nWicked v3.1\n")
        quit()

    colorama.init()  # Initialize colorama
    
    print_banner()

    creds = inputCreds()  # Enter and store creds

    # Driver initialization and argument setting
    chrome_options = Options()  # Initialize options
    chrome_options.add_argument("--headless")  # Headless option and Headed option return different HTML sometimes
    chrome_options.add_argument("--window-size=1920,1080")  # Do not use mobile template
    chrome_options.add_argument("--no-sandbox")  # Helping argument
    chrome_options.add_argument("--tls1.2")  # Encrypt info using TLS v1.2
    chrome_options.add_argument("--lang=en-US")  # Force English language so we can find the right elements
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Turn off logs in windows

    alreadyThere = False  # if localhost line is already present, we don't want to mess with it

    driver = chromedriver_setup()

    instagram_login(creds)

    mfa_check()

    myAmountofFollowing, myAmountofFollowers = open_elements(creds)

    differences = collect_and_finish(myAmountofFollowing, myAmountofFollowers)

    print_results(differences)
