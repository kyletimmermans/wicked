'''
Kyle Timmermans
05/16/20
Compiled in python 3.8.2
v2.3
'''

# Driving Chrome (Headless) with Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
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

creds = inputCreds()  # Enter and store creds

# Begin driver
chrome_options = Options()  # Initialize options
chrome_options.add_argument("--headless")  # Headless option and Headed option return different HTML sometimes
chrome_options.add_argument('--no-sandbox')  # Helping argument
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Turn off logs in windows

alreadyThere = False  # if localhost line is already present, we don't want to mess with it

def lineCheck(file, string):  # Check if hosts file is in normal spot, if not, show steps to fix
    try:
        with open(file, 'r') as hostsFile: #Open file in read-only
            for line in hostsFile:  # Check every line
                if string in line:  # If in the line, return True, else False
                    return True
        return False
    except FileNotFoundError:
        print(Fore.RED+"Error: "+Fore.RESET+"Hosts file not found! Make sure hosts file is in",  end=" ")  # append error handling to this string
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
    except WebDriverException:
        print(Fore.RED+"Error: "+Fore.RESET+"Correct chromedriver version file not found in working directory!")
        print("Try updating your current version of Chrome, and place an updated version of chromedriver in the 'Wicked.py' directory")
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
    except WebDriverException:
        print(Fore.RED+"Error: "+Fore.RESET+"Chromedriver not found in working directory!")
        print("Try updating your current version of Chrome, and place an updated version of chromedriver in the 'Wicked.py' directory")
        quit()

# Check if username / password is correct
while True:
    try:
        driver.get("https://instagram.com")  # Login page
        time.sleep(5)
        try:  # Check internet connection
            driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input").send_keys(creds[0])  # Send username
        except NoSuchElementException:
            print(Fore.RED+"Error: "+Fore.RESET+ "No Internet Connection!")
            quit()
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input").send_keys(creds[1])  # Send password
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[4]/button").click()  # Login button click
        print("")
        print("Establishing Connection with Instagram...")
        time.sleep(10)  # Login Wait Grace Period
        driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]").click()  # Go to instagram.com/username
        break  # Breakout of loop, correct login
    except ElementClickInterceptedException:
        print("")
        print("Username or Password is Incorrect! Try Again")
        print("")
        creds = inputCreds()

time.sleep(5)  # Wait after clicking on profile
# Get Following Number
myAmountofFollowing = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text  # Used to track javascript passes
myAmountofFollowing = int(myAmountofFollowing.replace(',', '').replace('K', ''))  # Make into int and remove commas and 'K' (thousand) if present

# Get Followers Number
myAmountofFollowers = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text
myAmountofFollowers = int(myAmountofFollowers.replace(',', '').replace('K', ''))

# JavaScript Auto Scroll Div List - To Load All Elements (prints in one line)
# Multi-line construct, extra quotations added. see scrolldown.js for vanilla script
scroll_script = ("var x = document.evaluate('/html/body/div[4]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;"
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
    x = soup.select("div > div > div > div > a")  # div > div > div > div > a  works best
    for i in x:
        if i.text.strip() and i.text != "1":  # Don't append whitespace, don't print just "1" randomly
            tempList.append(i.text)
    return tempList

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

# Remove hosts addition if it was made
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

differences = list(set(following) - set(followers))  # Everyone in following list who's not in followers list

# Print Results to Console
print(Fore.GREEN, " ")  # Space before "Results: "
print("Results: ", Fore.RESET)
for i in differences:
    print(i)

print("")  # Separate list from command line text
