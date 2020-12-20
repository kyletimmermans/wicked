'''
Kyle Timmermans
12/19/20
Compiled in python 3.8.2
v2.5
'''

# Driving Chrome (Headless) with Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import getpass
import time
import colorama
from colorama import Fore
from sys import platform
from tqdm import trange
colorama.init()  # Initialize colorama

print(Fore.GREEN) # Make ASCII Art and Banner Green
print(" ")
print("       .*.                                       ")
print("     *' + '*      ,       ,                      ")
print("      *'|'*       |`;`;`;`|                      ")
print("        |         |:.'.'.'|                      ")
print("        |         |:.:.:.:|                      ")
print("        |         |::....:|                                                    _________ _______  _        _______  ______  ")
print("        |        /`   / ` \                                           |\     /|\__   __/(  ____ \| \    /\(  ____ \(  __  \ ")
print("        |       (   .' ^ \^)                                          | )   ( |   ) (   | (    \/|  \  / /| (    \/| (  \  )")
print("        |_.,   (    \    -/(            You're" + "                        | | _ | |   | |   | |      |  (_/ / | (__    | |   ) |")
print("     ,~`|   `~./     )._=/  )  ,,            gonna"+ "                    | |( )| |   | |   | |      |   _ (  |  __)   | |   | |")
print("    {   |     (       )|   (.~`  `~,             be"+ "                   | || || |   | |   | |      |  ( \ \ | (      | |   ) |")
print("    {   |      \   _.'  \   )       }             pop-u-lar!"+"          | () () |___) (___| (____/\|  /  \ \| (____/\| (__/  )")
print("    ;   |       ;`\      `)-`       }     _.._   "+"                     (_______)\_______/(_______/|_/    \/(_______/(______/ ")
print("     '.(\,     ;   `\    / `.       }__.-'__.-'  ")
print("      ( (/-;~~`;     `\_/    ;   .'`  _.-'       ")
print("      `/|\/   .'\.    /o\   ,`~~`~~~~`           ")
print("       \| ` .'   \'--'   '-`                     ")
print("        |--',==~~`)       (`~~==,_               ")
print("        ,=~`      `-.     /       `~=,           ")
print("     ,=`             `-._/            `=,        ")
print(" ")
print("Created by: @KyleTimmermans")
print("ASCII Art by jgs")
print(" ")
print("See who's not following you back on Instagram!")
print("This may take some time depending on how many people you follow / follow you")
print(Fore.RESET)  # Reset text color

# Input insta creds
def inputCreds():
    username = input("Input your Instagram username: ")
    password = getpass.getpass("Input your password (Not Stored): ")  # getpass used to prevent shoulder surfing
    return [username, password]  # Return creds as list

print("If your profile is public, you can just leave the password field blank")
creds = inputCreds()  # Enter and store creds

# Begin driver
chrome_options = Options()  # Initialize options
chrome_options.add_argument("--headless")  # Headless option and Headed option return different HTML sometimes
chrome_options.add_argument("--window-size=1920,1080")  # Do not use mobile template
chrome_options.add_argument('--no-sandbox')  # Helping argument
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Turn off logs in windows

alreadyThere = False  # if localhost line is already present, we don't want to mess with it

# Remove hosts addition if it was made, needed for everytime an exception interrupts program
# So we can remove it even when it fails, e.g. is an exception also does quit()
def hostsRemoval(alreadyThere):
    if alreadyThere == False:
        if platform == "darwin" or platform == "linux" or platform == "linux2":  # OSX and Linux have same instructions
            readFile = open("/etc/hosts")
            lines = readFile.readlines()
            readFile.close()
            w = open("/etc/hosts", 'w')
            w.writelines([item for item in lines[:-1]])
            w.close()
        elif platform == "win32":  # Windows
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
        if platform == "darwin" or platform == "linux" or platform == "linux2":
            print("/etc/ and that the file is not hidden")
        elif platform == "win32":
            print("C:\Windows\System32\drivers\etc\ and that the file is not hidden")
        quit()

# Check OS type for correct path format and if hosts file needs to be changed
if platform == "darwin" or platform == "linux" or platform == "linux2":  # OSX and Linux have the same instructions
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
elif platform == "win32":  # Windows
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

