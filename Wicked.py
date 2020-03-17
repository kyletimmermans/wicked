'''
Kyle Timmermans
03/12/2020
Compiled in python 3.8.2

v1.0
'''

# Driving Chrome (Headless) with Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import getpass
import time
import colorama
from colorama import Fore
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
print("This make take some time depending on how many people you follow")
print(Fore.RESET)  # Reset text color

'''
print("[+] Checking Internet Connection: ", end='') + print(Fore.GREEN, "Working") if true, print(Fore.RED, "Error: No Internet Connection") && break if not
print(Fore.RESET)
print("[+] Checking if chromedriver is in this folder + print(Fore.GREEN, "Working") if true, print(Fore.RED, "Error: chromedriver not found in parent folder") && break if not
print(Fore.RESET)
'''

# Input insta creds
username = input("Input your Instagram username: ")
password = getpass.getpass("Input your password (Not Stored): ")  # getpass used to prevent shoulder surfing

# Begin driver
chrome_options = Options()  # Initialize options
chrome_options.add_argument("--headless")  # Headless option and Headed option return different HTML sometimes
chrome_options.add_argument('--no-sandbox')  # Helping argument
driver = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")  # ./ indicates this folder
driver.get("https://instagram.com")  # Login page
time.sleep(1)
driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input").send_keys(username)
driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input").send_keys(password)
driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[4]/button").click()  # Login button click
time.sleep(10)  # Login Wait Grace Period
driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/a/img").click()  # Go to instagram.com/username
time.sleep(3)

# Get Following Number
myAmountofFollowing = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text  # Used to track javascript passes
myAmountofFollowing = int(myAmountofFollowing.replace(',', '').replace('K', ''))  # Make into int and remove commas and 'K' (thousand) if present

# Get Followers Number
myAmountofFollowers = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text
myAmountofFollowers = int(myAmountofFollowers.replace(',', '').replace('K', ''))

# JavaScript Auto Scroll Div List - To Load All Elements (prints on one line)
scroll_script = ("var x = document.evaluate('/html/body/div[4]/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;"
                 "x.scrollTo(0, x.scrollHeight);")

# Send scrolls
def jsLoop(size):
    for i in range(int(size * 0.115)):  # Only 0.115 percent of total follow count = sufficient loops
        driver.execute_script(scroll_script)
        time.sleep(0.5)

# Used to get list of following and followers
def getList():
    tempList = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    x = soup.select("div > div > div > div > a")  # div > div > div > div > a  works best
    for i in x:
        if i.text.strip():  # Don't print whitespace lines
            tempList.append(i.text)
    return tempList

time.sleep(2)
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").click()  # Open 'Following' Modal
time.sleep(2)
jsLoop(myAmountofFollowing)
following = getList()  # Following List
time.sleep(2)
driver.execute_script("window.history.go(-1)")  # Close out of 'Following' Modal
time.sleep(2)
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()  # Open 'Followers' Modal
jsLoop(myAmountofFollowers)
followers = getList()  # Followers List

driver.quit()  # DON'T DELETE THIS

differences = list(set(following) - set(followers))  # Everyone in following list who's not in followers list

# Print Results to Console
for i in differences:
    print(i)
