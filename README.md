![Version 4.7](http://img.shields.io/badge/version-v4.7-orange.svg)
![Python 3.11](http://img.shields.io/badge/python-3.11-blue.svg)
![Latest Commit](https://img.shields.io/github/last-commit/kyletimmermans/wicked?color=green)
[![kyletimmermans Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/kyletimmermans)

# <div align="center">Wicked</div>

A program that prints a list of people that you follow, but don't follow you back on Instagram, using Selenium and Beautiful Soup

</br>

## How it works:
This program scrapes Instagram web pages that contain the usernames of the people the you follow and who are following you. By comparing the two lists, it returns all the usernames that are in the "Following" list and are not in your "Followers" list. Essentially, showing you who has not followed you back. This program does not use the Instagram API.

</br>

## How to run it:
1. Prerequisites: Must have Python3 and Google Chrome on your system
2. Run: **pip3 install -r requirements.txt**
3. Run: **python3 Wicked.py**
4. Input your username/email/phone # and password for Instagram (MFA code too, if enabled), and wait a few minutes for it to return the results. Run time is dependant on how many people you follow / follow you

_Note:_ 

_1. This program does not log your username or password, it simply passes it to the Instagram login form._    
_2. This program uses HTTPS and TLSv1.2 to send information to Instagram._

</br>

### Sample Program Output
![alt text](https://github.com/kyletimmermans/wicked/blob/master/output_screenshot.png "Sample Program Output")

</br>

### Changelog
<div>v1.0: Initial-Release</div>
<div>v2.0:<div>
<div>&ensp;&ensp;-Handle for possible incorrect username and password and re-input them if their incorrect</div>
<div>&ensp;&ensp;-Handle path change for different Operating Systems (Windows, OSX, Linux)</div>
<div>&ensp;&ensp;-Automatically add and then remove a line from 'hosts' file to fix selenium error</div>
<div>v2.1: Added progress bars while loading results</div>
<div>v2.2:</div>
<div>&ensp;&ensp;-Added error handling for not being able to find the host file</div>
<div>&ensp;&ensp;-Added error handling for not finding chromedriver in the same folder as itself</div>
<div>&ensp;&ensp;-Added "Establishing Connection" print line
<div>&ensp;&ensp;-Removed logs showing up in console for Windows</div>
<div>v2.3:</div>
<div>&ensp;&ensp;-Added error handling for no internet connection</div>
<div>&ensp;&ensp;-Added better error handling for chromedriver not found in 'Wicked.py' directory</div> 
<div>&ensp;&ensp;-Better error handling for hosts file not found</div>
<div>&ensp;&ensp;-Syntax sugar added, small code cleanup</div> 
<div>v2.4:</div>
<div>&ensp;&ensp;-Fixed JavascriptException: Cannot read property 'scrollTo' of null</div>
<div>&ensp;&ensp;-Fixed issue where selenium couldn't find user profile div</div>
<div>&ensp;&ensp;-Fixed issue with output where '1' would randomly show up
<div>v2.5:</div>
<div>&ensp;&ensp;-Added final count of usernames along with Results</div>
<div>&ensp;&ensp;-Fixed issue with accounts that have a 'K' or 'M' in their following/followers number</div>
<div>&ensp;&ensp;-Login page needed to have 'react-root' replaced with 'loginForm'</div>
<div>&ensp;&ensp;-Automatically remove "Headless" from user agent string for the driver (Instagram can block headless ones)</div>
<div>&ensp;&ensp;-Fixed bs4 list iterator</div>
<div>&ensp;&ensp;-Logic for (following - followers) detailed in comments</div>
<div>v3.0:</div>
<div>&ensp;&ensp;-Using TLSv1.2 to send information</div>
<div>&ensp;&ensp;-Added MFA Support</div>
<div>&ensp;&ensp;-Added better correct-login checking</div>
<div>&ensp;&ensp;-Added v3 to the ASCII art title</div>
<div>&ensp;&ensp;-Removed JavaScript that scrolls div (was always changing) and sends scroll key instead</div>
<div>v3.1:</div>
<div>&ensp;&ensp;-Added Python Shebang</div>
<div>&ensp;&ensp;-Added if __name__ == "__main__":</div>
<div>&ensp;&ensp;-Refactor / Moved code into main</div>
<div>&ensp;&ensp;-Removed hard-coded XPATHs</div>
<div>&ensp;&ensp;-Added language chromedriver flag to force en-US</div>
<div>&ensp;&ensp;-Added --version and -v command line flag<div>
<div>v4.0:</div>
<div>&ensp;&ensp;-Updated banner to v4<div>
<div>&ensp;&ensp;-Added option to take email or phone number instead of just Instagram username<div>
<div>&ensp;&ensp;-Added support for million(s) and just 0 followers / following<div>
<div>&ensp;&ensp;-Using wakepy to prevent program from sleeping and crashing<div>
<div>&ensp;&ensp;-Deal with "Suggested for you" accounts in following modal</div>
<div>&ensp;&ensp;-Bug & Logic fixes</div> 
<div>&ensp;&ensp;-Selenium:</div>
<div>&ensp;&ensp;&ensp;&ensp;-Switched from executable_path to "service" model</div>
<div>&ensp;&ensp;&ensp;&ensp;-Switched to new "find_element(By.)" model</div>
<div>&ensp;&ensp;&ensp;&ensp;-No longer clicking follower / following modal, now visits links: instagram.com/{username}/followers</div>
<div>&ensp;&ensp;&ensp;&ensp;-Removed hard-coded cursor coordinates system for scrolling modal</div>
<div>&ensp;&ensp;&ensp;&ensp;-Using WebDriverWait to wait for elements to show up</div>
<div>v4.1: Print results to a .txt file</div>
<div>v4.5: Now using <a href="https://pypi.org/project/webdriver-manager/">webdriver-manager</a> to automatically install chromedriver</div>
<div>v4.6:</div>
<div>&ensp;&ensp;-Removed host file manipulation files<div>
<div>&ensp;&ensp;-Regex fixes<div>
<div>v4.7:</div>
<div>&ensp;&ensp;-Switched from getpass to pwinput for password masking<div>
<div>&ensp;&ensp;-Fix failed MFA retry support<div>
<div>&ensp;&ensp;-Scrolling method now requires devtools to open each time to load followers/following</div>