# Check if username / password is correct
while True:
    try:
        driver.get("https://www.instagram.com/accounts/login/")  # Login page
        time.sleep(5)
        try:  # Check internet connection
            driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(creds[0])  # Send username
        except NoSuchElementException:
            print(Fore.RED+"Error: "+Fore.RESET+ "No Internet Connection!")
            hostsRemoval(alreadyThere)
            quit()
        driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(creds[1])  # Send password
        driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button/div").click()  # Login button click
        print("")
        print("Establishing Connection with Instagram...")
        time.sleep(10)  # Login Wait Grace Period
        driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]").click()  # Open profile pic modal (top right)
        time.sleep(0.5)  # Wait for modal to pop up
        driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div").click()  # Go to their profile page from profile pic modal
        time.sleep(5) # Wait after clicking on profile
        break  # Breakout of loop, there is a correct login
    except ElementClickInterceptedException:
        print("")
        print("Username or Password is Incorrect! Try Again")
        print("")
        creds = inputCreds()

# Get Following Number
myAmountofFollowing = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text  # Used to track javascript passes
if myAmountofFollowing.find(',') != -1:  # Handle for commas and K in number, can't have both in one number
    myAmountofFollowing = int(myAmountofFollowing.replace(',', ''))  # Make into int and remove commas if present
elif myAmountofFollowing.find('K') != -1:  # If K (thousand) is present
    myAmountofFollowing = int(myAmountofFollowing.replace('K', '') + "000")  # Remove K and add 000 to make it a usable thousand number
elif myAmountofFollowing.find('M') != -1:  # If account has a million or more followers, just quit
    print("")
    print("This account has >= 1 Million followers, you don't want to do that to your computer")
    hostsRemoval(alreadyThere)
    quit()

# Get Followers Number
myAmountofFollowers = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text
if myAmountofFollowers.find(',') != -1:  # Handle for commas and K in number, can't have both in one number
    myAmountofFollowers = int(myAmountofFollowers.replace(',', ''))  # Make into int and remove commas if present
elif myAmountofFollowers.find('K') != -1:  # If K (thousand) is present
    myAmountofFollowers = int(myAmountofFollowers.replace('K', '') + "000")  # Remove K and add 000 to make it a usable thousand number
elif myAmountofFollowers.find('M') != -1:  # If account has a million or more followers, just quit
    print("")
    print("This account follows >= 1 Million people, you don't want to do that to your computer")
    hostsRemoval(alreadyThere)
    quit()

# JavaScript Auto Scroll Div List - To Load All Elements (prints in one line)
# Multi-line construct, extra quotations added. see scrolldown.js for vanilla script
scroll_script = ("var x = document.evaluate('/html/body/div[5]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;"
                 "x.scrollTo(0, x.scrollHeight);")

# Send scrolls
def jsLoop(size):
    for i in trange(int(size * 0.115)):  # Only 0.115 percent of total follow count = sufficient loops, trange prints progressbar
        driver.execute_script(scroll_script)
        time.sleep(0.5)

# Used to get list of following and followers
def getList():
    tempList = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    x = soup.select("body > div > div > div > div > ul > div > li > div > div > div > div > span > a")  # Line to usernames in the HTML
    for i in x:
        if i.text.strip() and i.text != "1":  # Don't append whitespace, don't print just "1" randomly
            tempList.append(i.text)
    return tempList

# Run through following and followers lists and append as we go
time.sleep(2)
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").click()  # Open 'Following' Modal
time.sleep(2)
print("")
print("Part 1/2")
jsLoop(myAmountofFollowing)
following = getList()  # Following List
time.sleep(2)
driver.execute_script("window.history.go(-1)")  # Close out of 'Following' Modal
time.sleep(2)
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()  # Open 'Followers' Modal
print("Part 2/2")
jsLoop(myAmountofFollowers)
followers = getList()  # Followers List

driver.quit()  # DON'T DELETE THIS

hostsRemoval(alreadyThere) # Final chance to remove it

# differences = whoIFollow - (myFollowers - peopleIdontFollowBack)
differences = list(set(following) - set(followers))  # Remove the people in my followers list from the following list (set logic)
# Note to self: The results number is not necessarily just following - followers, because there are people that follow
# me that I don't follow back. And they would be removed from the followers number. We are essentially just removing anything,
# any dupes if we put the lists together, b/c a dupe means that we are both following each other. It's about the ones that don't follow back

# Print Results to Console
print(Fore.GREEN, " ")  # Space before "Results: "
print("Results (" + str(len(differences)) + "): " + Fore.RESET)  # Number of people noted as well
for i in differences:
    print(i)

print("")  # Separate list from command line text
